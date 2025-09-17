# 📋 TODO - Funcionalidades Pendentes do Servidor MCP DOU

**Status**: Atualizado em 17/09/2025  
**Versão Atual**: 0.1.0 (Beta)

## 🔍 **ANÁLISE DAS FUNCIONALIDADES FALTANTES**

### ❌ **Funcionalidades Não Implementadas (Críticas)**

#### 1. 🔍 **BUSCA E CONSULTA** - **Alta Prioridade**

**Status**: ⚠️ Skeleton implementado, funcionalidade não desenvolvida

**Impacto**: Esta é a funcionalidade mais solicitada pelos usuários. Sem ela, o servidor é apenas um downloader.

**Ferramentas Afetadas**:

- `search_dou_content()` - Busca textual no conteúdo
- `list_publications()` - Listagem de publicações por critérios

**Funcionalidades Essenciais Faltantes**:

- [ ] Busca por texto livre (ex: "Receita Federal do Brasil")
- [ ] Filtros por data (intervalo)
- [ ] Filtros por seção (DO1, DO2, DO3)
- [ ] Filtros por tipo de ato (portaria, decreto, lei)
- [ ] Filtros por órgão/entidade
- [ ] Busca por número de ato/processo
- [ ] Indexação para busca rápida
- [ ] Ranking de relevância dos resultados

---

#### 2. 🔧 **PARSER DE XML** - **Alta Prioridade**

**Status**: ⚠️ Skeleton implementado, funcionalidade não desenvolvida

**Impacto**: Sem o parser, não é possível extrair conteúdo estruturado dos arquivos XML para realizar buscas.

**Ferramentas Afetadas**:

- `parse_xml_content()` - Parsing completo de XML
- `extract_metadata()` - Extração de metadados

**Funcionalidades Essenciais Faltantes**:

- [ ] Extração de texto dos artigos/matérias
- [ ] Extração de metadados (data, órgão, tipo de ato)
- [ ] Estruturação de dados em formato JSON
- [ ] Suporte aos diferentes formatos de XML por seção
- [ ] Tratamento de caracteres especiais e encoding
- [ ] Cache de dados extraídos
- [ ] Validação de estrutura XML

---

#### 3. 🗄️ **SISTEMA DE INDEXAÇÃO** - **Média Prioridade**

**Status**: ❌ Não implementado

**Impacto**: Necessário para buscas rápidas e eficientes em grandes volumes de dados.

**Funcionalidades Faltantes**:

- [ ] Índice de texto completo
- [ ] Índice por metadados (data, órgão, tipo)
- [ ] Índice por palavras-chave
- [ ] Sistema de cache otimizado
- [ ] Atualização incremental de índices

---

### ✅ **Funcionalidades Implementadas**

- [x] **Autenticação INLABS** - Sistema completo e funcional
- [x] **Download XML/PDF** - Download de arquivos por data e seção
- [x] **Ferramentas Auxiliares** - Configuração, testes, informações
- [x] **Gestão de Cache** - Sistema de armazenamento local organizado
- [x] **Logging e Erro** - Sistema robusto de logs e tratamento de erros

---

## 🎯 **PLANO DE IMPLEMENTAÇÃO PRIORITÁRIO**

### **FASE 1: Parser XML (Semana 1-2)** 🔧

#### **1.1 Análise da Estrutura XML**

- [ ] Estudar estrutura XML das 3 seções (DO1, DO2, DO3)
- [ ] Mapear elementos essenciais para extração
- [ ] Definir schema de dados estruturados
- [ ] Criar testes com amostras reais

#### **1.2 Implementação do Parser Base**

- [ ] Desenvolver classe `DOUXMLParser`
- [ ] Implementar extração de metadados básicos
- [ ] Implementar extração de conteúdo textual
- [ ] Tratar encoding e caracteres especiais

#### **1.3 Estruturação de Dados**

- [ ] Criar modelos Pydantic para dados extraídos
- [ ] Implementar serialização JSON
- [ ] Sistema de cache para dados parseados
- [ ] Validação e limpeza de dados

---

### **FASE 2: Busca Textual (Semana 3-4)** 🔍

#### **2.1 Busca Básica**

- [ ] Implementar busca por texto livre
- [ ] Busca case-insensitive
- [ ] Busca com operadores AND/OR
- [ ] Destacar termos encontrados

#### **2.2 Filtros Avançados**

- [ ] Filtro por intervalo de datas
- [ ] Filtro por seção DOU
- [ ] Filtro por órgão/entidade
- [ ] Filtro por tipo de ato

#### **2.3 Indexação Simples**

- [ ] Criar índice invertido básico
- [ ] Cache de resultados frequentes
- [ ] Otimização de performance

---

### **FASE 3: Funcionalidades Avançadas (Semana 5-6)** 📊

#### **3.1 Análise de Conteúdo**

- [ ] Extração de entidades (órgãos, leis, pessoas)
- [ ] Análise de frequência de termos
- [ ] Detecção de tipos de ato automatizada
- [ ] Extração de datas e números relevantes

#### **3.2 API Avançada**

- [ ] Busca por similaridade
- [ ] Sugestões de busca
- [ ] Estatísticas de uso
- [ ] Exportação de resultados

---

## 🛠️ **ESPECIFICAÇÕES TÉCNICAS**

### **Parser XML - Especificações**

```python
class DOUXMLParser:
    """Parser para arquivos XML do DOU."""

    async def parse_file(self, xml_path: str) -> DOUDocument:
        """Parsea arquivo XML completo."""
        pass

    async def extract_articles(self, xml_content: str) -> List[DOUArticle]:
        """Extrai artigos/matérias do XML."""
        pass

    async def extract_metadata(self, xml_content: str) -> DOUMetadata:
        """Extrai metadados do documento."""
        pass
```

### **Sistema de Busca - Especificações**

```python
class DOUSearchEngine:
    """Motor de busca para conteúdo DOU."""

    async def search_content(
        self,
        query: str,
        filters: DOUSearchFilters
    ) -> DOUSearchResults:
        """Busca no conteúdo com filtros."""
        pass

    async def build_index(self, documents: List[DOUDocument]):
        """Constrói índice de busca."""
        pass
```

---

## 📅 **CRONOGRAMA ESTIMADO**

| Fase       | Duração   | Funcionalidades           | Prioridade |
| ---------- | --------- | ------------------------- | ---------- |
| **Fase 1** | 2 semanas | Parser XML completo       | 🔴 Alta    |
| **Fase 2** | 2 semanas | Busca textual básica      | 🔴 Alta    |
| **Fase 3** | 2 semanas | Funcionalidades avançadas | 🟡 Média   |
| **Teste**  | 1 semana  | Testes e otimização       | 🟢 Baixa   |

**Total Estimado**: 7 semanas para servidor completamente funcional

---

## 🎯 **PRÓXIMOS PASSOS IMEDIATOS**

### **1. Primeira Implementação (Esta Semana)**

- [ ] Analisar estrutura XML de amostras DOU
- [ ] Implementar parser XML básico para DO1
- [ ] Criar extração de texto simples
- [ ] Implementar busca textual rudimentar

### **2. Teste Rápido**

- [ ] Baixar DOU de hoje via MCP
- [ ] Parser o XML baixado
- [ ] Buscar por "Receita Federal do Brasil"
- [ ] Validar resultados encontrados

---

## 💡 **OBSERVAÇÕES IMPORTANTES**

1. **Dependências Adicionais Necessárias**:

   ```python
   # Adicionar ao requirements.txt
   lxml>=4.9.0          # Parser XML eficiente
   beautifulsoup4>=4.12.0  # Parsing HTML/XML
   whoosh>=2.7.4        # Motor de busca/indexação
   nltk>=3.8            # Processamento de linguagem natural
   ```

2. **Estrutura XML Varia por Seção**:

   - DO1: Estrutura mais complexa (leis, decretos)
   - DO2: Foco em recursos humanos
   - DO3: Editais e contratos

3. **Performance Critical**:
   - Arquivos XML podem ser grandes (>100MB)
   - Cache agressivo necessário
   - Indexação offline quando possível

---

**🎯 OBJETIVO: Implementar busca por "Receita Federal do Brasil" funcionando em 1-2 semanas**
