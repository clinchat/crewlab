#!/bin/bash

# Cores ANSI
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # Sem cor

echo -e "${YELLOW}🚀 Iniciando a aplicação CrewLab com Streamlit...${NC}"

# Garante que o diretório atual esteja no PYTHONPATH
export PYTHONPATH=$(pwd)

# Inicia o Streamlit
streamlit run app.py

# Captura o status de saída
STATUS=$?

if [ $STATUS -eq 0 ]; then
  echo -e "${GREEN}✅ Streamlit finalizado sem erros.${NC}"
else
  echo -e "${RED}❌ Ocorreu um erro ao rodar o Streamlit.${NC}"
  echo -e "${RED}Código de erro: $STATUS${NC}"
fi
