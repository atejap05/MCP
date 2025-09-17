#!/usr/bin/env python3
"""
Script de inicialização do servidor MCP DOU.

Este script pode ser usado para testar e iniciar o servidor
diretamente sem configuração adicional.
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

try:
    from src.server import main
    
    if __name__ == "__main__":
        print("🚀 Iniciando Servidor MCP DOU...")
        print("📋 Para parar o servidor, use Ctrl+C")
        print("=" * 50)
        main()
        
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("💡 Certifique-se de instalar as dependências:")
    print("   pip install -r requirements.txt")
    sys.exit(1)
except KeyboardInterrupt:
    print("\n👋 Servidor interrompido pelo usuário")
    sys.exit(0)
except Exception as e:
    print(f"❌ Erro fatal: {e}")
    sys.exit(1)