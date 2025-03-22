#!/bin/bash

# Cores ANSI
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # Sem cor

echo -e "${YELLOW}🔧 Inicializando o sistema CrewLab...${NC}"

# Define PYTHONPATH corretamente para o projeto
export PYTHONPATH=$(pwd)

# Executa o script
python init_tables.py

# Captura código de saída
STATUS=$?

if [ $STATUS -eq 0 ]; then
  echo -e "${GREEN}✅ Inicialização concluída com sucesso.${NC}"
else
  echo -e "${RED}❌ Ocorreu um erro durante a inicialização.${NC}"
  echo -e "${RED}Código de erro: $STATUS${NC}"
fi

