import os
import json
from db.models import Agent as AgentModel
from db.init_db import SessionLocal

AGENTS_DIR = "data/agents"
os.makedirs(AGENTS_DIR, exist_ok=True)

def save_agent_to_file(agent_data):
    agent_id = agent_data["agent_id"]
    file_path = os.path.join(AGENTS_DIR, f"{agent_id}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(agent_data, f, indent=2, ensure_ascii=False)

def load_agent_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return AgentModel(**data)

def create_agent(agent_data):
    save_agent_to_file(agent_data)

def delete_agent(agent_id):
    file_path = os.path.join(AGENTS_DIR, f"{agent_id}.json")
    if os.path.exists(file_path):
        os.remove(file_path)

def list_agents():
    agents = []
    for filename in os.listdir(AGENTS_DIR):
        if filename.endswith(".json"):
            file_path = os.path.join(AGENTS_DIR, filename)
            try:
                agent = load_agent_from_file(file_path)
                agents.append(agent)
            except Exception as e:
                print(f"Erro ao carregar agente {filename}: {e}")
    return agents
