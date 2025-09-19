#!/usr/bin/env python3
"""
Script de teste para as tools do MCP Server
"""

import asyncio
import sys
import os

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp_server import consultar_processo, consultar_temas, resumir_analisar

async def testar_tools():
    """Testa as tools do MCP Server com dados de exemplo"""

    print("=== TESTANDO MCP SERVER TOOLS ===\n")

    # Testar consultar_processo com dados do test-data.txt
    print("1. Testando consultar_processo...")
    try:
        resultado = await consultar_processo("1026220-43.2025.4.01.3600", "G1")
        print("✅ consultar_processo executado com sucesso")
        print(f"Resultado (primeiras 200 chars): {resultado[:200]}...\n")
    except Exception as e:
        print(f"❌ Erro em consultar_processo: {e}\n")

    # Testar consultar_temas
    print("2. Testando consultar_temas...")
    try:
        resultado = await consultar_temas("Bônus de Eficiência")
        print("✅ consultar_temas executado com sucesso")
        print(f"Resultado: {resultado[:300]}...\n")
    except Exception as e:
        print(f"❌ Erro em consultar_temas: {e}\n")

    # Testar resumir_analisar com dados simulados
    print("3. Testando resumir_analisar...")
    dados_simulados = """PROCESSO: 1026220-43.2025.4.01.3600 (Grau: G1)

=== ANDAMENTOS (5) ===
1. 15/01/2025 - Distribuição
2. 20/01/2025 - Juntada de petição
3. 25/01/2025 - Decisão interlocutória
4. 01/02/2025 - Audiência de conciliação
5. 10/02/2025 - Sentença"""

    try:
        resultado = await resumir_analisar(dados_simulados)
        print("✅ resumir_analisar executado com sucesso")
        print(f"Resultado: {resultado}\n")
    except Exception as e:
        print(f"❌ Erro em resumir_analisar: {e}\n")

    print("=== TESTES CONCLUÍDOS ===")

if __name__ == "__main__":
    asyncio.run(testar_tools())