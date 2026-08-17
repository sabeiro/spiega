#!/usr/bin/env python3
"""
Agent that injects MCP tools into Ollama chat requests and runs the tool-call loop.
POST /api/chat receives the same body as Ollama; we add tools, call Ollama, execute any
tool_calls, and repeat until the model returns a final response. This makes the model
aware of and able to use current_date, numpy math, ollama_* etc. without the client
having to implement the loop.
"""
from __future__ import annotations

import asyncio
import base64
import json
import logging
import os
import re
import secrets
import sqlite3
import time
from typing import Any, Callable
from llama_cpp import Llama

import cv2

# Response logging: when payload options.log_response or log_response is true, store in SQLite (join on req_id with performance logs)
RESPONSE_LOG_DB = os.environ.get("OLLAMA_RESPONSE_LOG_DB", "/app/data/response_log.db")

# Structured logs to stderr for Ansible/container logs (req_id, stage, duration_ms)
logging.basicConfig(
    level=logging.DEBUG if os.environ.get("MCP_AGENT_DEBUG") else logging.INFO,
    format="%(asctime)s [mcp-agent] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
log = logging.getLogger("mcp-agent")

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles

from connection_scan import scan_stream as _connection_scan_stream
from connection_scan import scan_sync_async as _connection_scan_sync
from connection_scan import validate_connections_body as _validate_connections_body

# Limit concurrent requests to Ollama to avoid OOM (stacking loads)
OLLAMA_AGENT_MAX_CONCURRENT = int(os.environ.get("OLLAMA_AGENT_MAX_CONCURRENT", "1"))
# When set (bytes), do not forward if Ollama already uses this much VRAM (from /api/ps). Empty = disabled.
_raw = (os.environ.get("OLLAMA_MAX_VRAM_BYTES") or "").strip()
OLLAMA_MAX_VRAM_BYTES = int(_raw) if _raw else None
# How long to wait for capacity (VRAM under limit) before returning 503 (seconds)
OLLAMA_CAPACITY_WAIT = float(os.environ.get("OLLAMA_CAPACITY_WAIT", "5.0"))
# Retry Ollama request on runner crash / OOM before returning 503
OLLAMA_RETRY_ATTEMPTS = int(os.environ.get("OLLAMA_RETRY_ATTEMPTS", "3"))
OLLAMA_RETRY_DELAY = float(os.environ.get("OLLAMA_RETRY_DELAY", "5.0"))

_ollama_semaphore: asyncio.Semaphore | None = None

def _get_semaphore() -> asyncio.Semaphore:
    global _ollama_semaphore
    if _ollama_semaphore is None:
        _ollama_semaphore = asyncio.Semaphore(OLLAMA_AGENT_MAX_CONCURRENT)
    return _ollama_semaphore

# Import tool implementations from server (same process, no HTTP)
from server import (
    camera_describe_scene,
    current_date,
    numpy_array_op,
    numpy_binary_op,
    numpy_unary_op,
    ollama_chat,
    ollama_list_models,
    ollama_show_model,
)

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://ollama:11434")
# Default model when the client omits "model" in JSON (e.g. minimal clients). Client-sent model always wins when non-empty.
OLLAMA_TOOL_MODEL = (os.environ.get("OLLAMA_TOOL_MODEL") or "").strip() or None
# Debug endpoints: camera index and vision model (same as server.py for camera_describe_scene)
CAMERA_INDEX = int(os.environ.get("CAMERA_INDEX", "0"))
OLLAMA_VISION_MODEL = os.environ.get("OLLAMA_VISION_MODEL", "llava")
MAX_TOOL_LOOPS = 10

# Ollama-format tool definitions; kept short to reduce tokens and VRAM (Jetson 7.4 GiB)
OLLAMA_TOOLS: list[dict[str, Any]] = [
    {"type": "function", "function": {"name": "ollama_list_models", "description": "List Ollama models.", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "ollama_show_model", "description": "Show model info.", "parameters": {"type": "object", "required": ["name"], "properties": {"name": {"type": "string"}}}}},
    {"type": "function", "function": {"name": "ollama_chat", "description": "Chat with a model.", "parameters": {"type": "object", "required": ["model", "message"], "properties": {"model": {"type": "string"}, "message": {"type": "string"}, "stream": {"type": "boolean", "default": False}}}}},
    {"type": "function", "function": {"name": "current_date", "description": "Current date/time.", "parameters": {"type": "object", "properties": {"include_time": {"type": "boolean", "default": True}, "iso_only": {"type": "boolean", "default": True}}}}},
    {"type": "function", "function": {"name": "numpy_array_op", "description": "Aggregate numbers: sum, mean, std, min, max, prod, median.", "parameters": {"type": "object", "required": ["operation", "values"], "properties": {"operation": {"type": "string"}, "values": {"type": "array", "items": {"type": "number"}}}}}},
    {"type": "function", "function": {"name": "numpy_binary_op", "description": "Two numbers: add, subtract, multiply, divide, power, remainder.", "parameters": {"type": "object", "required": ["operation", "a", "b"], "properties": {"operation": {"type": "string"}, "a": {"type": "number"}, "b": {"type": "number"}}}}},
    {"type": "function", "function": {"name": "numpy_unary_op", "description": "One number: sqrt, sin, cos, tan, log, log10, exp, abs, floor, ceil.", "parameters": {"type": "object", "required": ["operation", "x"], "properties": {"operation": {"type": "string"}, "x": {"type": "number"}}}}},
    {"type": "function", "function": {"name": "camera_describe_scene", "description": "Take a picture from the camera and return a text description of the scene (objects, etc.). Use when the user asks what you see or to describe the room.", "parameters": {"type": "object", "properties": {"prompt": {"type": "string", "description": "Question for the vision model (default: list objects in the image)."}}}}},
]

TOOL_FUNCTIONS: dict[str, Callable[..., str]] = {
    "ollama_list_models": ollama_list_models,
    "ollama_show_model": ollama_show_model,
    "ollama_chat": ollama_chat,
    "current_date": current_date,
    "numpy_array_op": numpy_array_op,
    "numpy_binary_op": numpy_binary_op,
    "numpy_unary_op": numpy_unary_op,
    "camera_describe_scene": camera_describe_scene,
}


def _response_log_init() -> None:
    d = os.path.dirname(RESPONSE_LOG_DB)
    if d:
        os.makedirs(d, exist_ok=True)
    with sqlite3.connect(RESPONSE_LOG_DB) as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS response_log (
                req_id TEXT PRIMARY KEY,
                model TEXT,
                effective_model TEXT,
                question TEXT,
                answer TEXT,
                total_ms INTEGER,
                max_loops INTEGER DEFAULT 0,
                created_at TEXT
            )"""
        )
        conn.commit()


def _response_log_insert(
    req_id: str,
    model: str,
    effective_model: str | None,
    question: str,
    answer: str,
    total_ms: int,
    max_loops: bool = False,
) -> None:
    try:
        _response_log_init()
        created = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        with sqlite3.connect(RESPONSE_LOG_DB) as conn:
            conn.execute(
                """INSERT OR REPLACE INTO response_log
                   (req_id, model, effective_model, question, answer, total_ms, max_loops, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (req_id, model, effective_model or "", question, answer, total_ms, 1 if max_loops else 0, created),
            )
            conn.commit()
    except Exception as e:
        log.warning("req_id=%s response_log insert failed: %s", req_id, e)


def parse_args(raw: dict[str, Any] | str) -> dict[str, Any]:
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {}
    return {}


def run_tool(name: str, arguments: dict[str, Any] | str) -> str:
    fn = TOOL_FUNCTIONS.get(name)
    if not fn:
        return json.dumps({"error": f"Unknown tool: {name}"})
    args = parse_args(arguments)
    try:
        return fn(**args)
    except Exception as e:
        return json.dumps({"error": str(e)})


async def _ollama_has_capacity() -> tuple[bool, str]:
    """Check Ollama /api/ps: return (True, '') if OK to send, else (False, reason)."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get(f"{OLLAMA_HOST}/api/ps")
            if r.status_code != 200:
                return False, f"Ollama /api/ps returned {r.status_code}"
            data = r.json()
            models = data.get("models") or []
            vram_used = sum((m.get("size_vram") or 0) for m in models)
            if OLLAMA_MAX_VRAM_BYTES is not None and vram_used >= OLLAMA_MAX_VRAM_BYTES:
                return False, f"Ollama VRAM at limit ({vram_used} >= {OLLAMA_MAX_VRAM_BYTES})"
            return True, ""
    except Exception as e:
        return False, str(e)
    
    
def parse_ollama_chat_response_body(text: str) -> dict[str, Any]:
    """Parse Ollama /api/chat response: one JSON object, or NDJSON stream (multiple lines).

    If Ollama streams despite ``stream: false`` (or a proxy buffers oddly), the body is
    several JSON objects with incremental ``message.content``. ``response.json()`` only
    decodes the first line, so the client sees the first token only. We merge all chunks.
    """
    text = (text or "").strip()
    if not text:
        return {}
    try:
        out = json.loads(text)
        return out if isinstance(out, dict) else {}
    except json.JSONDecodeError:
        pass
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    objs: list[dict[str, Any]] = []
    for line in lines:
        try:
            o = json.loads(line)
            if isinstance(o, dict):
                objs.append(o)
        except json.JSONDecodeError:
            continue
    if not objs:
        raise ValueError("no parseable JSON in Ollama /api/chat body")
    if len(objs) == 1:
        return objs[0]
    # NDJSON streaming shape: concatenate assistant deltas
    content_parts: list[str] = []
    thinking_parts: list[str] = []
    last_role = "assistant"
    tool_calls_final: Any = None
    meta: dict[str, Any] = {}
    for o in objs:
        for k, v in o.items():
            if k != "message":
                meta[k] = v
        m = o.get("message") or {}
        if not isinstance(m, dict):
            continue
        last_role = m.get("role") or last_role
        c = m.get("content")
        if isinstance(c, str) and c:
            content_parts.append(c)
        th = m.get("thinking")
        if isinstance(th, str) and th:
            thinking_parts.append(th)
        tc = m.get("tool_calls")
        if tc:
            tool_calls_final = tc
    merged: dict[str, Any] = {**meta, "done": True}
    msg_out: dict[str, Any] = {"role": last_role, "content": "".join(content_parts)}
    if thinking_parts:
        msg_out["thinking"] = "".join(thinking_parts)
    if tool_calls_final is not None:
        msg_out["tool_calls"] = tool_calls_final
    merged["message"] = msg_out
    return merged

async def cpp_chat(request: Request) -> JSONResponse:
    model_id = "bartowski/Meta-Llama-3.1-8B-Instruct-GGUF"
    llm = Llama.from_pretrained(repo_id=model_id,local_dir=os.environ['HOME'] + "/Downloads/llm_model/",filename="Meta-Llama-3.1-8B-Instruct-IQ2_M.gguf")
    req_id = secrets.token_hex(4)
    t_start = time.perf_counter()
    body = await request.json()
    _raw_model = body.get("model")
    if isinstance(_raw_model, str) and _raw_model.strip():
        model = _raw_model.strip()
        effective_model = model
    else:
        effective_model = OLLAMA_TOOL_MODEL or "bartowski/Meta-Llama-3.1-8B-Instruct-GGUF"
        model = effective_model
    messages = list(body.get("messages", []))
    stream = body.get("stream", False)
    options = body.get("options") or {}
    debug = options.get("debug") or body.get("debug") or os.environ.get("MCP_AGENT_DEBUG")
    log_response = options.get("log_response") or body.get("log_response")
    log.info("req_id=%s stage=request_received model=%s messages=%s", req_id, model, len(messages))
    if debug:
        log.info("req_id=%s [debug] payload_keys=%s", req_id, list(body.keys()))

    if not messages:
        return JSONResponse({"error": "messages required"}, status_code=400)

    # Non-streaming agent loop
    if stream:
        # For streaming we'd need to accumulate chunks and handle tool_calls; return 501 for now
        return JSONResponse({"error": "Streaming with tools not implemented; use stream: false"}, status_code=501)

    # Short system message to limit tokens (VRAM on Jetson)
    system_msg = {
        "role": "system",
        "content": "Use tools for time/date (current_date), math (numpy_*), models (ollama_list_models, ollama_show_model), and camera (camera_describe_scene for 'what do you see?' or describing the scene). Call the tool, report the result.",
    }
    messages_with_system = [system_msg] + messages

    if not (isinstance(_raw_model, str) and _raw_model.strip()) and OLLAMA_TOOL_MODEL:
        log.info(
            "req_id=%s stage=model_default (no model in request) effective_model=%s",
            req_id,
            effective_model,
        )
    payload = {
        "model": effective_model,
        "messages": messages_with_system,
        "stream": False,
        "tools": OLLAMA_TOOLS,
        "options": options,
    }

    sem = _get_semaphore()
    # Optional: wait for Ollama to have capacity (VRAM under limit) before acquiring semaphore
    t_cap = time.perf_counter()
    log.info("req_id=%s stage=capacity_wait_start", req_id)
    deadline = time.monotonic() + OLLAMA_CAPACITY_WAIT
    while True:
        ok, reason = await _ollama_has_capacity()
        if ok:
            break
        if time.monotonic() >= deadline:
            log.warning("req_id=%s stage=capacity_timeout reason=%s", req_id, reason)
            return JSONResponse(
                {"error": f"Ollama at capacity: {reason}", "retry_after": 10},
                status_code=503,
                headers={"Retry-After": "10"},
            )
        await asyncio.sleep(0.5)
    log.info("req_id=%s stage=capacity_ok duration_ms=%d", req_id, int((time.perf_counter() - t_cap) * 1000))


async def agent_chat(request: Request) -> JSONResponse:
    req_id = secrets.token_hex(4)
    t_start = time.perf_counter()
    body = await request.json()
    _raw_model = body.get("model")
    if isinstance(_raw_model, str) and _raw_model.strip():
        model = _raw_model.strip()
        effective_model = model
    else:
        effective_model = OLLAMA_TOOL_MODEL or "qwen2.5-coder:3b"
        model = effective_model
    messages = list(body.get("messages", []))
    stream = body.get("stream", False)
    options = body.get("options") or {}
    debug = options.get("debug") or body.get("debug") or os.environ.get("MCP_AGENT_DEBUG")
    log_response = options.get("log_response") or body.get("log_response")
    if "num_gpu" not in options:
        options["num_gpu"] = int(os.environ.get("OLLAMA_NUM_GPU", "20"))
    # Cap context so Ollama allocates less VRAM; avoids cudaMalloc OOM on 7.4 GiB (Jetson). Client can override.
    if "num_ctx" not in options:
        options["num_ctx"] = int(os.environ.get("OLLAMA_NUM_CTX", "2048"))

    log.info("req_id=%s stage=request_received model=%s messages=%s", req_id, model, len(messages))
    if debug:
        log.info("req_id=%s [debug] payload_keys=%s", req_id, list(body.keys()))

    if not messages:
        return JSONResponse({"error": "messages required"}, status_code=400)

    # Non-streaming agent loop
    if stream:
        # For streaming we'd need to accumulate chunks and handle tool_calls; return 501 for now
        return JSONResponse({"error": "Streaming with tools not implemented; use stream: false"}, status_code=501)

    # Short system message to limit tokens (VRAM on Jetson)
    system_msg = {
        "role": "system",
        "content": "Use tools for time/date (current_date), math (numpy_*), models (ollama_list_models, ollama_show_model), and camera (camera_describe_scene for 'what do you see?' or describing the scene). Call the tool, report the result.",
    }
    messages_with_system = [system_msg] + messages

    if not (isinstance(_raw_model, str) and _raw_model.strip()) and OLLAMA_TOOL_MODEL:
        log.info(
            "req_id=%s stage=model_default (no model in request) effective_model=%s",
            req_id,
            effective_model,
        )
    payload = {
        "model": effective_model,
        "messages": messages_with_system,
        "stream": False,
        "tools": OLLAMA_TOOLS,
        "options": options,
    }

    sem = _get_semaphore()
    # Optional: wait for Ollama to have capacity (VRAM under limit) before acquiring semaphore
    t_cap = time.perf_counter()
    log.info("req_id=%s stage=capacity_wait_start", req_id)
    deadline = time.monotonic() + OLLAMA_CAPACITY_WAIT
    while True:
        ok, reason = await _ollama_has_capacity()
        if ok:
            break
        if time.monotonic() >= deadline:
            log.warning("req_id=%s stage=capacity_timeout reason=%s", req_id, reason)
            return JSONResponse(
                {"error": f"Ollama at capacity: {reason}", "retry_after": 10},
                status_code=503,
                headers={"Retry-After": "10"},
            )
        await asyncio.sleep(0.5)
    log.info("req_id=%s stage=capacity_ok duration_ms=%d", req_id, int((time.perf_counter() - t_cap) * 1000))

    def _is_retryable(err: str) -> bool:
        e = str(err or "").lower()
        return (
            "out of memory" in e
            or "terminated" in e
            or "cudamalloc" in e
            or "runner" in e
        )

    async with sem:
        log.info("req_id=%s stage=sem_acquired", req_id)
        for loop_idx in range(MAX_TOOL_LOOPS):
            data = None
            for attempt in range(OLLAMA_RETRY_ATTEMPTS):
                t_ollama = time.perf_counter()
                log.info("req_id=%s stage=ollama_request_start loop=%s attempt=%s", req_id, loop_idx + 1, attempt + 1)
                try:
                    async with httpx.AsyncClient(timeout=120.0) as client:
                        r = await client.post(f"{OLLAMA_HOST}/api/chat", json=payload)
                except Exception as e:
                    ollama_ms = int((time.perf_counter() - t_ollama) * 1000)
                    log.warning("req_id=%s stage=ollama_error duration_ms=%d error=%s", req_id, ollama_ms, e)
                    if attempt < OLLAMA_RETRY_ATTEMPTS - 1:
                        log.info("req_id=%s stage=ollama_retry delay=%.0fs", req_id, OLLAMA_RETRY_DELAY)
                        await asyncio.sleep(OLLAMA_RETRY_DELAY)
                        continue
                    return JSONResponse(
                        {"error": f"Ollama unreachable: {e}", "retry_after": 5},
                        status_code=503,
                        headers={"Retry-After": "5"},
                    )
                ollama_ms = int((time.perf_counter() - t_ollama) * 1000)
                log.info("req_id=%s stage=ollama_response status=%s duration_ms=%d", req_id, r.status_code, ollama_ms)
                if r.status_code != 200:
                    err_text = r.text
                    try:
                        err_body = r.json()
                        err_msg = err_body.get("error", err_text)
                    except Exception:
                        err_msg = err_text
                    log.warning("req_id=%s stage=ollama_error status=%s duration_ms=%d msg=%s", req_id, r.status_code, ollama_ms, (err_msg or "")[:200])
                    retryable = r.status_code >= 500 or _is_retryable(err_msg)
                    if retryable and attempt < OLLAMA_RETRY_ATTEMPTS - 1:
                        log.info("req_id=%s stage=ollama_retry delay=%.0fs msg=%s", req_id, OLLAMA_RETRY_DELAY, (err_msg or "")[:80])
                        await asyncio.sleep(OLLAMA_RETRY_DELAY)
                        continue
                    if retryable:
                        return JSONResponse(
                            {"error": err_msg, "retry_after": 15},
                            status_code=503,
                            headers={"Retry-After": "15"},
                        )
                    return JSONResponse({"error": err_msg}, status_code=r.status_code)
                try:
                    data = parse_ollama_chat_response_body(r.text)
                except ValueError as e:
                    log.warning("req_id=%s stage=ollama_bad_body err=%s preview=%s", req_id, e, (r.text or "")[:200])
                    return JSONResponse(
                        {"error": f"Invalid Ollama response: {e}", "preview": (r.text or "")[:800]},
                        status_code=502,
                    )
                if len(r.text.strip().splitlines()) > 1 and data.get("message", {}).get("content"):
                    log.info(
                        "req_id=%s stage=ollama_merged_ndjson lines=%s content_len=%s",
                        req_id,
                        len([ln for ln in r.text.splitlines() if ln.strip()]),
                        len((data.get("message") or {}).get("content") or ""),
                    )
                err_in_body = data.get("error")
                if err_in_body and _is_retryable(err_in_body):
                    log.warning("req_id=%s stage=ollama_error body_error=%s", req_id, (str(err_in_body))[:200])
                    if attempt < OLLAMA_RETRY_ATTEMPTS - 1:
                        log.info("req_id=%s stage=ollama_retry delay=%.0fs", req_id, OLLAMA_RETRY_DELAY)
                        await asyncio.sleep(OLLAMA_RETRY_DELAY)
                        continue
                    return JSONResponse(
                        {"error": err_in_body, "retry_after": 15},
                        status_code=503,
                        headers={"Retry-After": "15"},
                    )
                break  # success
            msg = (data or {}).get("message") or {}
            tool_calls = list(msg.get("tool_calls") or [])
            # Parse tool call from content: formats {"name": "...", "arguments": {...}} or {"tool_name": {...}}
            if not tool_calls and msg.get("content"):
                content = (msg.get("content") or "").strip()
                if isinstance(content, str) and content.startswith("{"):
                    parsed = None
                    try:
                        parsed = json.loads(content)
                    except json.JSONDecodeError:
                        # Try fixing unquoted keys (e.g. {include_time: true} -> {"include_time": true})
                        fixed = re.sub(r"([{,]\s*)(\w+)(\s*:)", r'\1"\2"\3', content)
                        try:
                            parsed = json.loads(fixed)
                        except json.JSONDecodeError:
                            pass
                    if isinstance(parsed, dict):
                        if "name" in parsed:
                            tool_calls = [{
                                "type": "function",
                                "function": {
                                    "name": parsed["name"],
                                    "arguments": parsed.get("arguments") or {},
                                },
                            }]
                        elif len(parsed) == 1:
                            name = next(iter(parsed.keys()))
                            args = parsed[name]
                            if name in TOOL_FUNCTIONS and isinstance(args, dict):
                                tool_calls = [{
                                    "type": "function",
                                    "function": {"name": name, "arguments": args},
                                }]

            if not tool_calls:
                total_ms = int((time.perf_counter() - t_start) * 1000)
                log.info("req_id=%s stage=response_sent total_ms=%d", req_id, total_ms)
                # Eval log: question + answer with req_id for joining with performance logs
                question = ""
                for m in reversed(messages):
                    if m.get("role") == "user":
                        c = m.get("content")
                        question = c if isinstance(c, str) else json.dumps(c)[:10000]
                        break
                answer = msg.get("content") or ""
                answer = answer if isinstance(answer, str) else json.dumps(answer)[:10000]
                log.info("req_id=%s [eval] %s", req_id, json.dumps({"question": question, "answer": answer}, ensure_ascii=False))
                if log_response:
                    await asyncio.to_thread(
                        _response_log_insert,
                        req_id,
                        model,
                        effective_model,
                        question,
                        answer,
                        total_ms,
                        max_loops=False,
                    )
                return JSONResponse(data)

            log.info("req_id=%s stage=tool_calls count=%s", req_id, len(tool_calls))
            messages_with_system.append(msg)
            for tc in tool_calls:
                t_tool = time.perf_counter()
                fn = tc.get("function") or {}
                name = fn.get("name", "")
                args = fn.get("arguments") or {}
                if isinstance(args, str) and not args.strip():
                    args = {}
                result = run_tool(name, args)
                tool_ms = int((time.perf_counter() - t_tool) * 1000)
                log.info("req_id=%s stage=tool_done name=%s duration_ms=%d", req_id, name, tool_ms)
                if debug:
                    log.info("req_id=%s [debug] tool=%s result_len=%s", req_id, name, len(str(result)))
                messages_with_system.append({"role": "tool", "tool_name": name, "content": result})
            payload["messages"] = messages_with_system

        total_ms = int((time.perf_counter() - t_start) * 1000)
        log.warning("req_id=%s stage=max_loops_exceeded total_ms=%d", req_id, total_ms)
        last_msg = (data.get("message") or {})
        partial = last_msg.get("content") or ""
        partial = partial if isinstance(partial, str) else json.dumps(partial)[:10000]
        question = ""
        for m in reversed(messages):
            if m.get("role") == "user":
                c = m.get("content")
                question = c if isinstance(c, str) else json.dumps(c)[:10000]
                break
        log.info("req_id=%s [eval] %s", req_id, json.dumps({"question": question, "answer": partial, "max_loops": True}, ensure_ascii=False))
        if log_response:
            await asyncio.to_thread(
                _response_log_insert,
                req_id,
                model,
                effective_model,
                question,
                partial,
                total_ms,
                max_loops=True,
            )
        return JSONResponse({"error": "Max tool loops exceeded", "message": data.get("message")}, status_code=500)


def _capture_jpeg() -> bytes | None:
    """Capture one frame from the camera (cam0). Returns JPEG bytes or None on failure."""
    try:
        cap = cv2.VideoCapture(CAMERA_INDEX)
        if not cap.isOpened():
            return None
        ok, frame = cap.read()
        cap.release()
        if not ok or frame is None:
            return None
        _, jpeg = cv2.imencode(".jpg", frame)
        return jpeg.tobytes()
    except Exception:
        return None


app = FastAPI(
    title="Ollama agent (tools injected)",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Serve control UI at /control/ (same origin as /api/* for CORS-free testing)
# Register explicit routes before the mount so /control and /control/ are handled first.
_CONTROL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "control")


@app.get("/control", include_in_schema=False)
def control_redirect():
    """Redirect /control to /control/."""
    return RedirectResponse(url="/control/", status_code=301)


@app.get("/control/", include_in_schema=False)
def control_index():
    """Serve control UI index."""
    if os.path.isdir(_CONTROL_DIR):
        index = os.path.join(_CONTROL_DIR, "index.html")
        if os.path.isfile(index):
            return FileResponse(index)
    raise HTTPException(status_code=404, detail="control UI not found")


if os.path.isdir(_CONTROL_DIR):
    app.mount("/control", StaticFiles(directory=_CONTROL_DIR, html=True), name="control")
else:
    log.warning("control static dir not found: %s (rebuild image with static/)", _CONTROL_DIR)


@app.post("/api/chat")
async def api_chat(request: Request):
    return await agent_chat(request)

@app.post("/api/chat_cpp")
async def api_chat_cpp(request: Request):
    return await cpp_chat(request)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/screenshot")
def screenshot():
    """Debug: return current camera frame as JPEG (open in browser)."""
    jpeg = _capture_jpeg()
    if jpeg is None:
        return JSONResponse({"error": "Camera capture failed"}, status_code=503)
    return Response(content=jpeg, media_type="image/jpeg")


@app.get("/api/describe_vision")
def describe_vision():
    """Debug: return YOLO object-detection description of what the camera sees (same as camera_describe_scene tool)."""
    jpeg = _capture_jpeg()
    if jpeg is None:
        return JSONResponse({"error": "Camera capture failed"}, status_code=503)
    try:
        from vision import describe_scene_yolo
        description = describe_scene_yolo(jpeg)
        if description.strip().startswith("{"):
            return JSONResponse({"error": description}, status_code=503)
        return JSONResponse({"description": description, "engine": "yolo"})
    except Exception as e:
        return JSONResponse({"error": str(e), "engine": "yolo"}, status_code=503)


@app.get("/api/yolo")
def yolo_detections():
    """Return YOLO detections as JSON (bbox + label + confidence)."""
    jpeg = _capture_jpeg()
    if jpeg is None:
        return JSONResponse({"error": "Camera capture failed"}, status_code=503)
    try:
        from vision import detect_yolo
        detections = detect_yolo(jpeg)
        return JSONResponse({"detections": detections, "engine": "yolo"})
    except Exception as e:
        return JSONResponse({"error": str(e), "engine": "yolo"}, status_code=503)


@app.post("/api/connection_scan")
async def api_connection_scan(request: Request):
    """Classify connection payloads (local heuristic or Morpheus HTTP). Full JSON result."""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "invalid JSON body"}, status_code=400)
    try:
        conns, _ = _validate_connections_body(body)
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    result = await _connection_scan_sync(conns)
    return JSONResponse(result)


@app.post("/api/connection_scan/stream")
async def api_connection_scan_stream(request: Request):
    """NDJSON stream: start, progress, item (per connection), done. See README."""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "invalid JSON body"}, status_code=400)
    try:
        conns, pe = _validate_connections_body(body)
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)

    async def ndjson_body():
        async for chunk in _connection_scan_stream(conns, progress_every=pe):
            yield chunk

    return StreamingResponse(ndjson_body(), media_type="application/x-ndjson")


@app.get("/api/yolo_image")
def yolo_image():
    """Return the camera frame with YOLO bounding boxes and labels drawn (standard visual)."""
    jpeg = _capture_jpeg()
    if jpeg is None:
        return JSONResponse({"error": "Camera capture failed"}, status_code=503)
    try:
        from vision import plot_yolo
        out_jpeg = plot_yolo(jpeg)
        if out_jpeg is None:
            return JSONResponse({"error": "YOLO plot failed"}, status_code=503)
        return Response(content=out_jpeg, media_type="image/jpeg")
    except Exception as e:
        return JSONResponse({"error": str(e), "engine": "yolo"}, status_code=503)

