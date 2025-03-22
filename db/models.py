from sqlalchemy import Column, String, Integer, Text, Boolean, JSON
from sqlalchemy.orm import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(Text)
    expected_output = Column(Text)
    agent_id = Column(Integer, ForeignKey('agents.id'))
    dependencies = Column(JSON)

    agent = relationship("Agent")


class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String(50), unique=True, index=True)
    name = Column(String(100))
    role = Column(String(150))
    goal = Column(Text)
    backstory = Column(Text)
    verbose = Column(Boolean, default=True)
    allow_delegation = Column(Boolean, default=False)
    memory = Column(Boolean, default=False)
    tools = Column(JSON)
    llm_config = Column(JSON)

class LLMModel(Base):
    __tablename__ = 'llm_models'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    config_json = Column(JSON, nullable=False)
    description = Column(String)
