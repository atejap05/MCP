"""
MCP Server para consultas judiciais - TRF1
Fornece ferramentas para consultar processos judiciais, temas e fazer análises.
"""

from typing import Any, Dict, List, Optional
import asyncio
import logging
from mcp.server.fastmcp import FastMCP

# Importar funcionalidades existentes do projeto
from app.application.services.trf1_scraper import TRF1Scraper
from app.core.config import LOGGER_NAME

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(LOGGER_NAME)

# Inicializar FastMCP server
mcp = FastMCP("mcp-jud")

# Instância do scraper
scraper = TRF1Scraper()


@mcp.tool()
async def consultar_processo(numero_processo: str, grau: str = "G1") -> str:
    """
    Consulta os andamentos de um processo judicial pelo seu número CNJ.

    Args:
        numero_processo: Número do processo no formato CNJ (ex: 1026220-43.2025.4.01.3600)
        grau: Grau do processo (G1 ou G2), padrão G1

    Returns:
        Lista de andamentos do processo
    """
    try:
        logger.info(f"Consultando processo: {numero_processo}, grau: {grau}")

        # Usar o scraper para obter andamentos do processo
        andamentos = await scraper.get_all_events(numero_processo, grau)

        if not andamentos:
            return f"Nenhum andamento encontrado para o processo {numero_processo} no grau {grau}."

        # Formatar os dados de forma legível
        resultado = f"PROCESSO: {numero_processo} (Grau: {grau})\n\n"
        resultado += f"=== ANDAMENTOS ({len(andamentos)}) ===\n"

        for i, andamento in enumerate(andamentos, 1):
            resultado += f"{i}. {andamento}\n"

        return resultado

    except Exception as e:
        logger.error(f"Erro ao consultar processo {numero_processo}: {str(e)}")
        return f"Erro ao consultar processo: {str(e)}"


@mcp.tool()
async def consultar_temas(filtro: str) -> str:
    """
    Busca processos judiciais por temas, assuntos ou palavras-chave.

    Nota: Esta funcionalidade requer integração com API DataJud ou base de dados
    indexada para busca eficiente. Atualmente retorna orientações sobre implementação.

    Args:
        filtro: Palavra-chave ou tema para buscar (ex: "Bônus de Eficiência")

    Returns:
        Orientação sobre como implementar busca por temas
    """
    try:
        logger.info(f"Solicitação de consulta por tema: {filtro}")

        return f"""CONSULTA POR TEMAS - IMPLEMENTAÇÃO NECESSÁRIA

Tema solicitado: "{filtro}"

Esta funcionalidade requer integração com a API DataJud do CNJ para busca eficiente por temas/assuntos.

Para implementar:
1. Obter chave da API DataJud (https://datajud-wiki.cnj.jus.br/api-publica/)
2. Usar endpoints de busca da API com filtros por assunto/classe
3. Indexar resultados para busca rápida

Atualmente, o sistema trabalha com scraping direto dos tribunais, que não suporta busca por temas.

Para testes, use a tool 'consultar_processo' com números específicos de processo."""

    except Exception as e:
        logger.error(f"Erro na consulta de temas: {str(e)}")
        return f"Erro ao processar consulta de temas: {str(e)}"


@mcp.tool()
async def resumir_analisar(dados_processo: str) -> str:
    """
    Faz resumo e análise dos dados de um processo judicial.

    Args:
        dados_processo: Dados do processo (geralmente saída da tool consultar_processo)

    Returns:
        Análise e resumo dos dados do processo
    """
    try:
        logger.info("Fazendo resumo e análise dos dados do processo")

        if not dados_processo or not dados_processo.strip():
            return "Dados do processo vazios ou inválidos para análise."

        # Análise básica dos dados
        linhas = [linha.strip() for linha in dados_processo.split('\n') if linha.strip()]

        # Extrair andamentos
        andamentos = []
        for linha in linhas:
            if linha.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')) and ' - ' in linha:
                # Remove o número e extrai data e título
                partes = linha.split(' - ', 1)
                if len(partes) == 2:
                    andamentos.append({
                        'data': partes[0].split('. ', 1)[1] if '. ' in partes[0] else partes[0],
                        'titulo': partes[1]
                    })

        # Gerar análise
        analise = "ANÁLISE DO PROCESSO\n\n"

        if andamentos:
            analise += f"Número total de andamentos identificados: {len(andamentos)}\n\n"

            # Análise temporal
            analise += "ANÁLISE TEMPORAL:\n"
            analise += f"- Primeiro andamento: {andamentos[-1]['data']}\n"
            analise += f"- Último andamento: {andamentos[0]['data']}\n\n"

            # Análise de tipos de andamento
            from collections import Counter
            titulos = [a['titulo'] for a in andamentos]
            tipos_comuns = Counter(titulos).most_common(5)

            analise += "TIPOS DE ANDAMENTO MAIS FREQUENTES:\n"
            for titulo, count in tipos_comuns:
                analise += f"- {titulo}: {count} ocorrências\n"

            # Identificar padrões
            analise += "\nPADRÕES IDENTIFICADOS:\n"
            if len(andamentos) > 10:
                analise += "- Processo com alta atividade (mais de 10 andamentos)\n"
            elif len(andamentos) < 3:
                analise += "- Processo recente ou com baixa atividade\n"

            # Verificar se há decisões
            decisoes = [a for a in andamentos if any(palavra in a['titulo'].lower() for palavra in ['decisão', 'sentença', 'julgamento', 'acórdão'])]
            if decisoes:
                analise += f"- Identificadas {len(decisoes)} possíveis decisões/julgamentos\n"

        else:
            analise += "Não foi possível identificar andamentos estruturados nos dados fornecidos.\n"
            analise += "Verifique se os dados foram gerados pela tool 'consultar_processo'.\n"

        return analise

    except Exception as e:
        logger.error(f"Erro ao fazer análise: {str(e)}")
        return f"Erro ao fazer análise dos dados: {str(e)}"


if __name__ == "__main__":
    # Inicializar e executar o servidor MCP
    logger.info("Iniciando MCP Server para consultas judiciais")
    mcp.run(transport='stdio')