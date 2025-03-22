import streamlit as st
import json
import sys

from agents.agent_manager import create_agent, delete_agent, list_agents
from tasks.task_manager import create_task, delete_task, list_tasks
from playground.chat_interface import chat_playground_interface
from agents.agent_interface import agent_interface
from tasks.task_interface import task_interface
from playground.export_interface import export_import_interface
from playground.llm_interface import llm_interface
from playground.benchmark_interface import benchmark_interface
from playground.log_interface import log_interface


def rerun():
    """Executa um rerun compatível com versões antigas do Streamlit."""
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()


def agentes_interface():
    st.header("🤖 Cadastro e Configuração de Agentes")

    tab1, tab2 = st.tabs(["Criar Agente", "Lista de Agentes"])

    with tab1:
        with st.form("form_agente"):
            st.subheader("Novo Agente")
            agent_id = st.text_input("ID do Agente")
            name = st.text_input("Nome")
            role = st.text_input("Papel do Agente")
            goal = st.text_area("Objetivo")
            backstory = st.text_area("História (backstory)")
            verbose = st.checkbox("Verbose", True)
            allow_delegation = st.checkbox("Permitir delegação")
            memory = st.checkbox("Memória")
            tools = st.text_area("Ferramentas (JSON)", "[]")
            llm_config = st.text_area(
                "Configuração do LLM (JSON) *",
                value=json.dumps({
                    "provider": "openai",
                    "config": {
                        "model": "gpt-3.5-turbo",
                        "api_key": "sua-api-key-aqui",
                        "temperature": 0.5
                    }
                }, indent=2),
                height=200,
                help="Este campo é obrigatório. Exemplo: {'provider': 'openai', 'config': {'model': 'gpt-3.5-turbo', 'api_key': 'chave', 'temperature': 0.5}}"
            )

            submitted = st.form_submit_button("Salvar Agente")
            if submitted:
                try:
                    tools_json = json.loads(tools)
                    llm_json = json.loads(llm_config)

                    if "provider" not in llm_json or "config" not in llm_json:
                        st.error("⚠️ A configuração do LLM deve conter os campos 'provider' e 'config'.")
                        return

                    if "model" not in llm_json["config"]:
                        st.error("⚠️ O campo 'model' dentro de 'config' é obrigatório.")
                        return

                    data = {
                        "agent_id": agent_id,
                        "name": name,
                        "role": role,
                        "goal": goal,
                        "backstory": backstory,
                        "verbose": verbose,
                        "allow_delegation": allow_delegation,
                        "memory": memory,
                        "tools": tools_json,
                        "llm_config": llm_json,
                    }
                    create_agent(data)
                    st.success(f"Agente '{name}' criado com sucesso!")
                    rerun()

                except json.JSONDecodeError:
                    st.error("Erro no formato JSON das ferramentas ou do LLM.")

    with tab2:
        st.subheader("Agentes cadastrados")
        agentes = list_agents()
        if agentes:
            for agente in agentes:
                st.write(f"**{agente.name}** ({agente.agent_id}) - {agente.role}")
                with st.expander("🔍 Ver detalhes do agente"):
                    st.code(json.dumps(agente.llm_config, indent=2), language="json")
                if st.button(f"Excluir {agente.agent_id}", key=f"del_{agente.agent_id}"):
                    try:
                        delete_agent(agente.agent_id)
                        st.success(f"Agente '{agente.agent_id}' excluído!")
                        rerun()
                    except Exception as e:
                        st.error(f"Erro ao excluir agente: {e}")
        else:
            st.info("Nenhum agente cadastrado ainda.")


def tarefas_interface():
    st.header("📋 Cadastro e Configuração de Tarefas")

    tab1, tab2 = st.tabs(["Criar Tarefa", "Lista de Tarefas"])

    with tab1:
        with st.form("form_tarefa"):
            name = st.text_input("Nome da Tarefa")
            description = st.text_area("Descrição da Tarefa")
            expected_output = st.text_area("Resultado Esperado", placeholder="Ex: Resposta clara e objetiva")
            agent_id = st.number_input("ID do Agente", step=1)
            dependencies = st.text_area("Dependências (JSON)", value="[]")

            submitted = st.form_submit_button("Salvar Tarefa")
            if submitted:
                if not expected_output.strip():
                    st.error("O campo 'Resultado Esperado' é obrigatório.")
                else:
                    try:
                        deps = json.loads(dependencies)
                        data = {
                            "name": name,
                            "description": description,
                            "expected_output": expected_output.strip(),
                            "agent_id": agent_id,
                            "dependencies": deps
                        }
                        create_task(data)
                        st.success(f"Tarefa '{name}' criada com sucesso!")
                        rerun()
                    except json.JSONDecodeError:
                        st.error("Erro no formato JSON das dependências.")

    with tab2:
        tarefas = list_tasks()
        if not tarefas:
            st.info("Nenhuma tarefa cadastrada.")
        else:
            for tarefa in tarefas:
                st.write(f"**{tarefa.name}** (Agente ID: {tarefa.agent_id})")
                st.markdown(f"> {tarefa.description}")
                if st.button(f"Excluir {tarefa.name}", key=f"del_{tarefa.id}"):
                    try:
                        delete_task(tarefa.id)
                        st.success(f"Tarefa '{tarefa.name}' excluída.")
                        rerun()
                    except Exception as e:
                        st.error(f"Erro ao excluir tarefa: {e}")


def main():
    if "--benchmark" in sys.argv:
        benchmark_interface()
        return

    st.set_page_config(page_title="CrewAI Playground", layout="wide")
    st.title("🚀 CrewAI Playground")
    st.sidebar.title("📌 Navegação")

    menu_options = {
        "🏠 Dashboard": "Dashboard",
        "🤖 Agentes": "Agentes",
        "📋 Tarefas": "Tarefas",
        "🧠 Modelos LLM": "ModelosLLM",
        "🎮 Playground": "Playground",
        "📁 Importação/Exportação": "ImportExport",
        "📊 Benchmarks": "Benchmarks"
    }

    menu = st.sidebar.radio("Selecione uma opção", list(menu_options.keys()))

    match menu_options[menu]:
        case "Dashboard":
            st.header("🏠 Dashboard")
            st.write("Resumo rápido do sistema aqui.")
        case "Agentes":
            agentes_interface()
        case "Tarefas":
            tarefas_interface()
        case "ModelosLLM":
            llm_interface()
        case "Playground":
            chat_playground_interface()
        case "ImportExport":
            export_import_interface()
        case "Benchmarks":
            benchmark_interface()


if __name__ == "__main__":
    main()
