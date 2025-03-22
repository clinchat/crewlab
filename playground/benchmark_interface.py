import streamlit as st
import json
from common.services.benchmark_manager import list_benchmarks, load_benchmark

def benchmark_interface():
    st.header("📊 Benchmarks salvos")

    arquivos = list_benchmarks()

    if not arquivos:
        st.info("Nenhum benchmark encontrado.")
        return

    selecionado = st.selectbox("Selecione um benchmark", arquivos)

    if selecionado:
        dados = load_benchmark(selecionado)
        st.markdown(f"**🆔 ID:** {dados['id']}")
        st.markdown(f"**📅 Data/hora:** {dados['timestamp']}")
        st.markdown(f"**📝 Prompt:** `{dados['prompt']}`")

        for r in dados["resultados"]:
            st.markdown(f"### 🤖 {r['agent_name']} (`{r['model']}`)")
            st.code(r["resposta"])
            st.markdown("---")

        st.download_button(
            "⬇️ Baixar este benchmark",
            data=json.dumps(dados, indent=2, ensure_ascii=False),
            file_name=f"{dados['id']}.json",
            mime="application/json"
        )
