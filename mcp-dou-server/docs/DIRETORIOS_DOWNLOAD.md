# 📁 Diretório de Download - Servidor MCP DOU

## 📍 **Localização dos Arquivos Baixados**

Quando você usar o prompt **"Baixe o diario oficial de hoje"**, os arquivos serão salvos na seguinte estrutura:

### 🗂️ **Estrutura de Diretórios:**

```
d:\Git_Projects\MCP\mcp-dou-server\
└── cache\                          ← Diretório base (configurável)
    └── 2025\                       ← Ano da publicação
        └── 09\                     ← Mês da publicação (formato 01-12)
            ├── 2025-09-17-DO1.zip  ← DOU Seção 1 (XML)
            ├── 2025-09-17-DO2.zip  ← DOU Seção 2 (XML)
            ├── 2025-09-17-DO3.zip  ← DOU Seção 3 (XML)
            ├── 2025-09-17-DO1.pdf  ← DOU Seção 1 (PDF)
            ├── 2025-09-17-DO2.pdf  ← DOU Seção 2 (PDF)
            └── 2025-09-17-DO3.pdf  ← DOU Seção 3 (PDF)
```

### 📋 **Configuração Atual:**

- **Diretório base**: `./cache` (relativo ao servidor)
- **Caminho completo**: `d:\Git_Projects\MCP\mcp-dou-server\cache\`
- **Organização**: `Ano\Mês\arquivo`
- **Formatos**: XML (ZIP) e PDF

### ⚙️ **Como Alterar o Diretório:**

1. **Crie um arquivo `.env`** na raiz do projeto:

```bash
# Exemplo de configuração personalizada
DOU_CACHE_DIR=D:\MeusArquivos\DOU
DOU_MAX_CACHE_SIZE=2000
DOU_CACHE_TTL_HOURS=48
```

2. **Ou configure via variáveis de ambiente**:

```powershell
# PowerShell
$env:DOU_CACHE_DIR="D:\MeusArquivos\DOU"
```

### 📝 **Exemplos de Arquivos (hoje: 17/09/2025):**

- **XML (ZIP)**: `cache\2025\09\2025-09-17-DO1.zip`
- **PDF**: `cache\2025\09\2025-09-17-DO1.pdf`

### 🔧 **Configurações Relacionadas:**

- **DOU_CACHE_DIR**: Diretório base para downloads (padrão: `./cache`)
- **DOU_MAX_CACHE_SIZE**: Máximo de arquivos em cache (padrão: 1000)
- **DOU_CACHE_TTL_HOURS**: Tempo de vida em cache (padrão: 24 horas)

### ✅ **Verificação:**

Para verificar onde os arquivos estão sendo salvos, você pode usar a ferramenta `get_server_info` que mostrará:

- Diretório de cache configurado
- Espaço usado
- Número de arquivos armazenados

---

**Data da última atualização**: 17 de setembro de 2025
