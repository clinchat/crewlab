#!/bin/bash

# Cores ANSI
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # Sem cor

echo -e "${YELLOW}🐞 Iniciando CrewLab em modo DEBUG (log detalhado)...${NC}"

# Garante que o diretório atual esteja no PYTHONPATH
export PYTHONPATH=$(pwd)

# Inicia o Streamlit com log detalhado
streamlit run app.py --logger.level=debug

STATUS=$?

if [ $STATUS -eq 0 ]; then
  echo -e "${GREEN}✅ Streamlit encerrado com sucesso.${NC}"
else
  echo -e "${RED}❌ Erro durante execução com debug. Código: $STATUS${NC}"
fi
