# common/schemas.py

from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class AgentModel(BaseModel):
    agent_id: str
    name: str
    role: str
    goal: str
    backstory: str
    verbose: bool = True
    allow_delegation: bool = False
    memory: bool = False
    tools: List[Dict[str, Any]] = []
    llm_config: Dict[str, Any]
    rag_files: Optional[List[str]] = []

    class Config:
        orm_mode = True
