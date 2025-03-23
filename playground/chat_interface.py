import streamlit as st
from agents.agent_manager import list_agents
from llms.llm_manager import list_llm_models
from crewai import Crew, Task
from crewai import Agent as CrewAgent
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI  # ✅ substituto compatível
from litellm import completion  # para contar tokens (opcional)

def executar_agente_interface():
    st.subheader("🎯 Executar um Agente com uma LLM")

    agentes = list_agents()
    llms = list_llm_models()

    if not agentes or not llms:
        st.warning("⚠️ É necessário ter ao menos um agente e uma LLM cadastrados.")
        return

    agente_selecionado = st.selectbox(
        "👤 Selecione o Agente",
        agentes,
        format_func=lambda a: f"{a.name} ({a.agent_id})"
    )

    llm_selecionada = st.selectbox(
        "🧠 Selecione a LLM",
        llms,
        format_func=lambda l: f"{l.name} ({l.provider})"
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    prompt = st.chat_input("💬 Envie sua mensagem para o agente:")

    if prompt:
        if prompt.strip().lower() == "#sair":
            st.success("🚪 Encerrando a conversa com o agente.")
            st.session_state.chat_history = []
            return

        with st.spinner("⏳ Executando agente..."):
            try:
                # Preparar LLM
                llm_config = llm_selecionada.config_json.copy()
                model = llm_config.pop("model", None)
                api_key = llm_config.pop("api_key", None)

                llm = ChatOpenAI(
                    model_name=model,
                    openai_api_key=api_key,
                    **llm_config
                )

                # Ferramentas (dummies por enquanto)
                tools = []
                if agente_selecionado.tools:
                    for tool in agente_selecionado.tools:
                        if isinstance(tool, dict) and "name" in tool:
                            tools.append(Tool(
                                name=tool["name"],
                                description=tool.get("description", "Sem descrição"),
                                func=lambda x: "🔧 Ferramenta ainda não implementada."
                            ))

                # Criar agente CrewAI
                agent = CrewAgent(
                    role=agente_selecionado.role,
                    goal=agente_selecionado.goal,
                    backstory=agente_selecionado.backstory,
                    verbose=agente_selecionado.verbose,
                    allow_delegation=agente_selecionado.allow_delegation,
                    tools=tools,
                    llm=llm
                )

                # Criar tarefa e crew
                task = Task(description=prompt, agent=agent)
                crew = Crew(
                    agents=[agent],
                    tasks=[task],
                    verbose=True
                )

                # Executar o Crew
                result = crew.kickoff()

                # Contar tokens (estimativa usando LiteLLM)
                token_info = completion(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    api_key=api_key,
                    **llm_config
                )
                usage = token_info.get("usage", {})
                prompt_tokens = usage.get("prompt_tokens", "N/A")
                completion_tokens = usage.get("completion_tokens", "N/A")
                total_tokens = usage.get("total_tokens", "N/A")

                # Atualizar histórico
                st.session_state.chat_history.append(("Usuário", prompt))
                st.session_state.chat_history.append(("Agente", result))

                for autor, mensagem in st.session_state.chat_history:
                    if autor == "Usuário":
                        st.chat_message("user").write(mensagem)
                    else:
                        st.chat_message("assistant").write(mensagem)

                st.info(f"📊 Tokens — Prompt: {prompt_tokens} | Resposta: {completion_tokens} | Total: {total_tokens}")

            except Exception as e:
                st.error(f"❌ Erro ao executar agente: {e}")


def comparar_agentes_interface():
    st.subheader("⚖️ Comparar dois agentes (em breve)")
    st.info("🚧 Esta funcionalidade será implementada em breve. Aguarde atualizações!")


def chat_playground_interface():
    st.header("🎮 Playground de Agentes")

    tab1, tab2 = st.tabs(["🎯 Executar um agente com uma LLM", "⚖️ Comparar dois agentes"])

    with tab1:
        executar_agente_interface()

    with tab2:
        comparar_agentes_interface()
