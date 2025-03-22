from db.database import engine, Base, SessionLocal
from agents.models import Agent
from tasks.models import Task
from llms.models import LLMModel

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso.")

    # Chama função para incluir exemplos padrão
    incluir_modelos_llm_exemplo()


def incluir_modelos_llm_exemplo():
    session = SessionLocal()

    modelo_nome = "Gemini 1.5 Flash"
    modelo_existente = session.query(LLMModel).filter_by(name=modelo_nome).first()

    if modelo_existente:
        print(f"ℹ️ Modelo '{modelo_nome}' já cadastrado. Pulando...")
        session.close()
        return

    exemplo_modelo = LLMModel(
        name=modelo_nome,
        provider="google",
        config_json={
            "model": "gemini-1.5-flash",
            "temperature": 0.7
            # ❌ api_key será inserida manualmente via interface
        },
        description="Modelo rápido da família Gemini 1.5 (via Google AI Studio)"
    )

    session.add(exemplo_modelo)
    session.commit()
    session.close()

    print(f"✅ Modelo '{modelo_nome}' incluído como exemplo padrão.")


if __name__ == "__main__":
    create_tables()

