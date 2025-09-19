# Documentação do Projeto MCP-JUD

## Visão Geral

O projeto MCP-JUD é um servidor MCP (Model Context Protocol) desenvolvido para fornecer ferramentas de consulta a dados judiciais brasileiros, com foco inicial no Tribunal Regional Federal da 1ª Região (TRF1). O servidor permite que aplicações compatíveis com MCP (como Claude Desktop) consultem processos judiciais, façam buscas por temas e analisem dados processuais através de uma interface padronizada.

## Arquitetura do Sistema

O projeto segue uma arquitetura simplificada baseada no protocolo MCP, utilizando apenas os componentes essenciais para scraping e exposição de ferramentas:

### 1. Core (Núcleo)

- **Configuração**: Configurações básicas de logging e URLs dos tribunais
- **Logging**: Sistema de logs estruturados para monitoramento e debugging

### 2. Application (Aplicação)

- **TRF1Scraper**: Scraper específico para o TRF1 usando httpx e BeautifulSoup
  - Extração de ViewState para formulários JSF
  - Parsing de HTML para extração de andamentos
  - Implementação de cache básico para otimizar requisições

### 3. MCP Server

- **FastMCP**: Framework para criação de servidores MCP
- **Tools**: Três ferramentas principais expostas via protocolo MCP
- **Transporte**: Comunicação via stdio para integração com clientes MCP

## Tools Disponíveis

### 1. `consultar_processo`

**Função**: Consulta os andamentos de um processo judicial específico.

**Parâmetros**:
- `numero_processo`: String - Número do processo no formato CNJ (ex: `1026220-43.2025.4.01.3600`)
- `grau`: String - Grau do processo (`G1` ou `G2`, padrão: `G1`)

**Retorno**: String formatada com lista de andamentos do processo.

**Implementação**: Utiliza TRF1Scraper para fazer scraping do site do tribunal e extrair andamentos.

### 2. `consultar_temas`

**Função**: Busca processos por temas, assuntos ou palavras-chave.

**Parâmetros**:
- `filtro`: String - Palavra-chave ou tema para buscar

**Retorno**: Orientação sobre implementação (atualmente placeholder).

**Status**: Requer integração com API DataJud para implementação completa.

### 3. `resumir_analisar`

**Função**: Faz resumo e análise dos dados de um processo judicial.

**Parâmetros**:
- `dados_processo`: String - Dados do processo (geralmente saída de `consultar_processo`)

**Retorno**: Análise estruturada incluindo:
- Número total de andamentos
- Análise temporal (primeiro/último andamento)
- Tipos de andamento mais frequentes
- Padrões identificados
- Possíveis decisões/julgamentos

**Implementação**: Análise heurística baseada em padrões de texto nos dados fornecidos.

## Funcionalidades Principais

### Consulta de Processos

- **Scraping TRF1**: Extração automática de andamentos do Tribunal Regional Federal da 1ª Região
- **Suporte a graus**: Consulta de processos em primeiro grau (G1) e segundo grau (G2)
- **Formatação estruturada**: Apresentação clara e organizada dos dados extraídos
- **Tratamento de erros**: Logging detalhado e mensagens de erro informativas

### Busca por Temas

- **Interface preparada**: Estrutura pronta para integração com API DataJud
- **Orientação implementativa**: Documentação sobre próximos passos para busca por assuntos
- **Expansibilidade**: Arquitetura preparada para múltiplas fontes de dados

### Análise e Resumo

- **Análise temporal**: Identificação do primeiro e último andamento
- **Estatísticas de andamento**: Contagem e categorização de tipos de movimentação
- **Padrões identificados**: Detecção automática de processos ativos/inativos
- **Identificação de decisões**: Reconhecimento de sentenças, acórdãos e decisões

## Tecnologias Utilizadas

- **MCP SDK**: Protocolo Model Context Protocol para exposição de ferramentas
- **FastMCP**: Framework Python para criação rápida de servidores MCP
- **httpx**: Cliente HTTP assíncrono para requisições web
- **BeautifulSoup4**: Parsing e extração de dados HTML
- **lxml**: Parser XML/HTML de alta performance
- **Pydantic**: Validação e serialização de dados
- **python-dotenv**: Gerenciamento de variáveis de ambiente

## Fluxo de Dados

### Consulta de Processo

1. **Recebimento**: Tool `consultar_processo` recebe número do processo e grau
2. **Validação**: Verificação básica do formato do número
3. **Scraping**: TRF1Scraper faz requisições HTTP para o site do tribunal
4. **Extração**: Parsing do HTML para identificar andamentos
5. **Formatação**: Estruturação dos dados em formato legível
6. **Retorno**: Dados formatados retornados via protocolo MCP

### Análise de Dados

1. **Recebimento**: Tool `resumir_analisar` recebe dados do processo
2. **Parsing**: Extração de andamentos individuais dos dados
3. **Análise**: Processamento estatístico e identificação de padrões
4. **Síntese**: Geração de relatório analítico estruturado
5. **Retorno**: Análise completa retornada ao cliente MCP

## Scraping e Integração com DataJud

### Implementação Atual

O sistema utiliza scraping web direto dos sites dos tribunais, especificamente:

- **TRF1 (Tribunal Regional Federal da 1ª Região)**
- **Suporte a G1 e G2**: Primeiro e segundo graus de jurisdição
- **Técnicas avançadas**: Extração de ViewState, handling de formulários JSF
- **Cache inteligente**: Redução de requisições repetidas

### Limitações do Scraping

- **Dependência de HTML**: Vulnerável a mudanças na estrutura dos sites
- **Performance**: Requisições HTTP mais lentas que APIs dedicadas
- **Limitações de busca**: Dificuldade para buscas por tema/assunto
- **Escopo limitado**: Atualmente apenas TRF1 implementado

### Integração com DataJud

A API DataJud do CNJ oferece vantagens significativas:

- **Busca por assunto**: Possibilita consultas por temas e classes processuais
- **Dados estruturados**: Informações normalizadas e completas
- **Performance**: Respostas mais rápidas e confiáveis
- **Cobertura nacional**: Acesso a todos os tribunais brasileiros

Para implementar:
1. Obter credenciais da API DataJud
2. Implementar autenticação OAuth2
3. Desenvolver endpoints de busca e consulta
4. Migrar gradualmente do scraping

## Testes

### Estratégia de Testes

- **Testes funcionais**: Validação das tools MCP com dados reais
- **Testes de integração**: Verificação do fluxo completo de scraping
- **Testes de erro**: Cenários de falha e tratamento de exceções
- **Script automatizado**: `test_mcp_tools.py` para validação rápida

### Cobertura

- **consultar_processo**: Teste com número real de processo
- **consultar_temas**: Validação da resposta orientativa
- **resumir_analisar**: Teste com dados simulados estruturados

## Configuração e Execução

### Pré-requisitos

- Python 3.10+
- Ambiente virtual (recomendado)
- Conexão com internet para scraping

### Instalação

```bash
# Clonar repositório
git clone <repository-url>
cd mcp-jud

# Criar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt
```

### Configuração no Cliente MCP

Para Claude Desktop:

1. Localizar arquivo de configuração
2. Adicionar servidor MCP-JUD
3. Configurar caminho do executável
4. Reinicializar cliente

### Execução Independente

```bash
# Executar servidor MCP
python mcp_server.py

# Testar tools
python test_mcp_tools.py
```

## Limitações e Melhorias Futuras

### Limitações Atuais

- **Escopo geográfico**: Apenas TRF1 implementado
- **Busca limitada**: Sem suporte nativo a busca por temas
- **Dependência de scraping**: Vulnerável a mudanças nos sites
- **Sem cache persistente**: Dados não armazenados entre sessões

### Melhorias Planejadas

#### Curto Prazo
- **Cache Redis**: Implementar cache distribuído para melhor performance
- **Múltiplos tribunais**: Adicionar suporte a outros TRFs
- **Rate limiting**: Controle de frequência de requisições
- **Retry logic**: Estratégia de tentativas para falhas temporárias

#### Médio Prazo
- **API DataJud**: Integração completa com API oficial do CNJ
- **Busca avançada**: Filtros por data, juiz, vara, etc.
- **Dados enriquecidos**: Extração de metadados completos (partes, valores)
- **Interface web**: Dashboard administrativo para monitoramento

#### Longo Prazo
- **Machine Learning**: Análises preditivas de duração de processos
- **Notificações**: Sistema de alertas para movimentações importantes
- **API pública**: Exposição de dados agregados anonimizados
- **Multi-tenant**: Suporte a múltiplas organizações

## Monitoramento e Observabilidade

### Logging

- **Estrutura JSON**: Logs estruturados para fácil parsing
- **Níveis configuráveis**: INFO, WARNING, ERROR
- **Contexto rico**: Inclusão de metadados relevantes
- **Performance**: Logging assíncrono para não impactar performance

### Métricas

- **Contadores**: Número de consultas por tool
- **Latência**: Tempo de resposta das operações
- **Taxa de erro**: Percentual de falhas por operação
- **Cache hits/misses**: Eficiência do sistema de cache

### Alertas

- **Limites de erro**: Notificação quando taxa de erro ultrapassa threshold
- **Performance**: Alertas para degradação de performance
- **Disponibilidade**: Monitoramento de uptime do serviço

## Segurança

### Considerações de Segurança

- **HTTPS**: Todas as requisições usam HTTPS
- **Rate limiting**: Controle de frequência para prevenir abuso
- **Input validation**: Validação rigorosa de parâmetros
- **Error handling**: Não exposição de detalhes internos em erros

### Dados Sensíveis

- **Anonimização**: Dados processuais são públicos por natureza
- **Não armazenamento**: Dados não são persistidos localmente
- **Transmissão segura**: Comunicação encriptada via HTTPS

## Contribuição e Desenvolvimento

### Estrutura do Código

```
mcp-jud/
├── mcp_server.py          # Servidor MCP principal
├── test_mcp_tools.py       # Script de testes
├── requirements.txt        # Dependências
├── README.md              # Documentação de uso
├── doc/
│   └── documentacao_projeto.md  # Esta documentação
└── app/
    ├── core/
    │   └── config.py      # Configurações
    └── application/
        └── services/
            └── trf1_scraper.py  # Scraper TRF1
```

### Padrões de Desenvolvimento

- **Type hints**: Uso consistente de type hints
- **Docstrings**: Documentação completa das funções
- **Error handling**: Tratamento robusto de exceções
- **Logging**: Logs informativos em todas as operações críticas

### Testes Locais

```bash
# Executar testes
python test_mcp_tools.py

# Verificar logs
# Logs são exibidos no console durante execução
```

Esta documentação fornece uma visão abrangente do sistema MCP-JUD, permitindo compreensão profunda de sua arquitetura, funcionalidades e operação como servidor MCP.
