# Guia de Integração com Clientes MCP

## 🎯 Visão Geral

Este guia detalha como conectar seu servidor MCP a diferentes clientes de IA:

- ✅ **Cursor** - IDE com IA integrada
- ✅ **Claude Desktop** - Aplicativo desktop da Anthropic
- ✅ **Continue** - Extensão VS Code
- ✅ **Outros clientes** compatíveis com MCP

## 📋 Pré-requisitos

Antes de configurar os clientes:

1. **Servidor rodando**: `npm run dev` (porta 3000)
2. **Clerk configurado**: Dynamic Client Registration habilitado
3. **Endpoints funcionando**: Teste com `curl http://localhost:3000/.well-known/oauth-authorization-server`

## 🖱️ Cursor

### Configuração Passo a Passo

#### 1. Acessar Configurações MCP

```
Windows/Linux: Ctrl + Shift + P
macOS: Cmd + Shift + P

Digite: "MCP Settings" ou "Open MCP Settings"
```

#### 2. Adicionar Servidor

No arquivo de configuração JSON que abrir:

```json
{
  "mcpServers": {
    "bookmark-manager": {
      "url": "http://localhost:3000/mcp"
    }
  }
}
```

Para produção:

```json
{
  "mcpServers": {
    "bookmark-manager": {
      "url": "https://seu-dominio.com/mcp"
    }
  }
}
```

#### 3. Processo de Autenticação

1. **Status inicial**: Você verá "Needs login" ao lado do servidor
2. **Clicar em "Login"**: Abrirá o navegador
3. **Fazer login no Clerk**: Use suas credenciais
4. **Autorizar**: Clique em "Allow" ou "Permitir"
5. **Voltar ao Cursor**: As ferramentas estarão disponíveis

### Interface do Cursor

```
┌─────────────────────────────────────┐
│ MCP Servers                         │
├─────────────────────────────────────┤
│ ✅ bookmark-manager                 │
│    Tools: 6                         │
│    - get_user_bookmarks             │
│    - create_bookmark                │
│    - delete_bookmark                │
│    - search_bookmarks               │
│    - get_user_info                  │
│    - export_bookmarks               │
└─────────────────────────────────────┘
```

### Testando no Cursor

No chat do Cursor, teste os comandos:

```
"Quais são meus bookmarks?"
"Adicione um bookmark para https://nextjs.org"
"Busque bookmarks sobre React"
"Delete o bookmark com ID abc123"
"Exporte meus bookmarks em formato markdown"
```

### Configurações Avançadas do Cursor

`cursor-settings.json`:

```json
{
  "mcpServers": {
    "bookmark-manager": {
      "url": "http://localhost:3000/mcp",
      "retryAttempts": 3,
      "retryDelay": 1000,
      "timeout": 30000,
      "headers": {
        "X-Custom-Header": "value"
      }
    }
  },
  "mcpClient": {
    "autoConnect": true,
    "showNotifications": true,
    "debugMode": false
  }
}
```

## 🤖 Claude Desktop

### Instalação do mcp-remote

Claude Desktop precisa do `mcp-remote` para conectar a servidores HTTP:

```bash
# Instalação global
npm install -g mcp-remote

# Ou usando npx (sem instalação)
npx mcp-remote --version
```

### Configuração

#### 1. Localizar arquivo de configuração

**Windows**:

```
%APPDATA%\Claude\claude_desktop_config.json
```

**macOS**:

```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux**:

```
~/.config/Claude/claude_desktop_config.json
```

#### 2. Editar configuração

```json
{
  "mcpServers": {
    "bookmark-manager": {
      "command": "npx",
      "args": ["mcp-remote", "http://localhost:3000/mcp", "--allow-http"]
    }
  }
}
```

Para produção com HTTPS:

```json
{
  "mcpServers": {
    "bookmark-manager": {
      "command": "npx",
      "args": ["mcp-remote", "https://seu-dominio.com/mcp"]
    }
  }
}
```

#### 3. Reiniciar Claude Desktop

1. Feche completamente o Claude Desktop
2. Abra novamente
3. Verifique em Settings → MCP Servers

### Autenticação no Claude

1. Claude mostrará uma notificação para autenticar
2. Clique no link que aparece
3. Complete o login no navegador
4. Volte ao Claude - ferramentas estarão disponíveis

### Troubleshooting Claude

Se não funcionar:

```bash
# Teste o mcp-remote diretamente
npx mcp-remote http://localhost:3000/mcp --allow-http --debug

# Verifique logs
# Windows: %APPDATA%\Claude\logs
# macOS: ~/Library/Logs/Claude
# Linux: ~/.local/share/Claude/logs
```

## 🔧 Continue (VS Code)

### Instalação

1. Instale a extensão Continue no VS Code
2. Configure o arquivo `.continuerc.json`:

```json
{
  "models": [
    {
      "title": "Claude 3",
      "provider": "anthropic",
      "model": "claude-3-sonnet",
      "apiKey": "YOUR_API_KEY"
    }
  ],
  "mcpServers": {
    "bookmark-manager": {
      "url": "http://localhost:3000/mcp",
      "auth": {
        "type": "oauth",
        "autoConnect": true
      }
    }
  }
}
```

## 🌐 Configuração para Desenvolvimento

### Usando ngrok para Desenvolvimento Remoto

```bash
# Instalar ngrok
npm install -g ngrok

# Expor servidor local
ngrok http 3000

# Você receberá uma URL como:
# https://abc123.ngrok.io
```

Então use a URL ngrok nas configurações:

```json
{
  "mcpServers": {
    "bookmark-manager": {
      "url": "https://abc123.ngrok.io/mcp"
    }
  }
}
```

### Docker Compose para Desenvolvimento

`docker-compose.yml`:

```yaml
version: "3.8"

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/bookmarks
      - NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=${CLERK_PUBLISHABLE_KEY}
      - CLERK_SECRET_KEY=${CLERK_SECRET_KEY}
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: bookmarks
    volumes:
      - postgres_data:/var/lib/postgresql/data

  ngrok:
    image: ngrok/ngrok:latest
    command:
      - "http"
      - "app:3000"
      - "--domain=seu-dominio.ngrok.io"
    environment:
      - NGROK_AUTHTOKEN=${NGROK_TOKEN}

volumes:
  postgres_data:
```

## 🔍 Debug e Diagnóstico

### Teste Manual com cURL

```bash
# 1. Testar discovery
curl -v http://localhost:3000/.well-known/oauth-authorization-server

# 2. Listar ferramentas (sem auth - deve falhar)
curl -X POST http://localhost:3000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}'

# Resposta esperada: 401 Unauthorized
```

### Logs do Servidor

Adicione logs detalhados em desenvolvimento:

`src/app/api/[transport]/route.ts`:

```typescript
// No início do handler
if (process.env.NODE_ENV === "development") {
  console.log("[MCP Request]", {
    method: request.method,
    headers: Object.fromEntries(request.headers.entries()),
    url: request.url,
  });
}

// Após autenticação
if (process.env.NODE_ENV === "development") {
  console.log("[MCP Auth]", {
    authenticated: !!authInfo?.extra?.userId,
    userId: authInfo?.extra?.userId,
  });
}
```

### Cliente de Teste MCP

`scripts/test-mcp-client.js`:

```javascript
const { Client } = require("@modelcontextprotocol/sdk");

async function testMCPServer() {
  const client = new Client({
    name: "test-client",
    version: "1.0.0",
  });

  try {
    // Conectar ao servidor
    await client.connect({
      url: "http://localhost:3000/mcp",
    });

    console.log("✅ Conectado ao servidor MCP");

    // Listar ferramentas
    const tools = await client.request({
      method: "tools/list",
    });

    console.log("📋 Ferramentas disponíveis:");
    tools.tools.forEach(tool => {
      console.log(`  - ${tool.name}: ${tool.description}`);
    });

    // Desconectar
    await client.close();
  } catch (error) {
    console.error("❌ Erro:", error.message);
  }
}

testMCPServer();
```

## 🚀 Deploy em Produção

### Checklist de Produção

- [ ] HTTPS configurado (obrigatório para OAuth)
- [ ] Variáveis de ambiente de produção
- [ ] Clerk em modo produção
- [ ] Rate limiting implementado
- [ ] Logs e monitoramento configurados
- [ ] Backup do banco de dados
- [ ] URLs de callback atualizadas

### Configuração de Produção

#### Vercel

`vercel.json`:

```json
{
  "functions": {
    "src/app/api/[transport]/route.ts": {
      "maxDuration": 30
    }
  },
  "headers": [
    {
      "source": "/.well-known/(.*)",
      "headers": [
        {
          "key": "Access-Control-Allow-Origin",
          "value": "*"
        }
      ]
    }
  ]
}
```

#### Railway/Render

```yaml
# railway.toml ou render.yaml
services:
  - type: web
    name: bookmark-mcp
    env: node
    buildCommand: npm run build
    startCommand: npm start
    envVars:
      - key: NODE_ENV
        value: production
    domains:
      - bookmarks-mcp.railway.app
```

## 📱 Aplicações Móveis (Futuro)

### React Native com MCP

```typescript
// Exemplo de implementação futura
import { MCPClient } from "@mcp/react-native";

const client = new MCPClient({
  serverUrl: "https://api.bookmarks.com/mcp",
  auth: {
    type: "oauth",
    clientId: "mobile-app",
  },
});

// Usar em componentes
function BookmarkScreen() {
  const { tools, callTool } = useMCP(client);

  const addBookmark = async (url: string) => {
    await callTool("create_bookmark", { url });
  };
}
```

## 🎮 Casos de Uso Avançados

### 1. Integração com Workflows

```typescript
// Cursor: Criar workflow para salvar recursos de pesquisa
"Sempre que eu disser 'salvar isso', adicione a URL atual como bookmark com contexto da conversa";

// Claude: Organizar bookmarks por projeto
"Crie uma categoria 'Projeto X' e mova todos os bookmarks relacionados a React para lá";
```

### 2. Comandos Compostos

```typescript
// Exportar e enviar por email
"Exporte meus bookmarks de desenvolvimento em markdown e prepare um email";

// Análise de bookmarks
"Analise meus bookmarks e sugira categorias baseadas no conteúdo";
```

### 3. Automações

```typescript
// Verificar links quebrados
"Verifique todos os meus bookmarks e liste quais não estão mais acessíveis";

// Backup automático
"Faça backup dos meus bookmarks toda sexta-feira";
```

## 🆘 Suporte e Comunidade

### Recursos

- **Documentação MCP**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **Discord MCP**: [discord.gg/mcp](https://discord.gg/mcp)
- **GitHub Issues**: Para bugs e sugestões
- **Stack Overflow**: Tag `model-context-protocol`

### FAQ

**P: O servidor precisa estar sempre rodando?**
R: Sim, o servidor MCP precisa estar acessível quando os clientes tentarem se conectar.

**P: Posso usar múltiplos servidores MCP?**
R: Sim, cada cliente pode se conectar a vários servidores MCP simultaneamente.

**P: Como renovar tokens expirados?**
R: Os clientes MCP gerenciam automaticamente a renovação de tokens usando refresh tokens.

**P: É seguro expor meu servidor MCP na internet?**
R: Com HTTPS e autenticação OAuth adequada, sim. Sempre use rate limiting e monitore acessos.

---

Com este guia completo, você pode integrar seu servidor MCP com qualquer cliente compatível!
