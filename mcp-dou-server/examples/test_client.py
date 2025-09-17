"""
Cliente de exemplo para testar o servidor MCP DOU.

Este script demonstra como interagir com as ferramentas
do servidor MCP DOU programaticamente.
"""

import asyncio
import json
from datetime import date, timedelta


async def test_dou_server():
    """
    Testa as principais funcionalidades do servidor DOU.
    """
    print("🧪 Teste do Servidor MCP DOU")
    print("=" * 50)
    
    # Simula comandos que seriam enviados pelo cliente MCP
    test_commands = [
        {
            "name": "test_connection",
            "description": "Testa conexão com INLABS",
            "args": {}
        },
        {
            "name": "list_available_sections", 
            "description": "Lista seções do DOU",
            "args": {}
        },
        {
            "name": "get_server_info",
            "description": "Informações do servidor",
            "args": {}
        },
        {
            "name": "check_file_availability",
            "description": "Verifica arquivos de hoje",
            "args": {
                "date_str": date.today().strftime("%Y-%m-%d"),
                "sections": "DO1 DO2",
                "file_format": "xml"
            }
        },
        {
            "name": "validate_date_range",
            "description": "Valida intervalo de datas",
            "args": {
                "start_date": (date.today() - timedelta(days=7)).strftime("%Y-%m-%d"),
                "end_date": date.today().strftime("%Y-%m-%d")
            }
        }
    ]
    
    print("📋 Comandos de teste preparados:")
    for i, cmd in enumerate(test_commands, 1):
        print(f"{i}. {cmd['description']}")
    
    print(f"\n💡 Para testar o servidor real:")
    print(f"1. Configure suas credenciais INLABS no arquivo .env")
    print(f"2. Execute: python -m src.server")
    print(f"3. Configure Claude Desktop para usar este servidor")
    print(f"4. Teste com comandos como:")
    print(f'   • "Liste as seções disponíveis do DOU"')
    print(f'   • "Baixe os XMLs do DOU de hoje"')
    print(f'   • "Verifique se há arquivos disponíveis para ontem"')
    
    print(f"\n🔧 Configuração do Claude Desktop:")
    config_example = {
        "mcpServers": {
            "dou": {
                "command": "python",
                "args": ["-m", "src.server"],
                "cwd": "/caminho/para/mcp-dou-server"
            }
        }
    }
    
    print(f"Adicione ao claude_desktop_config.json:")
    print(json.dumps(config_example, indent=2))


if __name__ == "__main__":
    asyncio.run(test_dou_server())