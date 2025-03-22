# agents/agent_interface.py

import streamlit as st
import json
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

            llms = list_llm_models()
            if not llms:
                st.warning("⚠️ Cadastre um modelo LLM primeiro na aba 'Modelos LLM'.")
                return

            modelo_escolhido = st.selectbox(
                "Selecione o Modelo LLM",
                options=llms,
                format_func=lambda m: f"{m.name} ({m.provider})"
            )

            submitted = st.form_submit_button("Salvar Agente")
            if submitted:
                try:
                    tools_data = json.loads(tools)
                    llm_data = {
                        "provider": modelo_escolhido.provider,
                        "config": modelo_escolhido.config_json
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
                        "llm_config": llm_data
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
                    st.code(json.dumps(agente.llm_config, indent=2, ensure_ascii=False), language="json")

                    if st.button(f"🗑️ Excluir {agente.agent_id}", key=f"del_{agente.id}"):
                        delete_agent(agente.agent_id)
                        st.success(f"Agente '{agente.agent_id}' excluído com sucesso!")
                        st.rerun()
