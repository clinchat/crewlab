# agents/agent_manager.py

from db.init_db import SessionLocal
from db.models import Agent

# CRUD básico de Agentes

def create_agent(data):
    with SessionLocal() as session:
        agent = Agent(**data)
        session.add(agent)
        session.commit()
        session.refresh(agent)
        return agent

def get_agent_by_id(agent_id):
    with SessionLocal() as session:
        return session.query(Agent).filter(Agent.agent_id == agent_id).first()

def update_agent(agent_id, update_data):
    with SessionLocal() as session:
        agent = session.query(Agent).filter(Agent.agent_id == agent_id).first()
        if agent:
            for key, value in update_data.items():
                if hasattr(agent, key):
                    setattr(agent, key, value)
            session.commit()
            session.refresh(agent)
            return agent
        return None

def delete_agent(agent_id):
    with SessionLocal() as session:
        agent = session.query(Agent).filter(Agent.agent_id == agent_id).first()
        if agent:
            session.delete(agent)
            session.commit()
            return True
        return False

def list_agents():
    with SessionLocal() as session:
        return session.query(Agent).all()
