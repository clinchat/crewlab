#!/bin/bash

# Cores ANSI
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # Sem cor

echo -e "${YELLOW}📊 Iniciando o modo BENCHMARK do CrewLab...${NC}"

# Define a raiz como PYTHONPATH
export PYTHONPATH=$(pwd)

# Inicia o Streamlit diretamente na tela de benchmark
streamlit run app.py -- --benchmark

STATUS=$?

if [ $STATUS -eq 0 ]; then
  echo -e "${GREEN}✅ Benchmark executado e encerrado com sucesso.${NC}"
else
  echo -e "${RED}❌ Erro ao executar benchmark. Código: $STATUS${NC}"
fi
