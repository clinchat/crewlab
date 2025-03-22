# llms/llm_manager.py

from typing import List, Optional
from db.init_db import SessionLocal
from db.models import LLMModel
from sqlalchemy.exc import SQLAlchemyError


def create_llm_model(data: dict):
    with SessionLocal() as session:
        model = LLMModel(**data)
        session.add(model)
        session.commit()
        session.refresh(model)
        # ⚠️ Retorne apenas o id ou copie os dados antes de fechar a sessão
        model_dict = {
            "id": model.id,
            "name": model.name,
            "provider": model.provider,
            "config_json": model.config_json,
            "description": model.description
        }
    return model_dict


def list_llm_models() -> List[LLMModel]:
    """Retorna todos os modelos LLM cadastrados."""
    with SessionLocal() as session:
        return session.query(LLMModel).order_by(LLMModel.id.desc()).all()


def get_llm_model_by_id(model_id: int) -> Optional[LLMModel]:
    """Busca um modelo LLM pelo ID."""
    with SessionLocal() as session:
        return session.query(LLMModel).filter(LLMModel.id == model_id).first()


def delete_llm_model(model_id: int) -> bool:
    """Remove um modelo LLM pelo ID."""
    try:
        with SessionLocal() as session:
            model = session.query(LLMModel).filter(LLMModel.id == model_id).first()
            if model:
                session.delete(model)
                session.commit()
                return True
            return False
    except SQLAlchemyError as e:
        print(f"Erro ao deletar modelo LLM: {e}")
        return False
