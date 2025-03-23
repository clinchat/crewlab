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
        "🤖 Agentes (Agents)": "Agentes",
        "📋 Tarefas (Tasks)": "Tarefas",
        "🧠 Modelos LLM (Models LLM)": "ModelosLLM",
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
            agent_interface()
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
