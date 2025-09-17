#!/usr/bin/env python3
"""
Script de inicialização standalone para o Servidor MCP DOU.

Este script garante que o servidor seja executado com todas as 
dependências e configurações corretas, independente do diretório 
de trabalho atual.
"""

import os
import sys
import logging
from pathlib import Path

# Determina o diretório base do projeto
SCRIPT_DIR = Path(__file__).parent.absolute()
SERVER_DIR = SCRIPT_DIR
PYTHON_PATH = SERVER_DIR / "src"

# Configura logging para stderr (não interfere com JSON-RPC)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)

def main():
    """Inicia o servidor MCP DOU com configuração adequada."""
    
    # ✅ Usa logging em vez de print() para não corromper JSON-RPC
    logger.info("Iniciando Servidor MCP DOU...")
    logger.info(f"Diretorio do servidor: {SERVER_DIR}")
    logger.info(f"Python: {sys.executable}")
    logger.info("Servidor MCP DOU pronto para comunicacao JSON-RPC")
    
    # Configura o PYTHONPATH
    env = os.environ.copy()
    current_pythonpath = env.get('PYTHONPATH', '')
    if current_pythonpath:
        env['PYTHONPATH'] = f"{SERVER_DIR}{os.pathsep}{current_pythonpath}"
    else:
        env['PYTHONPATH'] = str(SERVER_DIR)
    
    # Muda para o diretório do servidor
    os.chdir(SERVER_DIR)
    
    try:
        # Importa e executa o servidor diretamente
        sys.path.insert(0, str(SERVER_DIR))
        from src.server import main as server_main
        
        # Executa o servidor
        server_main()
        
    except KeyboardInterrupt:
        logger.info("Servidor interrompido pelo usuario")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Erro ao iniciar servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()