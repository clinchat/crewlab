import streamlit as st
import json
from logs.log_manager import list_logs, read_log

def log_interface():
    st.header("📑 Histórico de Logs do CrewLab")

    logs = list_logs()

    if not logs:
        st.info("Nenhum log encontrado até o momento.")
        return

    log_selecionado = st.selectbox("Selecione um log para visualizar", logs)

    if log_selecionado:
        conteudo = read_log(log_selecionado)
        st.subheader(f"📄 Conteúdo do log: `{log_selecionado}`")
        st.code(json.dumps(conteudo, indent=2, ensure_ascii=False), language="json")

        st.download_button(
            label="⬇️ Baixar log como JSON",
            data=json.dumps(conteudo, indent=2, ensure_ascii=False),
            file_name=log_selecionado,
            mime="application/json"
        )
