# logs/log_manager.py
import os
import json
from datetime import datetime

LOG_DIR = "logs"

def ensure_log_dir_exists():
    os.makedirs(LOG_DIR, exist_ok=True)

def write_log(action: str, data: dict):
    ensure_log_dir_exists()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{action}.json"
    filepath = os.path.join(LOG_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": timestamp,
            "action": action,
            "data": data
        }, f, indent=2, ensure_ascii=False)

def list_logs():
    ensure_log_dir_exists()
    return sorted([f for f in os.listdir(LOG_DIR) if f.endswith(".json")], reverse=True)

def read_log(filename: str):
    filepath = os.path.join(LOG_DIR, filename)
    if not os.path.exists(filepath):
        return {"erro": "Arquivo de log não encontrado."}

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
