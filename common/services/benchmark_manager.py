import os
import json
from datetime import datetime
from uuid import uuid4

BENCHMARK_DIR = "benchmarks"
os.makedirs(BENCHMARK_DIR, exist_ok=True)

def save_benchmark(prompt, resultados):
    benchmark_id = str(uuid4())
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    benchmark = {
        "id": benchmark_id,
        "timestamp": timestamp,
        "prompt": prompt,
        "resultados": resultados
    }

    filename = f"{BENCHMARK_DIR}/{benchmark_id}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(benchmark, f, indent=2, ensure_ascii=False)

    return benchmark_id

def list_benchmarks():
    arquivos = sorted(os.listdir(BENCHMARK_DIR), reverse=True)
    return [f for f in arquivos if f.endswith(".json")]

def load_benchmark(filename):
    path = os.path.join(BENCHMARK_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
