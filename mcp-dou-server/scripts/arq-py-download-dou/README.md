# INLABS - Download Automático DOU

Este projeto contém scripts Python para download automático de publicações do Diário Oficial da União (DOU) em formato XML e PDF.

## 📋 Instruções de Utilização

### Passo 1: Download dos Scripts

Faça o download dos arquivos:

- `inlabs-auto-download-xml.py` (para arquivos XML)
- `inlabs-auto-download-pdf.py` (para arquivos PDF)

### Passo 2: Configuração de Credenciais

Edite o arquivo alterando as informações de login e senha nas linhas 4 e 5:

```python
email = "joaosilva@email.com"
senha = "J0ao747$#"
```

### Passo 3: Configuração das Seções DOU

Altere as seções desejadas na variável `tipo_dou` (linha 6 ou 7). Separe as seções por espaço:

#### Exemplos para XML:

```python
# Exemplo 1: Seções básicas
tipo_dou = "DO1 DO2 DO3"

# Exemplo 2: Seções extras
tipo_dou = "DO1E DO2E DO3E"

# Exemplo 3: Misto
tipo_dou = "DO1 DO1E DO2 DO2E"
```

#### Exemplos para PDF:

```python
# Exemplo 1: Todas as seções
tipo_dou = "do1 do2 do3"

# Exemplo 2: Seções específicas
tipo_dou = "do1 do2"

# Exemplo 3: Uma seção apenas
tipo_dou = "do3"
```

### Passo 4: Execução dos Scripts

Execute os comandos abaixo para realizar o download:

```bash
# Para arquivos XML
python -W ignore inlabs-auto-download-xml.py

# Para arquivos PDF
python -W ignore inlabs-auto-download-pdf.py
```

### 💡 Sugestões

- Adicione entradas no crontab para execuções periódicas de acordo com sua necessidade
- Configure execuções automáticas para manter os dados sempre atualizados

---

## 📚 Visão Geral - Diário Oficial da União (DOU)

### Seções do DOU

De acordo com a **Portaria nº 268, de 05 de outubro de 2009** da Imprensa Nacional, o conteúdo do Diário Oficial da União é dividido em três seções:

| Seção        | Descrição                                                                                                                                                                                                                                                                                                                                                      |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Seção 01** | "Atos normativos de interesse geral" (leis, decretos, resoluções, instruções normativas, portarias e outros)                                                                                                                                                                                                                                                   |
| **Seção 02** | "Atos de pessoal relativos aos servidores públicos"                                                                                                                                                                                                                                                                                                            |
| **Seção 03** | "Extratos de instrumentos contratuais" (acordos, ajustes, autorizações de compra, contratos, convênios, ordens de execução de serviço, termos aditivos e instrumentos congêneres) editais de citação, intimação, notificação e concursos públicos, comunicados, avisos de licitação entre outros atos da administração pública decorrentes de disposição legal |

### Formato dos Arquivos

O acesso disponibiliza as publicações do Diário Oficial da União em:

- **Formato**: XML (extensible mark-up language)
- **Compactação**: ZIP
- **Estrutura de acesso**: `ANO-MES-DIA / ANO-MES-DIA-SECAO.zip`

### ⚠️ Informações Importantes

- O conteúdo dos arquivos em "formato aberto" **não substitui** a publicação da versão certificada (PDF)
- As publicações dos dados do DOU em formato aberto serão disponibilizadas até o **quinto dia útil do mês subsequente** contendo as edições publicadas no mês anterior
- O dicionário de dados, arquivo necessário para auxiliar no entendimento do conteúdo em XML, será disponibilizado em data a ser definida

---

## 📖 Dicionário de Dados do XML

| Posição XML                      | Descrição                                                                                                                                                                                                                      |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Xml/article@id`                 | Id da matéria/artigo gerado pelo sistema editorial GN4 (não possui nenhuma referência com sistemas satélites)                                                                                                                  |
| `Xml/article@name`               | Nome da matéria no GN4                                                                                                                                                                                                         |
| `Xml/article@idOficio`           | Nº do id do ofício. O conceito de ofício é de grupo de matérias em um mesmo lote                                                                                                                                               |
| `Xml/article@pubName`            | Nome ou número da sessão (DOU1, DOU2, DOU3)                                                                                                                                                                                    |
| `Xml/article@artType`            | Tipo da matéria (ie. Portaria, Ato, e outros)                                                                                                                                                                                  |
| `Xml/article@pubDate`            | Data de publicação da matéria em formato dd/mm/aaaa                                                                                                                                                                            |
| `Xml/article@artClass`           | Código de ordenação usada na publicação do Portal (ex.: 00006:00004: 00007:00000: 00000:00000: 00000:00000: 00000:00000: 00024:00002)                                                                                          |
| `Xml/article@artCategory`        | Fornece a grade completa da matéria separado por "/"                                                                                                                                                                           |
| `Xml/article@artSize`            | Largura da matéria (ie. 12 ou 25cm)                                                                                                                                                                                            |
| `Xml/article@artNotes`           | Armazena informações de notas inseridas pelos usuários durante a produção                                                                                                                                                      |
| `Xml/article@numberPage`         | Nº da página na qual a matéria está conectada                                                                                                                                                                                  |
| `Xml/article@pdfPage`            | URL para acessar a página publicada em PDF                                                                                                                                                                                     |
| `Xml/article@editionNumber`      | Número da edição                                                                                                                                                                                                               |
| `Xml/article@highlightType`      | Tipos destaque (Destaque DOU, Concurso Seleção e Destaque Especial)                                                                                                                                                            |
| `Xml/article@highlightPriority`  | Priorização do destaque                                                                                                                                                                                                        |
| `Xml/article@highlight`          | Texto que será publicado no destaque Portal                                                                                                                                                                                    |
| `Xml/article@highlightImage`     | Imagem do destaque com o código base64 da imagem (formato HTML)                                                                                                                                                                |
| `Xml/article@highlightImageName` | Nome da imagem de destaque                                                                                                                                                                                                     |
| `Xml/article@idMateria`          | Nº do id da matéria publicada no Portal                                                                                                                                                                                        |
| `Xml/article/body/Identifica`    | Texto que identifica aquela norma na estrutura organização da origem ("Portaria 131 de 21 de março de 2017")                                                                                                                   |
| `Xml/article/body/Data`          | Texto contendo a data que identifica a matéria (Portaria 131 de "21 de março de 2017")                                                                                                                                         |
| `Xml/article/body/Ementa`        | Dado não obrigatório, mas existem matérias com este campo                                                                                                                                                                      |
| `Xml/article/body/Titulo`        | Dado não obrigatório, mas existem matérias com este campo                                                                                                                                                                      |
| `Xml/article/body/SubTitulo`     | Dado não obrigatório, mas existem matérias com este campo                                                                                                                                                                      |
| `Xml/article/body/Texto`         | Conterá o conteúdo completo da matéria, do título até a assinatura/cargo obedecendo a ordem do texto. E contará com classes relacionadas a estrutura de TAGs (identifica, ementa, titulo, subtitulo, data, assina, cargo, img) |
| `Xml/article/Midias/Midia`       | Legenda da(s) imagem(ns)                                                                                                                                                                                                       |

---

## 🏛️ Imprensa Nacional - INLABS

**Ajuda e Suporte**: Imprensa Nacional - INLABS
