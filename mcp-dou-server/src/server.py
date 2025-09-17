"""
Servidor MCP (Model Context Protocol) para Diário Oficial da União.

Este servidor permite que assistentes de IA como Claude consultem,
baixem e analisem publicações do DOU de forma natural e eficiente.
"""

import asyncio
import logging
import sys
from typing import Any, Dict

from mcp.server.fastmcp import FastMCP

from .config.settings import get_config
from .tools.download import register_download_tools
from .tools.search import register_search_tools
from .tools.parser import register_parser_tools
from .tools.utils import register_utility_tools


def setup_logging(config) -> None:
    """Configura o sistema de logging do servidor."""
    
    # Configuração básica do logging
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    if config.log_file:
        logging.basicConfig(
            level=getattr(logging, config.log_level.upper()),
            format=log_format,
            handlers=[
                logging.FileHandler(config.log_file),
                logging.StreamHandler(sys.stderr)  # Para servidores STDIO
            ]
        )
    else:
        logging.basicConfig(
            level=getattr(logging, config.log_level.upper()),
            format=log_format,
            handlers=[logging.StreamHandler(sys.stderr)]
        )
    
    # Configura loggers específicos
    logger = logging.getLogger(__name__)
    logger.info(f"Servidor MCP DOU iniciado - Versão {config.server_version}")


def create_server() -> FastMCP:
    """
    Cria e configura o servidor MCP DOU.
    
    Returns:
        FastMCP: Instância do servidor MCP configurada
    """
    config = get_config()
    
    # Configura logging
    setup_logging(config)
    
    # Cria instância do servidor
    mcp = FastMCP(config.server_name)
    
    # Registra todas as ferramentas
    register_download_tools(mcp)
    register_search_tools(mcp)
    register_parser_tools(mcp)
    register_utility_tools(mcp)
    
    logger = logging.getLogger(__name__)
    logger.info(f"Servidor '{config.server_name}' criado com sucesso")
    
    return mcp


def main() -> None:
    """Função principal do servidor."""
    try:
        server = create_server()
        
        # Executa o servidor usando STDIO (padrão para MCP)
        server.run(transport='stdio')
        
    except KeyboardInterrupt:
        logger = logging.getLogger(__name__)
        logger.info("Servidor interrompido pelo usuário")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Erro fatal no servidor: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()