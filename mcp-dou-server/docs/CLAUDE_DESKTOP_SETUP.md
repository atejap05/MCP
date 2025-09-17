# 🔧 Configuração do Claude Desktop para MCP DOU

## 📋 Instruções de Configuração

### 1. Localize o arquivo de configuração do Claude Desktop:

**Windows:**

```
%APPDATA%\Claude\claude_desktop_config.json
```

**Caminho completo típico:**

```
C:\Users\[SEU_USUARIO]\AppData\Roaming\Claude\claude_desktop_config.json
```

### 2. Use uma das configurações abaixo:

#### ✅ **Opção 1: Configuração Recomendada (Script Standalone)**

```json
{
  "mcpServers": {
    "dou-server": {
      "command": "C:\\Users\\94512868372\\Anaconda3\\envs\\pandas-course\\python.exe",
      "args": [
        "d:\\Git_Projects\\MCP\\mcp-dou-server\\run_server_standalone.py"
      ],
      "env": {
        "PYTHONPATH": "d:\\Git_Projects\\MCP\\mcp-dou-server"
      }
    }
  }
}
```

#### 🔧 **Opção 2: Usando Script Batch**

```json
{
  "mcpServers": {
    "dou-server": {
      "command": "d:\\Git_Projects\\MCP\\mcp-dou-server\\run_server.bat"
    }
  }
}
```

### 3. Após configurar:

1. **Salve o arquivo** `claude_desktop_config.json`
2. **Feche completamente** o Claude Desktop
3. **Reinicie** o Claude Desktop
4. **Verifique** se o servidor "dou-server" aparece na lista de MCP servers

## 🧪 **Teste Local**

Antes de configurar o Claude Desktop, teste se o servidor funciona:

```cmd
cd /d "d:\Git_Projects\MCP\mcp-dou-server"
C:\Users\94512868372\Anaconda3\envs\pandas-course\python.exe run_server_standalone.py
```

Deve aparecer:

```
🚀 Iniciando Servidor MCP DOU...
📁 Diretório do servidor: d:\Git_Projects\MCP\mcp-dou-server
🐍 Python: C:\Users\94512868372\Anaconda3\envs\pandas-course\python.exe
📋 Para parar o servidor, use Ctrl+C
==================================================
2025-09-17 16:16:37,326 - src.server - INFO - Servidor MCP DOU iniciado - Versão 0.1.0
2025-09-17 16:16:37,364 - src.server - INFO - Servidor 'dou' criado com sucesso
```

## 🔍 **Troubleshooting**

### Se o servidor não conectar:

1. **Verifique os caminhos** no arquivo de configuração
2. **Confirme** que o ambiente `pandas-course` existe
3. **Teste** o servidor localmente primeiro
4. **Verifique** os logs do Claude Desktop

### Se aparecer "Server disconnected":

1. Use a **Opção 1** (script standalone)
2. Certifique-se que todos os caminhos estão corretos
3. Teste o comando manualmente no terminal

## 🚀 **Ferramentas Disponíveis**

Quando configurado corretamente, você terá acesso a:

- 🔐 **configure_credentials** - Configurar credenciais INLABS
- 🧪 **test_connection** - Testar conexão
- 📋 **list_available_sections** - Listar seções do DOU
- 📥 **download_dou_xml** - Baixar XML
- 📄 **download_dou_pdf** - Baixar PDF
- ✅ **check_file_availability** - Verificar disponibilidade
- 📊 **get_server_info** - Informações do servidor
- 📈 **get_dou_statistics** - Estatísticas
- 📅 **validate_date_range** - Validar datas
