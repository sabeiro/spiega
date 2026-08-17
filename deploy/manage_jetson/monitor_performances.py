import requests
import time
import psutil
import pynvml

pynvml.nvmlInit()
handle = pynvml.nvmlDeviceGetHandleByIndex(0)

def benchmark_ollama(model, prompt, iterations=10):
    metrics = []
    
    for i in range(iterations):
        # GPU metrics before
        gpu_mem_before = pynvml.nvmlDeviceGetMemoryInfo(handle).used
        
        start_time = time.time()
        response = requests.post('http://localhost:11434/api/generate',
            json={
                'model': model,
                'prompt': prompt,
                'stream': False
            })
        end_time = time.time()
        
        # GPU metrics after
        gpu_mem_after = pynvml.nvmlDeviceGetMemoryInfo(handle).used
        gpu_util = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
        
        metrics.append({
            'latency': end_time - start_time,
            'gpu_memory_delta': gpu_mem_after - gpu_mem_before,
            'gpu_utilization': gpu_util,
            'tokens': response.json().get('eval_count', 0)
        })
    
    return metrics

# Run benchmark
results = benchmark_ollama('llama2:13b', 'Explain quantum computing', 10)
avg_latency = sum(r['latency'] for r in results) / len(results)
avg_tokens_per_sec = sum(r['tokens']/r['latency'] for r in results) / len(results)

print(f"Average Latency: {avg_latency:.2f}s")
print(f"Average Throughput: {avg_tokens_per_sec:.2f} tokens/sec")
