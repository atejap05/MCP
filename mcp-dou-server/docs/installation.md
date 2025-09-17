# Guia de Instalação - MCP DOU Server

## 📋 Pré-requisitos

### Python 3.10+

Este projeto requer Python 3.10 ou superior. Para verificar sua versão:

```bash
python --version
```

Se você tem uma versão mais antiga, instale uma versão mais recente:

#### Windows

- Baixe Python 3.11+ de [python.org](https://www.python.org/downloads/)
- Ou use o Microsoft Store
- Ou use conda: `conda install python=3.11`

#### Linux/Mac

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3.11 python3.11-pip

# macOS com Homebrew
brew install python@3.11

# Ou use pyenv
pyenv install 3.11.0 && pyenv global 3.11.0
```

## 🚀 Instalação Automática

1. **Clone o repositório** (se ainda não fez):

```bash
git clone https://github.com/atejap05/mcp-dou-server.git
cd mcp-dou-server
```

2. **Execute o instalador**:

```bash
python install.py
```

O script automaticamente:

- ✅ Verifica a versão do Python
- 📦 Instala todas as dependências
- 🔧 Configura o ambiente (.env)
- 📁 Cria diretórios necessários
- 🧪 Testa a instalação

## 🔧 Instalação Manual

Se preferir instalar manualmente:

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar ambiente

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite suas credenciais INLABS
nano .env  # ou seu editor favorito
```

### 3. Criar diretórios

```bash
mkdir -p cache logs downloads
```

## ⚙️ Configuração

### Credenciais INLABS

Edite o arquivo `.env` com suas credenciais:

```env
INLABS_EMAIL=seu_email@dominio.com
INLABS_PASSWORD=sua_senha_segura
```

### Claude Desktop

Adicione ao arquivo `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "dou": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "/caminho/absoluto/para/mcp-dou-server"
    }
  }
}
```

**Localizações do arquivo de configuração:**

- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

## 🧪 Teste da Instalação

### 1. Teste básico do servidor:

```bash
python run_server.py
```

### 2. Teste das credenciais:

```bash
python -c "
from src.auth.inlabs_auth import get_auth_instance
import asyncio

async def test():
    auth = get_auth_instance()
    result = await auth.test_connection()
    print(result.message)

asyncio.run(test())
"
```

### 3. Teste com Claude Desktop:

- Reinicie Claude Desktop
- Digite: "Liste as seções disponíveis do DOU"
- Verifique se o ícone de ferramentas aparece

## ❌ Solução de Problemas

### Erro de importação MCP

```bash
# Instale a versão mais recente
pip install "mcp[cli]>=1.2.0"
```

### Erro de autenticação INLABS

- Verifique suas credenciais no arquivo `.env`
- Teste login manual no site da INLABS
- Verifique conectividade com internet

### Claude Desktop não detecta o servidor

- Verifique o caminho absoluto no arquivo de configuração
- Reinicie Claude Desktop após mudanças
- Verifique logs de erro do Claude

### Problemas de dependências

```bash
# Limpe o cache do pip e reinstale
pip cache purge
pip install -r requirements.txt --force-reinstall
```

## 🔄 Atualização

Para atualizar o servidor:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## 📞 Suporte

- 📚 Documentação completa: `README.md`
- 🐛 Reportar bugs: GitHub Issues
- 💬 Discussões: GitHub Discussions
