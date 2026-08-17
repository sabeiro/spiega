import argparse
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
from typing import Any

import requests
import sys
import re


@lru_cache
def get_ollama_version(base_url: str) -> str:
    return requests.get(f"{base_url}/api/version").json().get("version", "unknown")


def _list_running_models(base_url: str) -> list[dict]:
    """Return the list of models currently loaded in Ollama."""
    try:
        resp = requests.get(f"{base_url}/api/ps")
        if resp.status_code != 200:
            return []
        data = resp.json()
        # API shape: {"models": [{"name": "model:tag", ...}, ...]}
        return data.get("models", []) if isinstance(data, dict) else []
    except Exception:
        return []


def _is_model_loaded(base_url: str, model_name: str) -> bool:
    """Check via Ollama API if the given model is currently loaded/warmed."""
    running = _list_running_models(base_url)
    for m in running:
        # Prefer 'name'; some responses may use 'model'
        name = m.get("name") or m.get("model")
        if name == model_name:
            return True
    return False


def ensure_model_warmed(base_url: str, model_name: str, *, timeout: float = 120.0, num_ctx: int | None = None) -> None:
    """
    Ensure the model is loaded into memory so benchmarking doesn't include load time.

    Strategy:
    - Check `GET /api/ps`. If present, it's already warmed.
    - If not loaded, send a tiny generation request (`num_predict: 1`) to trigger load.
    - Poll `GET /api/ps` until it appears or until `timeout`.
    """
    if _is_model_loaded(base_url, model_name):
        print(f"Model '{model_name}' is already loaded (warmed).")
        return

    print(f"Warming model '{model_name}' (loading into memory)...")

    # Trigger a minimal generation to force the model to load
    payload: dict[str, Any] = {
        "model": model_name,
        "prompt": " ",  # minimal prompt
        "stream": False,
        "options": {"num_predict": 1},  # generate 1 token to minimize work
    }
    if num_ctx:
        # Respect requested context size if provided
        payload["options"]["num_ctx"] = num_ctx

    try:
        resp = requests.post(f"{base_url}/api/generate", json=payload, timeout=timeout)
        if resp.status_code == 404:
            print(f"Error: Model '{model_name}' not found on this Ollama instance.")
            sys.exit(1)
        elif resp.status_code != 200:
            print(f"Warning: warm-up generate returned {resp.status_code}: {resp.text}")
    except requests.exceptions.RequestException as e:
        print(f"Warning: warm-up request failed: {e}")


def generate_with_ollama(model_name, prompt, base_url, num_ctx = None):
    """
    Generate text from an Ollama model and measure tokens per second.
    
    Args:
        model_name (str): The name of the Ollama model to use
        prompt (str): The input prompt to send to the model
        base_url (str): Base URL for the Ollama API
    
    Returns:
        dict: Statistics about the generation including tokens per second
    """
    url = f"{base_url}/api/generate"
    
    payload: dict[str, Any] = {
        "model": model_name,
        "prompt": prompt,
        "stream": False
    }

    if num_ctx:
        payload["options"] = { "num_ctx": num_ctx }

    print(f"Sending prompt to Ollama model '{model_name}'...")
    print(f"Prompt: {prompt}\n")
    
    try:
        start_time = time.time()
        response = requests.post(url, json=payload)
        end_time = time.time()
        
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response: {response.text}")
            sys.exit(1)
            
        result = response.json()
        
        # Extract relevant data
        total_duration = end_time - start_time  # Total wall clock time
        
        # Attempt to get model duration (convert from nanoseconds to seconds)
        # Some models might not return this data
        model_duration = result.get('total_duration', 0) / 1_000_000_000  
        if model_duration == 0:
            model_duration = total_duration  # Fallback to wall clock time
        
        # Get the generated text
        generated_text = result.get('response', '')
        
        # Estimate token counts since Ollama doesn't provide reliable counts for all models
        # This is a very rough estimate - 1 token is approximately 4 characters for English text
        est_prompt_tokens = len(prompt) // 4 + 1
        est_completion_tokens = len(generated_text) // 4 + 1
        est_total_tokens = est_prompt_tokens + est_completion_tokens
        
        # Calculate tokens per second for generation only
        tokens_per_second = est_completion_tokens / model_duration if model_duration > 0 else 0
        
        # Create statistics dictionary
        stats = {
            "version": get_ollama_version(base_url),
            "model": model_name,
            "num_ctx": num_ctx,
            "prompt_tokens": est_prompt_tokens,
            "completion_tokens": est_completion_tokens,
            "total_tokens": est_total_tokens,
            "processing_time": model_duration,
            "wall_clock_time": total_duration,
            "tokens_per_second": tokens_per_second,
            "response_text": generated_text,
            "note": "Token counts are estimated (4 chars ≈ 1 token)"
        }
        
        # Try to get actual token counts if available in the response
        if 'prompt_eval_count' in result and 'eval_count' in result:
            stats["prompt_tokens"] = result.get('prompt_eval_count', est_prompt_tokens)
            stats["completion_tokens"] = result.get('eval_count', est_completion_tokens)
            stats["total_tokens"] = stats["prompt_tokens"] + stats["completion_tokens"]
            stats["tokens_per_second"] = stats["completion_tokens"] / model_duration if model_duration > 0 else 0
            stats.pop("note", None)  # Remove the estimation note if we got actual counts
            
        return stats
        
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to Ollama at {base_url}. Is it running?")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def generate_with_ollama_stream(model_name, prompt, base_url, num_ctx = None):
    """
    Generate text from an Ollama model using streaming mode and measure tokens per second.
    This provides more accurate token counting.
    
    Args:
        model_name (str): The name of the Ollama model to use
        prompt (str): The input prompt to send to the model
        base_url (str): Base URL for the Ollama API
    
    Returns:
        dict: Statistics about the generation including tokens per second
    """
    url = f"{base_url}/api/generate"
    
    payload: dict[str, Any] = {
        "model": model_name,
        "prompt": prompt,
        "stream": True
    }

    if num_ctx:
        payload["options"] = { "num_ctx": num_ctx }

    print(f"Sending prompt to Ollama model '{model_name}' (streaming mode)...")
    print(f"Prompt: {prompt}\n")
    
    try:
        start_time = time.time()
        response = requests.post(url, json=payload, stream=True)
        
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response: {response.text}")
            sys.exit(1)
        
        generated_text = ""
        token_count = 0
        model_duration = 0
        prompt_eval_count = 0
        
        first_token_time = None
        
        for line in response.iter_lines():
            if not line:
                continue
                
            try:
                chunk = json.loads(line)
                
                # Update generated text
                if 'response' in chunk:
                    generated_text += chunk['response']
                    token_count += 1
                    
                    # Record time of first token
                    if first_token_time is None:
                        first_token_time = time.time()
                
                # Get prompt evaluation count if available
                if 'prompt_eval_count' in chunk and prompt_eval_count == 0:
                    prompt_eval_count = chunk['prompt_eval_count']
                    
                # Get final stats when done
                if chunk.get('done', False):
                    model_duration = chunk.get('total_duration', 0) / 1_000_000_000  # Convert from nanoseconds to seconds
                    break
                    
            except json.JSONDecodeError:
                continue
                
        end_time = time.time()
        total_duration = end_time - start_time
        
        # If model duration is not available, use wall clock time
        if model_duration == 0:
            model_duration = total_duration
            
        # Calculate time to first token
        time_to_first_token = (first_token_time - start_time) if first_token_time else 0
        
        # Calculate tokens per second for generation only
        tokens_per_second = token_count / (model_duration - time_to_first_token) if (model_duration - time_to_first_token) > 0 else 0
        
        # Create statistics dictionary
        stats = {
            "version": get_ollama_version(base_url),
            "model": model_name,
            "num_ctx": num_ctx,
            "prompt_tokens": prompt_eval_count if prompt_eval_count > 0 else len(prompt) // 4 + 1,
            "completion_tokens": token_count,
            "total_tokens": prompt_eval_count + token_count if prompt_eval_count > 0 else token_count + len(prompt) // 4 + 1,
            "processing_time": model_duration,
            "time_to_first_token": time_to_first_token,
            "wall_clock_time": total_duration,
            "tokens_per_second": tokens_per_second,
            "response_text": generated_text
        }
        
        return stats
        
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to Ollama at {base_url}. Is it running?")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def display_results(stats):
    """Display the benchmark results in a readable format"""
    print("\n" + "="*50)
    print("OLLAMA BENCHMARK RESULTS")
    print("="*50)
    print(f"Version: {stats['version']}")
    print(f"Model: {stats['model']}")
    if stats['num_ctx']:
        print(f"Context size: {stats['num_ctx']}")
    print(f"Prompt tokens: {stats['prompt_tokens']}")
    print(f"Completion tokens: {stats['completion_tokens']}")
    print(f"Total tokens: {stats['total_tokens']}")
    if "time_to_first_token" in stats:
        print(f"Time to first token: {stats['time_to_first_token']:.4f} seconds")
    print(f"Processing time: {stats['processing_time']:.4f} seconds")
    print(f"Wall clock time: {stats['wall_clock_time']:.4f} seconds")
    print(f"Tokens per second: {stats['tokens_per_second']:.2f}")
    if "note" in stats:
        print(f"Note: {stats['note']}")
    print("="*50)
    print("\nGenerated response:")
    print("-"*50)
    print(stats['response_text'])
    print("-"*50)

def run_parallel(model_name, prompt, base_url, num_ctx, use_stream, parallel_count):
    """Run multiple requests in parallel and return aggregate results."""
    print(f"\nStarting {parallel_count} parallel requests to model '{model_name}'...\n")

    all_stats = []
    overall_start = time.time()

    with ThreadPoolExecutor(max_workers=parallel_count) as executor:
        futures = []
        for i in range(parallel_count):
            if use_stream:
                future = executor.submit(generate_with_ollama_stream, model_name, prompt, base_url, num_ctx)
            else:
                future = executor.submit(generate_with_ollama, model_name, prompt, base_url, num_ctx)
            futures.append(future)

        for i, future in enumerate(as_completed(futures)):
            stats = future.result()
            all_stats.append(stats)
            print(f"\n--- Request {i+1} of {parallel_count} completed ---")
            display_results(stats)

    overall_end = time.time()
    overall_wall_time = overall_end - overall_start

    total_completion_tokens = sum(s['completion_tokens'] for s in all_stats)
    total_prompt_tokens = sum(s['prompt_tokens'] for s in all_stats)
    total_tokens = sum(s['total_tokens'] for s in all_stats)
    avg_tps = sum(s['tokens_per_second'] for s in all_stats) / len(all_stats)
    aggregate_tps = total_completion_tokens / overall_wall_time if overall_wall_time > 0 else 0
    min_time = min(s['processing_time'] for s in all_stats)
    max_time = max(s['processing_time'] for s in all_stats)
    avg_time = sum(s['processing_time'] for s in all_stats) / len(all_stats)

    agg_stats = {
        "version": get_ollama_version(base_url),
        "model": model_name,
        "num_ctx": num_ctx,
        "parallel_requests": parallel_count,
        "total_prompt_tokens": total_prompt_tokens,
        "total_completion_tokens": total_completion_tokens,
        "total_tokens": total_tokens,
        "overall_wall_time": overall_wall_time,
        "aggregate_tokens_per_second": aggregate_tps,
        "average_tokens_per_second": avg_tps,
        "min_processing_time": min_time,
        "max_processing_time": max_time,
        "avg_processing_time": avg_time,
        "per_request": all_stats,
    }

    return agg_stats


def display_aggregate_results(agg_stats):
    """Display aggregate parallel benchmark results."""
    print("\n" + "="*50)
    print("OLLAMA AGGREGATE BENCHMARK RESULTS")
    print("="*50)
    print(f"Version: {agg_stats['version']}")
    print(f"Model: {agg_stats['model']}")
    if agg_stats['num_ctx']:
        print(f"Context size: {agg_stats['num_ctx']}")
    print(f"Parallel requests: {agg_stats['parallel_requests']}")
    print(f"Total prompt tokens: {agg_stats['total_prompt_tokens']}")
    print(f"Total completion tokens: {agg_stats['total_completion_tokens']}")
    print(f"Total tokens: {agg_stats['total_tokens']}")
    print(f"Overall wall time: {agg_stats['overall_wall_time']:.4f} seconds")
    print(f"Aggregate tokens per second: {agg_stats['aggregate_tokens_per_second']:.2f}")
    print(f"Average tokens per second (per request): {agg_stats['average_tokens_per_second']:.2f}")
    print(f"Processing time - min: {agg_stats['min_processing_time']:.4f}s, "
          f"max: {agg_stats['max_processing_time']:.4f}s, "
          f"avg: {agg_stats['avg_processing_time']:.4f}s")
    print("="*50)


def main():
    parser = argparse.ArgumentParser(description='Benchmark Ollama models for tokens per second')
    parser.add_argument('--model', '-m', required=True, help='Name of the Ollama model')
    parser.add_argument('--prompt', '-p', default="Tell me a joke", help='Prompt to send to the model (default: "Tell me a joke")')
    parser.add_argument('--url', '-u', default="http://localhost:11434", help='Base URL for the Ollama API (default: http://localhost:11434)')
    parser.add_argument('--stream', '-s', action='store_true', help='Use streaming mode for more accurate token counting')
    parser.add_argument('--context', '-c', type=int, help='Content size')
    parser.add_argument('--parallel', '-P', type=int, default=1, help='Number of parallel requests (default: 1)')
    parser.add_argument('--output', '-o', help='Output file for JSON results (optional)')
    
    args = parser.parse_args()
    
    # Remove trailing slash from URL if present
    base_url = args.url.rstrip('/')

    num_ctx = args.context if args.context else None

    ensure_model_warmed(base_url, args.model, timeout=120.0, num_ctx=num_ctx)

    if args.parallel > 1:
        agg_stats = run_parallel(args.model, args.prompt, base_url, num_ctx, args.stream, args.parallel)
        display_aggregate_results(agg_stats)
        stats = agg_stats  # Save aggregate for JSON output
    elif args.stream:
        stats = generate_with_ollama_stream(args.model, args.prompt, base_url, num_ctx)
        display_results(stats)
    else:
        stats = generate_with_ollama(args.model, args.prompt, base_url, num_ctx)
        display_results(stats)
    
    # Save results to file if specified
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(stats, f, indent=2)
        print(f"\nResults saved to {args.output}")

if __name__ == "__main__":
    main()
