# MCP-JUD Server

Servidor MCP (Model Context Protocol) para consultas judiciais no Tribunal Regional Federal da 1ª Região (TRF1).

## Visão Geral

Este servidor MCP fornece ferramentas para interagir com dados judiciais brasileiros, permitindo que aplicações MCP (como Claude Desktop) consultem processos judiciais, façam buscas por temas e analisem dados processuais.

## Arquitetura MCP

O MCP-JUD é construído sobre o **Model Context Protocol (MCP)**, um protocolo aberto que permite aos modelos de IA (como Claude) acessar ferramentas e dados externos de forma segura e padronizada.

### Como Funciona

1. **Cliente MCP** (Claude Desktop) inicia conexão com o servidor
2. **Servidor MCP** (mcp_server.py) expõe ferramentas disponíveis
3. **Cliente** pode invocar ferramentas através de prompts naturais
4. **Servidor** executa a ferramenta e retorna resultados estruturados

### Vantagens do MCP

- **Interface Natural**: Use linguagem natural para acessar dados judiciais
- **Segurança**: Protocolo projetado com isolamento e controle de acesso
- **Extensibilidade**: Fácil adição de novas ferramentas
- **Padronização**: Compatível com qualquer cliente MCP

## Tools Disponíveis

### 1. `consultar_processo`

Consulta os andamentos de um processo judicial específico.

**Parâmetros:**

- `numero_processo`: Número do processo no formato CNJ (ex: `1026220-43.2025.4.01.3600`)
- `grau`: Grau do processo (`G1` ou `G2`, padrão: `G1`)

**Exemplo de uso:**

```text
Consultar o processo 1026220-43.2025.4.01.3600 no primeiro grau
```

```

### 2. `consultar_temas`

Busca processos por temas, assuntos ou palavras-chave.

**Nota:** Esta funcionalidade atualmente retorna orientações sobre implementação, pois requer integração com a API DataJud do CNJ.

**Parâmetros:**

- `filtro`: Palavra-chave ou tema para buscar

**Exemplo de uso:**

```

Buscar processos sobre "Bônus de Eficiência"

```

### 3. `resumir_analisar`

Faz resumo e análise dos dados de um processo judicial.

**Parâmetros:**

- `dados_processo`: String contendo os dados do processo (geralmente saída de `consultar_processo`)

**Exemplo de uso:**

```

Analisar os dados deste processo: [colar saída de consultar_processo]

````

## Instalação e Configuração

### Pré-requisitos

- Python 3.10 ou superior
- Ambiente virtual (recomendado)
- Conexão com internet para scraping de dados judiciais

### Instalação

```bash
# 1. Clonar ou baixar o projeto
cd mcp-jud

# 2. Criar ambiente virtual
python -m venv venv

# 3. Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
# source venv/bin/activate

# 4. Instalar dependências
pip install -r requirements.txt
```

### Configuração no Claude Desktop

#### Windows

1. Abra o arquivo de configuração: `%APPDATA%\Claude\claude_desktop_config.json`
2. Adicione a configuração do servidor:

```json
{
  "mcpServers": {
    "mcp-jud": {
      "command": "python",
      "args": ["C:\\caminho\\para\\mcp-jud\\mcp_server.py"],
      "env": {
        "PYTHONPATH": "C:\\caminho\\para\\mcp-jud"
      }
    }
  }
}
```

#### macOS

1. Abra o arquivo de configuração: `~/Library/Application Support/Claude/claude_desktop_config.json`
2. Adicione a configuração do servidor:

```json
{
  "mcpServers": {
    "mcp-jud": {
      "command": "python",
      "args": ["/caminho/para/mcp-jud/mcp_server.py"],
      "env": {
        "PYTHONPATH": "/caminho/para/mcp-jud"
      }
    }
  }
}
```

3. **Importante**: Reinicie o Claude Desktop completamente após salvar as alterações.

### Verificação da Instalação

Após configurar, teste se o servidor está funcionando:

```bash
# Executar testes das tools
python test_mcp_tools.py
```

Se os testes passarem, o servidor MCP está configurado corretamente.

## Uso

Após configurar, as tools estarão disponíveis no Claude Desktop. Você pode interagir naturalmente com os dados judiciais através de prompts em português.

### Exemplos Práticos

#### 1. Consultar um Processo Específico

```
"Me mostre os andamentos do processo 1026220-43.2025.4.01.3600 no primeiro grau"
```

#### 2. Analisar um Processo

```
"Consulte o processo 1026220-43.2025.4.01.3600 e depois faça uma análise completa dos dados"
```

#### 3. Buscar por Temas

```
"Quais processos existem sobre pensão alimentícia?"
```

#### 4. Análise Comparativa

```
"Compare os andamentos desses dois processos: 1026220-43.2025.4.01.3600 e 1026221-43.2025.4.01.3600"
```

### Comandos Avançados

O Claude pode encadear múltiplas operações automaticamente:

```
"Consulte o processo X, analise os dados, e me diga se há alguma decisão recente"
```

## Troubleshooting

### Problemas Comuns

#### "MCP server not found" ou "Tool not available"

1. **Verifique o caminho**: Certifique-se de que o caminho para `mcp_server.py` está correto no arquivo de configuração
2. **Reinicie o Claude**: Feche completamente o Claude Desktop e reabra
3. **Verifique o Python**: Execute `python --version` no terminal para confirmar que está usando Python 3.10+
4. **Teste local**: Execute `python test_mcp_tools.py` para verificar se o servidor funciona

#### "Erro de conexão" ou timeouts

1. **Conexão de internet**: Verifique se há conexão estável
2. **Firewall**: Certifique-se de que o Python pode fazer requisições HTTP
3. **Site do TRF1**: O tribunal pode estar temporariamente indisponível

#### "Processo não encontrado"

1. **Formato do número**: Verifique se o número do processo está no formato correto (NNNNNNN-DD.YYYY.T.OR.OOOO)
2. **Grau do processo**: Confirme se está consultando o grau correto (G1 ou G2)
3. **Disponibilidade**: Alguns processos podem não estar disponíveis publicamente

### Logs de Debug

Para ver logs detalhados, execute o servidor diretamente:

```bash
python mcp_server.py
```

Os logs aparecerão no terminal e podem ajudar a identificar problemas.

### Teste Manual

Se os testes automatizados falharem, teste manualmente:

```python
# No Python interativo
from mcp_server import consultar_processo
import asyncio

# Teste básico
resultado = asyncio.run(consultar_processo("1026220-43.2025.4.01.3600", "G1"))
print(resultado)
```

## Limitações Atuais

- **Escopo limitado:** Atualmente funciona apenas com o TRF1 (Tribunal Regional Federal da 1ª Região)
- **Busca por temas:** Requer integração com API DataJud para buscas eficientes por assunto
- **Dados disponíveis:** Limita-se aos andamentos públicos disponíveis no sistema do tribunal

## Desenvolvimento Futuro

- Integração com API DataJud para busca nacional por temas
- Suporte a múltiplos tribunais regionais
- Extração de metadados completos (partes, valores, etc.)
- Análises mais avançadas com IA
- Cache inteligente para melhorar performance

## Desenvolvimento

### Estrutura do Projeto

```
mcp-jud/
├── mcp_server.py          # Servidor MCP principal
├── test_mcp_tools.py       # Script de testes
├── requirements.txt        # Dependências Python
├── README.md              # Esta documentação
├── doc/
│   └── documentacao_projeto.md  # Documentação técnica completa
└── app/
    ├── core/
    │   └── config.py      # Configurações e URLs
    └── application/
        └── services/
            └── trf1_scraper.py  # Scraper do TRF1
```

### Adicionando Novas Tools

Para adicionar uma nova ferramenta MCP:

1. Defina a função com decorator `@mcp.tool()`
2. Adicione docstring com descrição e parâmetros
3. Implemente a lógica
4. Adicione testes em `test_mcp_tools.py`

Exemplo:

```python
@mcp.tool()
async def nova_tool(parametro: str) -> str:
    """
    Descrição da nova tool.

    Args:
        parametro: Descrição do parâmetro

    Returns:
        Descrição do retorno
    """
    # Implementação
    return f"Resultado: {parametro}"
```

### Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-tool`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova tool'`)
4. Push para a branch (`git push origin feature/nova-tool`)
5. Abra um Pull Request

### Testes

Para executar os testes:

```bash
python test_mcp_tools.py
```

Os testes validam todas as tools com dados de exemplo e ajudam a identificar regressões.
 
 

 
 
````
