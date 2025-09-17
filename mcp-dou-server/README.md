# MCP DOU Server - Servidor MCP para Diário Oficial da União

## 📋 Descrição

Servidor Model Context Protocol (MCP) para integração com o Diário Oficial da União (DOU) brasileiro. Permite que assistentes de IA como Claude consultem, baixem e analisem publicações oficiais do governo brasileiro de forma natural e eficiente.

## 🚀 Características

- **Download Automático**: Baixa arquivos XML e PDF do DOU por data e seção
- **Busca Inteligente**: Pesquisa por conteúdo, tipo de ato, órgão e outros critérios
- **Parser XML**: Extração estruturada de dados das publicações oficiais
- **Autenticação Segura**: Integração com sistema INLABS da Imprensa Nacional
- **Cache Inteligente**: Evita downloads desnecessários e acelera consultas
- **Compatibilidade MCP**: Funciona com Claude Desktop e outros clientes MCP

## 🛠️ Instalação

### Pré-requisitos

- Python 3.10 ou superior
- Conta no sistema INLABS da Imprensa Nacional

### Instalação via pip

```bash
pip install mcp-dou-server
```

### Instalação para desenvolvimento

```bash
git clone https://github.com/atejap05/mcp-dou-server.git
cd mcp-dou-server
pip install -e ".[dev]"
```

## ⚙️ Configuração

1. **Configurar credenciais INLABS**:
   Crie um arquivo `.env` na raiz do projeto:

   ```env
   INLABS_EMAIL=seu_email@dominio.com
   INLABS_PASSWORD=sua_senha_segura
   DOU_CACHE_DIR=./cache
   DOU_MAX_CACHE_SIZE=1000
   ```

2. **Configurar Claude Desktop**:
   Adicione ao arquivo `claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "dou": {
         "command": "python",
         "args": ["-m", "src.server"],
         "cwd": "/caminho/para/mcp-dou-server"
       }
     }
   }
   ```

## 🔧 Uso

### Ferramentas Disponíveis

#### Download e Acesso

- `download_dou_xml()` - Download de arquivos XML por data/seções
- `download_dou_pdf()` - Download de PDFs oficiais
- `check_file_availability()` - Verificar disponibilidade de arquivos

#### Busca e Consulta

- `search_dou_content()` - Busca textual no conteúdo
- `list_publications()` - Listar publicações por critérios
- `get_publication_details()` - Detalhes de publicação específica
- `search_by_article_type()` - Busca por tipo (portaria, decreto, etc)

#### Análise

- `parse_xml_content()` - Extrair dados estruturados
- `extract_metadata()` - Metadados das publicações
- `generate_summary()` - Resumos automáticos

#### Utilitários

- `list_available_sections()` - Seções DOU disponíveis
- `get_dou_statistics()` - Estatísticas de publicações
- `configure_credentials()` - Configurar autenticação

### Exemplos de Uso com Claude

```
"Baixe as publicações do DOU de hoje"
"Procure por portarias do Ministério da Saúde em setembro de 2024"
"Quais decretos foram publicados ontem na seção 1?"
"Resuma as principais publicações sobre educação desta semana"
```

## 📁 Estrutura do Projeto

```
mcp-dou-server/
├── src/
│   ├── server.py              # Servidor MCP principal
│   ├── auth/
│   │   └── inlabs_auth.py     # Autenticação INLABS
│   ├── tools/
│   │   ├── download.py        # Ferramentas de download
│   │   ├── search.py          # Ferramentas de busca
│   │   ├── parser.py          # Parser XML DOU
│   │   └── utils.py           # Utilitários
│   ├── models/
│   │   └── dou_models.py      # Modelos de dados
│   └── config/
│       └── settings.py        # Configurações
├── tests/                     # Testes automatizados
├── docs/                      # Documentação
├── examples/                  # Exemplos de uso
└── cache/                     # Cache local (criado automaticamente)
```

## 🧪 Testes

```bash
# Executar todos os testes
pytest

# Testes com cobertura
pytest --cov=src --cov-report=html

# Testes específicos
pytest tests/test_download.py -v
```

## 📖 Seções do DOU

O DOU é dividido em três seções principais:

| Seção       | Descrição                               | Códigos XML | Códigos PDF |
| ----------- | --------------------------------------- | ----------- | ----------- |
| **Seção 1** | Atos normativos de interesse geral      | DO1, DO1E   | do1         |
| **Seção 2** | Atos de pessoal dos servidores públicos | DO2, DO2E   | do2         |
| **Seção 3** | Extratos contratuais e editais          | DO3, DO3E   | do3         |

**Legenda**: E = Edição Extra

## 🔒 Segurança

- Credenciais armazenadas em variáveis de ambiente
- Sessões seguras com cookies criptografados
- Validação de entrada em todas as ferramentas
- Logs de auditoria para todas as operações

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

## 🏛️ Créditos

- **Imprensa Nacional - INLABS**: Sistema oficial de acesso aos dados do DOU
- **Model Context Protocol**: Anthropic e comunidade open-source
- **Diário Oficial da União**: Imprensa Nacional do Brasil

## 📞 Suporte

- 📧 Email: admin@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/atejap05/mcp-dou-server/issues)
- 📚 Documentação: [Documentação Completa](https://github.com/atejap05/mcp-dou-server/docs)

---

**Nota**: Este é um projeto independente e não é oficialmente afiliado à Imprensa Nacional ou ao Governo Federal do Brasil.
