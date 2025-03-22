import streamlit as st
from crewai import Agent, Crew, Task as CrewTask
from agents.agent_manager import list_agents, create_agent
from tasks.task_manager import list_tasks, create_task
import json

def run_agent_chat(agent_data, task_data, user_input):
    try:
        llm_data = agent_data.llm_config or {}
        provider = llm_data.get('provider')
        model_config = llm_data.get('config', {})

        if not provider or 'model' not in model_config:
            raise ValueError("Configuração LLM inválida. Verifique se 'provider' e 'model' estão definidos.")

        llm_config_final = {
            "provider": provider,
            **model_config
        }

        agent = Agent(
            role=agent_data.role,
            goal=agent_data.goal,
            backstory=agent_data.backstory,
            verbose=True,
            allow_delegation=agent_data.allow_delegation,
            memory=agent_data.memory,
            tools=agent_data.tools,
            llm=llm_config_final
        )

        task = CrewTask(
            description=user_input or task_data.description,
            expected_output=task_data.expected_output or "Uma resposta adequada ao usuário.",
            agent=agent
        )

        crew = Crew(agents=[agent], tasks=[task], verbose=True)
        result = crew.kickoff()
        return result

    except Exception as e:
        raise RuntimeError(f"Erro durante execução do agente: {str(e)}")

def chat_playground_interface():
    st.header("🎮 Playground interativo com Agentes e Tarefas")

    st.sidebar.markdown("---")
    modo_debug = st.sidebar.checkbox("🔍 Modo Debug: visualizar dados brutos")

    if modo_debug:
        st.subheader("📊 Dados brutos dos Agentes e Tarefas")

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

        st.markdown("### 🤖 Agentes")
        for a in agentes_json:
            st.code(json.dumps(a, indent=2, ensure_ascii=False), language="json")

        st.download_button(
            label="⬇️ Exportar apenas Agentes",
            data=json.dumps(agentes_json, indent=2, ensure_ascii=False),
            file_name="agentes.json",
            mime="application/json"
        )

        st.markdown("### 📋 Tarefas")
        for t in tarefas_json:
            st.code(json.dumps(t, indent=2, ensure_ascii=False), language="json")

        st.download_button(
            label="⬇️ Exportar apenas Tarefas",
            data=json.dumps(tarefas_json, indent=2, ensure_ascii=False),
            file_name="tarefas.json",
            mime="application/json"
        )

        export_data = {
            "agents": agentes_json,
            "tasks": tarefas_json
        }

        export_json = json.dumps(export_data, indent=2, ensure_ascii=False)
        st.download_button(
            label="⬇️ Exportar tudo em JSON",
            data=export_json,
            file_name="crewlab_export.json",
            mime="application/json"
        )

        st.markdown("---")
        st.subheader("📂 Importar agentes e tarefas de arquivo JSON")

        uploaded_file = st.file_uploader("Escolha um arquivo JSON exportado anteriormente", type=["json"])
        confirmar_importacao = st.checkbox("⚠️ Confirmo que desejo importar os dados e sobrescrever existentes se necessário")

        if uploaded_file is not None and confirmar_importacao:
            try:
                import_data = json.load(uploaded_file)

                imported_agents = import_data.get("agents", [])
                imported_tasks = import_data.get("tasks", [])

                agentes_existentes_ids = {a.agent_id for a in list_agents()}
                tarefas_existentes_nomes = {t.name for t in list_tasks()}

                for agent in imported_agents:
                    if agent.get("agent_id") in agentes_existentes_ids:
                        st.warning(f"Agente duplicado ignorado: {agent.get('agent_id')}")
                        continue
                    try:
                        create_agent(agent)
                    except Exception as e:
                        st.warning(f"Erro ao importar agente '{agent.get('agent_id')}': {e}")

                for task in imported_tasks:
                    if task.get("name") in tarefas_existentes_nomes:
                        st.warning(f"Tarefa duplicada ignorada: {task.get('name')}")
                        continue
                    try:
                        create_task(task)
                    except Exception as e:
                        st.warning(f"Erro ao importar tarefa '{task.get('name')}': {e}")

                st.success("Importação concluída com sucesso!")

            except json.JSONDecodeError:
                st.error("❌ Arquivo JSON inválido.")
            except Exception as e:
                st.error(f"❌ Erro ao importar dados: {e}")
        elif uploaded_file is not None and not confirmar_importacao:
            st.info("☝️ Marque a caixa de confirmação para importar os dados.")
        return

    # === PLAYGROUND DE COMPARAÇÃO DE AGENTES ===

    agentes = list_agents()
    tarefas = list_tasks()

    if not agentes or not tarefas:
        st.warning("Cadastre ao menos um agente e uma tarefa para usar o playground.")
        return

    agentes_selecionados = st.multiselect(
        "Selecione um ou mais agentes para comparar:",
        options=agentes,
        format_func=lambda a: f"{a.name} ({a.agent_id})"
    )

    if not agentes_selecionados:
        st.info("Selecione ao menos um agente para continuar.")
        return

    tarefas_do_agente = [
        t for t in tarefas if t.agent_id == agentes_selecionados[0].id
    ]

    if not tarefas_do_agente:
        st.info("Nenhuma tarefa vinculada ao primeiro agente selecionado.")
        return

    tarefa_selecionada = st.selectbox(
        "Selecione a tarefa base:",
        options=tarefas_do_agente,
        format_func=lambda t: f"{t.name} - {t.description[:40]}..."
    )

    prompt = st.text_area("💬 Prompt / Mensagem a ser enviada para todos os agentes")

    if st.button("🔍 Comparar Respostas"):
        if not prompt.strip():
            st.warning("Digite uma mensagem para enviar.")
        else:
            resultados = []
            for agente in agentes_selecionados:
                try:
                    with st.spinner(f"Executando com {agente.name}..."):
                        resposta = run_agent_chat(agente, tarefa_selecionada, prompt)
                        modelo = agente.llm_config.get("config", {}).get("model", "modelo indefinido")
                        resultados.append({
                            "agent_id": agente.agent_id,
                            "agent_name": agente.name,
                            "model": modelo,
                            "resposta": resposta
                        })
                        st.markdown(f"### 🤖 {agente.name} (`{modelo}`)")
                        st.code(resposta)
                        st.markdown("---")
                except Exception as e:
                    st.error(f"Erro com {agente.name}: {e}")

            if resultados:
                st.session_state.benchmark_resultados = resultados
                st.session_state.benchmark_prompt = prompt
                st.success("Comparação concluída! Você pode salvar como benchmark abaixo.")

    if "benchmark_resultados" in st.session_state and st.session_state.benchmark_resultados:
        if st.button("💾 Salvar como Benchmark"):
            from benchmark_manager import save_benchmark
            benchmark_id = save_benchmark(
                prompt=st.session_state.benchmark_prompt,
                resultados=st.session_state.benchmark_resultados
            )
            st.success(f"Benchmark salvo com ID: {benchmark_id}")

