import streamlit as st
import json
from tasks.task_manager import create_task, list_tasks, delete_task
from agents.agent_manager import list_agents

def task_interface():
    st.header("📋 Gerenciamento de Tarefas")

    aba = st.radio("Escolha uma ação:", ["➕ Cadastrar nova tarefa", "📂 Ver tarefas existentes"])

    if aba == "➕ Cadastrar nova tarefa":
        agentes = list_agents()

        if not agentes:
            st.warning("⚠️ Cadastre pelo menos um agente antes de criar tarefas.")
            return

        with st.form("form_cadastro_tarefa"):
            name = st.text_input("📌 Nome da tarefa", placeholder="Ex: Resumir artigo científico")
            description = st.text_area("📝 Descrição da tarefa", placeholder="Descreva o que a tarefa precisa fazer...")
            expected_output = st.text_area("🎯 Resultado Esperado (opcional)", placeholder="Ex: Resposta clara e objetiva")

            agente_vinculado = st.selectbox(
                "🤖 Agente responsável",
                agentes,
                format_func=lambda a: f"{a.name} ({a.agent_id})"
            )

            dependencies = st.text_area("🔗 Dependências (opcional)", value="[]", help="Informe nomes de tarefas anteriores ou IDs. Ex: ['tarefa1', 'tarefa2']")

            submitted = st.form_submit_button("✅ Salvar tarefa")

            if submitted:
                if not name.strip() or not description.strip():
                    st.error("❌ Nome e descrição são obrigatórios.")
                    return

                try:
                    deps_json = json.loads(dependencies)
                    if not isinstance(deps_json, list):
                        raise ValueError("Dependências devem estar em formato de lista.")

                    task_data = {
                        "name": name.strip(),
                        "description": description.strip(),
                        "expected_output": expected_output.strip() or None,
                        "agent_id": agente_vinculado.agent_id,
                        "dependencies": deps_json
                    }

                    create_task(task_data)
                    st.success(f"✅ Tarefa '{name}' cadastrada com sucesso!")
                    st.rerun()

                except json.JSONDecodeError:
                    st.error("❌ Erro de formatação: dependências devem estar em formato JSON válido.")
                except Exception as e:
                    st.error(f"Erro ao salvar tarefa: {e}")

    elif aba == "📂 Ver tarefas existentes":
        tarefas = list_tasks()

        if not tarefas:
            st.info("ℹ️ Nenhuma tarefa cadastrada.")
        else:
            for tarefa in tarefas:
                with st.expander(f"📌 {tarefa.name}"):
                    st.markdown(f"**📝 Descrição:** {tarefa.description}")
                    st.markdown(f"**🎯 Resultado Esperado:** {tarefa.expected_output or 'N/A'}")
                    st.markdown(f"**🤖 Agente Vinculado:** `{tarefa.agent_id}`")

                    deps = tarefa.dependencies or []
                    deps_str = ", ".join(deps) if isinstance(deps, list) else str(deps)
                    st.markdown(f"**🔗 Dependências:** {deps_str or 'Nenhuma'}")

                    if st.button(f"🗑️ Excluir '{tarefa.name}'", key=f"del_task_{tarefa.id}"):
                        delete_task(tarefa.id)
                        st.success(f"Tarefa '{tarefa.name}' excluída com sucesso!")
                        st.rerun()
