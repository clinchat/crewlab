import json
from llms.llm_manager import list_llm_models

def gerar_mapeamento_llms_por_config():
    """
    Gera um dicionário onde a chave é o config_json (como string JSON ordenada)
    e o valor é o nome do modelo LLM correspondente.
    """
    llms = list_llm_models()
    mapeamento = {}
    for llm in llms:
        config_str = json.dumps(llm.config_json, sort_keys=True)
        mapeamento[config_str] = llm.name
    return mapeamento


def obter_config_por_nome(nome_modelo: str):
    """
    Retorna o config_json de um modelo LLM cadastrado com base no nome informado.
    """
    llms = list_llm_models()
    for llm in llms:
        if llm.name == nome_modelo:
            return llm.config_json
    return None
