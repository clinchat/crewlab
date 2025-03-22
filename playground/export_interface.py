import streamlit as st
import json
from agents.agent_manager import list_agents, create_agent
from tasks.task_manager import list_tasks, create_task
from logs.log_manager import write_log, list_logs, read_log


def export_import_interface():
    st.header("📁 Importação e Exportação de Dados")

    agentes = list_agents()
    tarefas = list_tasks()

    agentes_json = [
        {
            "id": a.id,
            "agent_id": a.agent_id,
            "name": a.name,
            "role": a.role,
            "goal": a.goal,
            "backstory": a.backstory,
            "tools": a.tools,
            "llm_config": a.llm_config
        }
        for a in agentes
    ]

    tarefas_json = [
        {
            "id": t.id,
            "name": t.name,
            "description": t.description,
            "expected_output": t.expected_output,
            "agent_id": t.agent_id,
            "dependencies": t.dependencies
        }
        for t in tarefas
    ]

    st.subheader("📤 Exportar Dados")

    if st.download_button(
        label="⬇️ Exportar apenas Agentes",
        data=json.dumps(agentes_json, indent=2, ensure_ascii=False),
        file_name="agentes.json",
        mime="application/json"
    ):
        write_log("export_agents", {"total": len(agentes_json)})

    if st.download_button(
        label="⬇️ Exportar apenas Tarefas",
        data=json.dumps(tarefas_json, indent=2, ensure_ascii=False),
        file_name="tarefas.json",
        mime="application/json"
    ):
        write_log("export_tasks", {"total": len(tarefas_json)})

    export_data = {
        "agents": agentes_json,
        "tasks": tarefas_json
    }

    if st.download_button(
        label="⬇️ Exportar tudo em JSON",
        data=json.dumps(export_data, indent=2, ensure_ascii=False),
        file_name="crewlab_export.json",
        mime="application/json"
    ):
        write_log("export_all", {"agents": len(agentes_json), "tasks": len(tarefas_json)})

    st.markdown("---")
    st.subheader("📂 Importar Dados")

    uploaded_file = st.file_uploader("Escolha um arquivo JSON exportado anteriormente", type=["json"])
    confirmar_importacao = st.checkbox("⚠️ Confirmo que desejo importar os dados e sobrescrever existentes se necessário")

    if uploaded_file is not None and confirmar_importacao:
        try:
            import_data = json.load(uploaded_file)

            imported_agents = import_data.get("agents", [])
            imported_tasks = import_data.get("tasks", [])

            agentes_existentes_ids = {a.agent_id for a in list_agents()}
            tarefas_existentes_nomes = {t.name for t in list_tasks()}

            count_agents = 0
            count_tasks = 0

            for agent in imported_agents:
                if agent.get("agent_id") in agentes_existentes_ids:
                    st.warning(f"Agente duplicado ignorado: {agent.get('agent_id')}")
                    continue
                try:
                    create_agent(agent)
                    count_agents += 1
                except Exception as e:
                    st.warning(f"Erro ao importar agente '{agent.get('agent_id')}': {e}")

            for task in imported_tasks:
                if task.get("name") in tarefas_existentes_nomes:
                    st.warning(f"Tarefa duplicada ignorada: {task.get('name')}")
                    continue
                try:
                    create_task(task)
                    count_tasks += 1
                except Exception as e:
                    st.warning(f"Erro ao importar tarefa '{task.get('name')}': {e}")

            write_log("import_data", {
                "imported_agents": count_agents,
                "imported_tasks": count_tasks,
                "ignored_agents": len(imported_agents) - count_agents,
                "ignored_tasks": len(imported_tasks) - count_tasks
            })

            st.success("Importação concluída com sucesso!")

        except json.JSONDecodeError:
            st.error("❌ Arquivo JSON inválido.")
        except Exception as e:
            st.error(f"❌ Erro ao importar dados: {e}")
    elif uploaded_file is not None and not confirmar_importacao:
        st.info("☝️ Marque a caixa de confirmação para importar os dados.")

    st.markdown("---")
    st.subheader("📑 Histórico de Logs")

    logs = list_logs()
    if logs:
        log_selecionado = st.selectbox("Selecione um log para visualizar", logs)
        conteudo = read_log(log_selecionado)
        st.code(json.dumps(conteudo, indent=2, ensure_ascii=False), language="json")
    else:
        st.info("Nenhum log encontrado.")
