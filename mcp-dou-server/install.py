#!/usr/bin/env python3
"""
Script de instalação e configuração do MCP DOU Server.

Este script automatiza a instalação das dependências e configuração inicial.
"""

import os
import sys
import subprocess
from pathlib import Path
import shutil


def check_python_version():
    """Verifica se a versão do Python é adequada."""
    if sys.version_info < (3, 10):
        print("❌ Python 3.10 ou superior é necessário")
        print(f"   Versão atual: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")
    return True


def install_dependencies():
    """Instala as dependências do projeto."""
    print("📦 Instalando dependências...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências")
        return False


def setup_environment():
    """Configura o ambiente (cria .env baseado no exemplo)."""
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if env_file.exists():
        print("⚠️  Arquivo .env já existe")
        response = input("   Deseja sobrescrever? (s/N): ")
        if response.lower() != 's':
            print("   Mantendo arquivo .env existente")
            return True
    
    if env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ Arquivo .env criado baseado no exemplo")
        print("⚠️  IMPORTANTE: Configure suas credenciais INLABS no arquivo .env")
        return True
    else:
        print("❌ Arquivo .env.example não encontrado")
        return False


def create_directories():
    """Cria diretórios necessários."""
    directories = ["cache", "logs", "downloads"]
    
    for dir_name in directories:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Diretório '{dir_name}' criado")
    
    print("✅ Diretórios criados")
    return True


def test_installation():
    """Testa se a instalação foi bem-sucedida."""
    print("🧪 Testando instalação...")
    
    try:
        # Tenta importar os módulos principais
        from src.config.settings import get_config
        from src.models.dou_models import DOUSection
        from src.auth.inlabs_auth import INLABSAuth
        
        print("✅ Módulos importados com sucesso")
        
        # Testa configuração
        config = get_config()
        print(f"✅ Configuração carregada - Servidor: {config.server_name}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False


def show_next_steps():
    """Mostra os próximos passos após a instalação."""
    print("\n" + "="*60)
    print("🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
    print("="*60)
    print("\n📋 PRÓXIMOS PASSOS:\n")
    
    print("1. 🔐 Configure suas credenciais INLABS:")
    print("   • Edite o arquivo .env")
    print("   • Insira seu email e senha do sistema INLABS\n")
    
    print("2. 🧪 Teste o servidor:")
    print("   • python run_server.py")
    print("   • ou: python -m src.server\n")
    
    print("3. 🤖 Configure Claude Desktop:")
    print("   • Localize: claude_desktop_config.json")
    print("   • Adicione a configuração do servidor DOU")
    print("   • Veja exemplos/ para configuração completa\n")
    
    print("4. ✨ Teste com Claude:")
    print('   • "Liste as seções do DOU"')
    print('   • "Baixe os XMLs do DOU de hoje"')
    print('   • "Teste a conexão com INLABS"\n')
    
    print("📚 Documentação: README.md")
    print("🐛 Issues: https://github.com/atejap05/mcp-dou-server/issues")
    print("\n" + "="*60)


def main():
    """Função principal do instalador."""
    print("🚀 MCP DOU Server - Instalador")
    print("="*50)
    
    # Verifica Python
    if not check_python_version():
        sys.exit(1)
    
    # Instala dependências
    if not install_dependencies():
        sys.exit(1)
    
    # Configura ambiente
    if not setup_environment():
        sys.exit(1)
    
    # Cria diretórios
    if not create_directories():
        sys.exit(1)
    
    # Testa instalação
    if not test_installation():
        print("⚠️  Instalação pode ter problemas, mas prosseguindo...")
    
    # Mostra próximos passos
    show_next_steps()


if __name__ == "__main__":
    main()