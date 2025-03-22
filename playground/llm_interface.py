import streamlit as st
import json
import litellm
from llms.llm_manager import (
    create_llm_model,
    list_llm_models,
    delete_llm_model
)


def testar_conexao_llm(modelo):
    """Testa a conexão com o modelo LLM via LiteLLM."""
    try:
        config = modelo.config_json.copy()
        model_name = config.pop("model", None)
        api_key = config.pop("api_key", None)
        # ❗️ NÃO envie 'provider' para litellm, ele detecta automaticamente
        config.pop("provider", None)

        if not model_name:
            return False, "Configuração inválida: 'model' ausente."

        response = litellm.completion(
            model=model_name,
            messages=[{"role": "user", "content": "Olá, tudo bem?"}],
            api_key=api_key,
            **config
        )

        content = response['choices'][0]['message']['content']
        return True, content.strip()

    except Exception as e:
        error_msg = str(e)
        if "default credentials" in error_msg.lower() or "GOOGLE_APPLICATION_CREDENTIALS" in error_msg:
            return False, (
                "❌ Este modelo requer credenciais do Google configuradas.\n\n"
                "💡 Solução: defina a variável de ambiente `GOOGLE_APPLICATION_CREDENTIALS` com o caminho para seu arquivo .json de serviço, "
                "ou use a API Key com `provider: 'google'` se estiver usando Gemini via API pública."
            )
        return False, error_msg


def get_default_config(provider):
    """Retorna configuração padrão para o provedor informado."""
    if provider == "openai":
        return {
            "model": "gpt-4",
            "temperature": 0.7
        }
    elif provider == "google":
        return {
            "model": "gemini-pro",
            "temperature": 0.7
        }
    elif provider == "deepseek":
        return {
            "model": "deepseek-chat",
            "temperature": 0.7
        }
    elif provider == "ollama":
        return {
            "model": "llama3",
            "base_url": "http://localhost:11434",
            "temperature": 0.7
        }
    return {}


def rerun():
    """Compatibilidade com versões antigas e novas do Streamlit."""
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()


def llm_interface():
    st.header("🧠 Modelos LLM Cadastrados")

    aba = st.radio("Escolha uma ação:", ["Cadastrar novo modelo", "Ver modelos existentes"])

    if aba == "Cadastrar novo modelo":
        with st.form("form_modelo_llm"):
            name = st.text_input("Nome do modelo", placeholder="Ex: GPT-4 Turbo")
            provider = st.text_input("Provedor", placeholder="Ex: openai, ollama, google").lower()

            default_config = get_default_config(provider)
            config_str = json.dumps(default_config, indent=2) if default_config else "{}"

            config_text = st.text_area("Configuração JSON (sem api_key)", value=config_str, height=200)

            api_key = st.text_input("🔑 API Key", type="password", help="Este campo será incluído automaticamente na configuração.")
            description = st.text_input("Descrição (opcional)")

            submitted = st.form_submit_button("Salvar modelo")

            if submitted:
                if not name.strip() or not provider.strip():
                    st.warning("Por favor, preencha o nome e o provedor.")
                    return

                try:
                    config_json = json.loads(config_text)

                    provedores_que_exigem_chave = {"openai", "google", "deepseek"}

                    if provider in provedores_que_exigem_chave and not api_key:
                        st.error(f"⚠️ O provedor '{provider}' requer uma API Key para funcionar corretamente.")
                        return

                    if provider in {"vertex_ai", "vertex_gemini"} and not api_key:
                        st.warning(
                            "⚠️ Nenhuma API Key informada. Este provedor requer autenticação via variável "
                            "`GOOGLE_APPLICATION_CREDENTIALS`. Se não for configurada, o modelo não funcionará."
                        )

                    # 🔐 Adiciona api_key ao config_json, mas não o provider
                    if api_key:
                        config_json["api_key"] = api_key

                    # provider vai para o banco, mas não é enviado para LiteLLM
                    data = {
                        "name": name,
                        "provider": provider,
                        "config_json": config_json,
                        "description": description
                    }
                    create_llm_model(data)
                    st.success(f"Modelo '{name}' salvo com sucesso!")
                    rerun()

                except json.JSONDecodeError:
                    st.error("❌ JSON inválido. Verifique o campo de configuração.")
                except Exception as e:
                    st.error(f"Erro ao salvar modelo: {e}")

    elif aba == "Ver modelos existentes":
        modelos = list_llm_models()

        if not modelos:
            st.info("Nenhum modelo cadastrado ainda.")
        else:
            for modelo in modelos:
                with st.expander(f"🧠 {modelo.name} ({modelo.provider})"):
                    st.markdown(f"**Descrição:** {modelo.description or 'N/A'}")
                    st.code(json.dumps(modelo.config_json, indent=2, ensure_ascii=False), language="json")

                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button(f"❌ Excluir {modelo.name}", key=f"del_{modelo.id}"):
                            delete_llm_model(modelo.id)
                            st.success(f"Modelo '{modelo.name}' excluído.")
                            rerun()

                    with col2:
                        if st.button(f"🔌 Testar Conexão", key=f"test_{modelo.id}"):
                            with st.spinner("Testando modelo..."):
                                sucesso, resultado = testar_conexao_llm(modelo)
                                if sucesso:
                                    st.success(f"✅ Resposta recebida: {resultado}")
                                else:
                                    st.error(f"{resultado}")
