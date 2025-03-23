import streamlit as st
import json
import os
from agents.agent_manager import create_agent, delete_agent, list_agents
from llms.llm_manager import list_llm_models

def agent_interface():
    st.header("🤖 Cadastro e Gerenciamento de Agentes")

    tab1, tab2 = st.tabs(["➕ Novo Agente", "📋 Agentes Cadastrados"])

    with tab1:
        with st.form("form_criar_agente"):
            st.subheader("Cadastrar Novo Agente")

            agent_id = st.text_input("ID do Agente (único)")
            name = st.text_input("Nome do Agente")
            role = st.text_input("Papel do Agente")
            goal = st.text_area("Objetivo do Agente")
            backstory = st.text_area("História do Agente (backstory)")
            verbose = st.checkbox("Verbose (detalhar ações)", value=True)
            allow_delegation = st.checkbox("Permitir Delegação", value=False)
            memory = st.checkbox("Memória Ativada", value=False)

            tools = st.text_area("Ferramentas (formato JSON)", value="[]")

            modelos_llm = list_llm_models()
            llm_escolhida = st.selectbox("Modelo LLM", modelos_llm, format_func=lambda m: m.name)

            rag_files = st.file_uploader(
                "📂 Enviar arquivos de conhecimento (RAG)",
                type=["pdf", "docx", "doc", "txt", "csv", "xls", "xlsx", "md"],
                accept_multiple_files=True
            )

            submitted = st.form_submit_button("Salvar Agente")
            if submitted:
                try:
                    tools_data = json.loads(tools)

                    rag_paths = []
                    if rag_files:
                        rag_dir = os.path.join("data", "rag_files", agent_id)
                        os.makedirs(rag_dir, exist_ok=True)
                        for file in rag_files:
                            file_path = os.path.join(rag_dir, file.name)
                            with open(file_path, "wb") as f:
                                f.write(file.read())
                            rag_paths.append(file_path)

                    llm_data = {
                        "provider": llm_escolhida.provider,
                        "config": llm_escolhida.config_json
                    }

                    data = {
                        "agent_id": agent_id,
                        "name": name,
                        "role": role,
                        "goal": goal,
                        "backstory": backstory,
                        "verbose": verbose,
                        "allow_delegation": allow_delegation,
                        "memory": memory,
                        "tools": tools_data,
                        "llm_config": llm_data,
                        "rag_files": rag_paths
                    }

                    create_agent(data)
                    st.success(f"✅ Agente '{name}' criado com sucesso!")
                    st.rerun()

                except json.JSONDecodeError:
                    st.error("❌ Erro de formatação no JSON das ferramentas.")

    with tab2:
        st.subheader("📋 Lista de Agentes Cadastrados")

        agentes = list_agents()
        if not agentes:
            st.info("Nenhum agente cadastrado.")
        else:
            for agente in agentes:
                with st.expander(f"🤖 {agente.name} ({agente.agent_id})"):
                    st.markdown(f"**Papel:** {agente.role}")
                    st.markdown(f"**Objetivo:** {agente.goal}")
                    st.markdown(f"**Backstory:** {agente.backstory}")
                    st.markdown(f"**LLM:** {agente.llm_config.get('config', {}).get('model', 'Não especificado')} ({agente.llm_config.get('provider')})")

                    if hasattr(agente, "rag_files") and agente.rag_files:
                        st.markdown("**Arquivos RAG:**")
                        for file_path in agente.rag_files:
                            st.markdown(f"- {os.path.basename(file_path)}")

                    st.code(json.dumps(agente.llm_config, indent=2, ensure_ascii=False), language="json")

                    if st.button(f"🗑️ Excluir {agente.agent_id}", key=f"del_{agente.agent_id}"):
                        delete_agent(agente.agent_id)
                        st.success(f"Agente '{agente.agent_id}' excluído com sucesso!")
                        st.rerun()
