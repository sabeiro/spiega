"""
Connection payload scanning with progressive NDJSON results.

NVIDIA Morpheus normally runs as a separate GPU pipeline. This module provides:
- local: heuristic scoring (works without Morpheus).
- http: POST batch to MORPHEUS_INFER_URL and map predictions to verdicts.

See README for env vars.
"""
from __future__ import annotations

import hashlib
import json
import logging
import math
import os
import re
from typing import Any, AsyncIterator

import httpx

log = logging.getLogger("mcp-agent.connection_scan")

CONNECTION_SCAN_MAX = int(os.environ.get("CONNECTION_SCAN_MAX", "5000"))
ENGINE_MODE = (os.environ.get("CONNECTION_SCAN_ENGINE") or "local").strip().lower()
MORPHEUS_INFER_URL = (os.environ.get("MORPHEUS_INFER_URL") or "").strip()

SUSPICIOUS_PORTS = frozenset({4444, 5555, 6667, 31337, 23, 135, 139, 445, 3389, 1433, 6379})
SHELLISH = re.compile(
    r"(powershell|/bin/bash|cmd\.exe|wget\s+http|curl\s+.*\|\s*sh|base64\s+-d|"
    r"eval\s*\(|/dev/tcp|\$\{IFS\})",
    re.I,
)


def _shannon_entropy(s: str) -> float:
    if not s:
        return 0.0
    freq: dict[str, int] = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1
    n = len(s)
    h = 0.0
    for c in freq.values():
        p = c / n
        h -= p * math.log2(p)
    return h


def _stable_noise(conn: dict[str, Any]) -> float:
    blob = json.dumps(conn, sort_keys=True, default=str).encode()
    h = hashlib.sha256(blob).digest()
    return int.from_bytes(h[:8], "big") / (2**64)


def classify_connection_local(conn: dict[str, Any]) -> tuple[str, float, str]:
    if not isinstance(conn, dict):
        return "malicious", 1.0, "non_object_record"

    if conn.get("malicious") is True or str(conn.get("verdict", "")).lower() == "malicious":
        return "malicious", 0.95, "explicit_flag"

    score = 0.0
    reasons: list[str] = []

    try:
        port = int(conn.get("dst_port") or conn.get("dport") or conn.get("port") or 0)
    except (TypeError, ValueError):
        port = 0
    if port in SUSPICIOUS_PORTS:
        score += 0.35
        reasons.append("suspicious_dst_port=%s" % port)

    for key in ("payload", "payload_sample", "http_path", "uri", "user_agent", "command"):
        val = conn.get(key)
        if isinstance(val, str) and val:
            if SHELLISH.search(val):
                score += 0.45
                reasons.append("pattern:%s" % key)
            ent = _shannon_entropy(val[:2048])
            if ent > 4.5 and len(val) > 32:
                score += 0.12
                reasons.append("high_entropy:%s" % key)

    rs = conn.get("risk_score")
    if isinstance(rs, (int, float)):
        if rs > 0.75:
            score += 0.4
            reasons.append("risk_score_high")
        elif rs > 0.5:
            score += 0.15
            reasons.append("risk_score_med")

    score = min(1.0, score + _stable_noise(conn) * 0.08)

    verdict = "malicious" if score >= 0.55 else "ok"
    reason = (
        "; ".join(reasons)
        if reasons
        else ("elevated_score" if verdict == "malicious" else "clean_heuristic")
    )
    return verdict, round(score, 4), reason


async def fetch_morpheus_predictions(connections: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not MORPHEUS_INFER_URL:
        raise RuntimeError("MORPHEUS_INFER_URL not set for http engine")
    async with httpx.AsyncClient(timeout=120.0) as client:
        r = await client.post(
            MORPHEUS_INFER_URL,
            json={"connections": connections},
            headers={"Content-Type": "application/json"},
        )
        r.raise_for_status()
        data = r.json()
    preds = data.get("predictions")
    if not isinstance(preds, list) or len(preds) != len(connections):
        raise ValueError(
            "predictions must be a list of length %d" % len(connections)
        )
    return preds


def _normalize_prediction(p: Any, idx: int) -> tuple[str, float, str]:
    if not isinstance(p, dict):
        return "malicious", 1.0, "bad_prediction[%d]" % idx
    v = p.get("verdict") or p.get("label") or p.get("class")
    s = p.get("score")
    if isinstance(v, str) and v.lower() in ("malicious", "malware", "attack", "bad", "1", "true"):
        verdict = "malicious"
    elif isinstance(v, str) and v.lower() in ("ok", "benign", "clean", "good", "0", "false"):
        verdict = "ok"
    else:
        verdict = "ok"
    score = float(s) if isinstance(s, (int, float)) else (0.8 if verdict == "malicious" else 0.2)
    reason = str(p.get("reason") or p.get("detail") or "morpheus_http")
    return verdict, score, reason


async def scan_stream(
    connections: list[dict[str, Any]],
    progress_every: int = 1,
) -> AsyncIterator[str]:
    n = len(connections)
    mode = ENGINE_MODE
    if mode == "http" and not MORPHEUS_INFER_URL:
        log.warning("CONNECTION_SCAN_ENGINE=http but MORPHEUS_INFER_URL empty; falling back to local")
        mode = "local"

    engine_label = "morpheus_http" if mode == "http" else "local_heuristic"

    yield json.dumps(
        {
            "type": "start",
            "total": n,
            "engine": engine_label,
            "note": (
                "Morpheus HTTP sidecar"
                if mode == "http"
                else "Heuristic stand-in; set MORPHEUS_INFER_URL for Morpheus-backed inference"
            ),
        }
    ) + "\n"

    predictions: list[tuple[str, float, str]] = []
    if mode == "http":
        try:
            raw_preds = await fetch_morpheus_predictions(connections)
            for i, p in enumerate(raw_preds):
                predictions.append(_normalize_prediction(p, i))
        except Exception as e:
            yield json.dumps({"type": "error", "message": str(e)}) + "\n"
            return
    else:
        for c in connections:
            predictions.append(classify_connection_local(c))

    ok_count = 0
    mal_count = 0
    pe = max(1, int(progress_every))

    for i, conn in enumerate(connections):
        verdict, score, reason = predictions[i]
        if verdict == "malicious":
            mal_count += 1
        else:
            ok_count += 1

        if (i + 1) % pe == 0 or (i + 1) == n:
            yield json.dumps(
                {
                    "type": "progress",
                    "processed": i + 1,
                    "total": n,
                    "ok": ok_count,
                    "malicious": mal_count,
                }
            ) + "\n"

        yield json.dumps(
            {
                "type": "item",
                "index": i,
                "verdict": verdict,
                "score": score,
                "reason": reason,
                "summary": _summarize_conn(conn),
            }
        ) + "\n"

    yield json.dumps(
        {
            "type": "done",
            "total": n,
            "ok": ok_count,
            "malicious": mal_count,
            "engine": engine_label,
        }
    ) + "\n"


def _summarize_conn(conn: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k in ("src_ip", "dst_ip", "dst_port", "dport", "port", "proto", "service"):
        if k in conn:
            out[k] = conn[k]
    return out


async def scan_sync_async(connections: list[dict[str, Any]]) -> dict[str, Any]:
    n = len(connections)
    mode = ENGINE_MODE
    if mode == "http" and not MORPHEUS_INFER_URL:
        mode = "local"
    engine_label = "morpheus_http" if mode == "http" else "local_heuristic"

    if mode == "http":
        raw_preds = await fetch_morpheus_predictions(connections)
        preds = [_normalize_prediction(p, i) for i, p in enumerate(raw_preds)]
    else:
        preds = [classify_connection_local(c) for c in connections]
    items = []
    ok_count = mal_count = 0
    for i, conn in enumerate(connections):
        verdict, score, reason = preds[i]
        if verdict == "malicious":
            mal_count += 1
        else:
            ok_count += 1
        items.append(
            {
                "index": i,
                "verdict": verdict,
                "score": score,
                "reason": reason,
                "summary": _summarize_conn(conn),
            }
        )
    return {
        "total": n,
        "ok": ok_count,
        "malicious": mal_count,
        "engine": engine_label,
        "results": items,
    }


def validate_connections_body(body: Any) -> tuple[list[dict[str, Any]], int]:
    if not isinstance(body, dict):
        raise ValueError("body must be a JSON object")
    raw = body.get("connections")
    if not isinstance(raw, list):
        raise ValueError("connections must be a JSON array")
    if len(raw) > CONNECTION_SCAN_MAX:
        raise ValueError("too many connections (max %d)" % CONNECTION_SCAN_MAX)
    out: list[dict[str, Any]] = []
    for i, item in enumerate(raw):
        if isinstance(item, dict):
            out.append(item)
        else:
            out.append({"_raw": item, "index": i})
    progress_every = body.get("progress_every", 1)
    try:
        pe = int(progress_every)
    except (TypeError, ValueError):
        pe = 1
    return out, max(1, pe)
