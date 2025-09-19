# 📋 Relatório de Pesquisa - APIs Judiciais Brasileiras

A principal API pública no Brasil para consulta de processos judiciais é a **API Pública do DataJud (CNJ)**, que expõe metadados de capas e movimentações de processos de todos os segmentos do Judiciário, preservando sigilos e dados protegidos, e alguns tribunais também divulgam acessos orientados a essa API em seus portais de dados abertos, enquanto integrações diretas de sistemas processuais (PJe/MNI) exigem convênios específicos e não são abertas ao público geral. Há ainda provedores comerciais que agregam e enriquecem dados processuais via API (ex.: Judit, Escavador, Jusbrasil, Codilo), mas não se tratam de APIs públicas oficiais do Judiciário.[escavador**+9**](https://api.escavador.com/v1/docs/)

## O que é a API DataJud

A API Pública do DataJud permite acesso público aos metadados de processos judiciais (número do processo, tribunal, classe, órgão julgador, e movimentos) de todas as instâncias do Judiciário brasileiro, com base na Base Nacional de Dados do Poder Judiciário instituída e regulada pelo CNJ. O objetivo é habilitar pesquisas, aplicativos e análises sobre o sistema de Justiça, observando as portarias do CNJ e o resguardo de processos sob segredo de justiça e dados pessoais sensíveis.[datajud-wiki.cnj**+1**](https://datajud-wiki.cnj.jus.br/api-publica/)

## Autenticação e acesso

O acesso é autenticado com uma chave pública (APIKey) gerada e disponibilizada pelo Departamento de Pesquisas Judiciárias do CNJ, informada no cabeçalho “Authorization: APIKey {chave}”, podendo ser alterada a qualquer tempo por razões de segurança e gestão. A documentação oficial referencia onde obter a chave pública vigente e reforça que a API foi aberta ao consumo público após a fase beta, sem necessidade de cadastro individualizado além do uso da APIKey pública.[tjam**+1**](https://www.tjam.jus.br/index.php/transparencia/tecnologia-da-informacao-e-comunicacao/relatorios-dinamicos/numeracao-unica-e-consulta-via-api-do-datajud)

## Estrutura de endpoints

A API adota um padrão por alias de tribunal seguido do recurso de busca, com cada tribunal mapeado para um alias específico e consultas realizadas no endpoint “api*publica*{alias}/\_search” usando método POST e corpo JSON de consulta. Exemplos de aliases documentados incluem tribunais superiores (ex.: TST, TSE, STJ, STM) e regionais federais (TRF1 a TRF6), entre muitos outros na lista oficial de endpoints por tribunal.[datajud-wiki.cnj](https://datajud-wiki.cnj.jus.br/api-publica/endpoints/)

## Consultas típicas

Consultas são enviadas via POST com “Content-Type: application/json” e a APIKey no cabeçalho, usando corpo JSON conforme exemplos oficiais para pesquisar por número CNJ, filtros por tribunal, classe, datas, órgão julgador e outros campos disponibilizados pelo DataJud. Tribunais publicam guias práticos mostrando o passo a passo no Postman para “\_search” do respectivo alias, com autenticação por APIKey e corpo de consulta demonstrativo.[trt24](https://www.trt24.jus.br/web/transparencia/acesso-automatizado-api)

## Escopo e limitações

A API entrega metadados de capa processual e a lista de movimentações, não abrangendo peças integrais ou documentos dos autos, e bloqueia qualquer conteúdo coberto por segredo de justiça conforme regulamentação do CNJ. O uso é direcionado a transparência, pesquisa e automação respeitando termos de uso e salvaguardas legais de proteção de dados.[trf2**+1**](https://www.trf2.jus.br/trf2/noticia/2024/cnj-lanca-ferramenta-publica-que-universaliza-informacoes-sobre-processos)

## Portais e dados abertos correlatos

Diversos tribunais divulgam a própria página de “Dados Abertos” com referências e instruções para o consumo da API Pública do DataJud, incluindo links institucionais de acesso e apoio à numeração única de processos via painéis do CNJ. O STJ mantém um portal de dados abertos que cataloga o conjunto “API Pública – DataJud”, facilitando descoberta e acesso automatizado a partir do ecossistema de dados abertos do Judiciário.[dadosabertos.stj**+4**](https://dadosabertos.web.stj.jus.br/dataset/api-publica-datajud)

## APIs comerciais (não oficiais)

Há provedores privados que agregam, normalizam e enriquecem dados processuais e de diários oficiais, oferecendo busca por CPF/CNPJ/OAB, monitoramento com webhooks e, em alguns casos, acesso a documentos processuais, mediante contratação e chaves proprietárias. Exemplos incluem Judit, Escavador, Jusbrasil e Codilo, com escopos que podem abranger consulta processual ampla, alertas e integrações de compliance, porém não são APIs públicas do CNJ ou dos tribunais.[produto.judit**+5**](https://produto.judit.io/api)

## PJe/MNI e convênios

Serviços de interoperabilidade do PJe baseados no Modelo Nacional de Interoperabilidade (MNI) existem como webservices para integração sistêmica, mas exigem convênio formal com o tribunal e não são abertos para consumo público, além de não serem acessíveis diretamente por navegador. Esses serviços complementam integrações institucionais, enquanto a API Pública do DataJud é o canal oficial para acesso público a metadados processuais.[trt15**+1**](https://trt15.jus.br/transparencia/dados-abertos)

## Como começar

- Obter a APIKey pública vigente e revisar os termos de uso e escopo da API na documentação oficial do DataJud.[datajud-wiki.cnj**+1**](https://datajud-wiki.cnj.jus.br/api-publica/)
- Identificar o alias do tribunal desejado na lista oficial de endpoints e utilizar o recurso “\_search” com método POST.[datajud-wiki.cnj](https://datajud-wiki.cnj.jus.br/api-publica/endpoints/)
- Montar o cabeçalho com “Authorization: APIKey {chave}” e “Content-Type: application/json”, enviando o corpo de consulta conforme exemplos dos tribunais e da wiki.[trt24**+1**](https://www.trt24.jus.br/web/transparencia/acesso-automatizado-api)
- Validar resultados, paginação e limites operacionais conforme a documentação e orientações publicadas pelos tribunais e pelo CNJ.[datajud-wiki.cnj**+1**](https://datajud-wiki.cnj.jus.br/api-publica/)

1. [https://api.escavador.com/v1/docs/](https://api.escavador.com/v1/docs/)
2. [https://datajud-wiki.cnj.jus.br/api-publica/](https://datajud-wiki.cnj.jus.br/api-publica/)
3. [https://produto.judit.io/api](https://produto.judit.io/api)
4. [https://judit.io](https://judit.io/)
5. [https://www.trf2.jus.br/trf2/noticia/2024/cnj-lanca-ferramenta-publica-que-universaliza-informacoes-sobre-processos](https://www.trf2.jus.br/trf2/noticia/2024/cnj-lanca-ferramenta-publica-que-universaliza-informacoes-sobre-processos)
6. [https://api.escavador.com](https://api.escavador.com/)
7. [https://datajud-wiki.cnj.jus.br/api-publica/endpoints/](https://datajud-wiki.cnj.jus.br/api-publica/endpoints/)
8. [https://www.codilo.com.br](https://www.codilo.com.br/)
9. [https://insight.jusbrasil.com.br](https://insight.jusbrasil.com.br/)
10. [https://trt15.jus.br/transparencia/dados-abertos](https://trt15.jus.br/transparencia/dados-abertos)
11. [https://www.tjam.jus.br/index.php/transparencia/tecnologia-da-informacao-e-comunicacao/relatorios-dinamicos/numeracao-unica-e-consulta-via-api-do-datajud](https://www.tjam.jus.br/index.php/transparencia/tecnologia-da-informacao-e-comunicacao/relatorios-dinamicos/numeracao-unica-e-consulta-via-api-do-datajud)
12. [https://www.trt24.jus.br/web/transparencia/acesso-automatizado-api](https://www.trt24.jus.br/web/transparencia/acesso-automatizado-api)
13. [https://dadosabertos.web.stj.jus.br/dataset/api-publica-datajud](https://dadosabertos.web.stj.jus.br/dataset/api-publica-datajud)
14. [https://dadosabertos.web.stj.jus.br/dataset/?groups=consulta](https://dadosabertos.web.stj.jus.br/dataset/?groups=consulta)
15. [https://www.tjma.jus.br/midia/informatica/pagina/hotsite/508517](https://www.tjma.jus.br/midia/informatica/pagina/hotsite/508517)
16. [https://dadosabertos.web.stj.jus.br](https://dadosabertos.web.stj.jus.br/)
17. [https://ww2.trt2.jus.br/transparencia/resultados-e-indicadores/dados-estatisticos/acesso-a-dados-estatisticos-e-da-api-publica-do-datajud-cnj](https://ww2.trt2.jus.br/transparencia/resultados-e-indicadores/dados-estatisticos/acesso-a-dados-estatisticos-e-da-api-publica-do-datajud-cnj)
18. [https://dadosabertos.web.stj.jus.br/dataset/api-publica-datajud/resource/07bb3911-836e-4c11-865e-a94b1fc7bdda](https://dadosabertos.web.stj.jus.br/dataset/api-publica-datajud/resource/07bb3911-836e-4c11-865e-a94b1fc7bdda)
19. [https://www.tjmsp.jus.br/governanca-institucional/gestao-judiciaria/api-publica-datajud/](https://www.tjmsp.jus.br/governanca-institucional/gestao-judiciaria/api-publica-datajud/)
20. [https://www.youtube.com/watch?v=BoADSiUV-2o](https://www.youtube.com/watch?v=BoADSiUV-2o)
21. [https://judit.io/blog/artigos/api-judit-consultas-monitoramento-processos/](https://judit.io/blog/artigos/api-judit-consultas-monitoramento-processos/)
22. [https://www.tjpa.jus.br/PortalExterno/institucional/Gestao-Estatistica/978295-api-datajud.xhtml](https://www.tjpa.jus.br/PortalExterno/institucional/Gestao-Estatistica/978295-api-datajud.xhtml)
23. [https://dados.gov.br](https://dados.gov.br/)
24. [https://portaldatransparencia.gov.br/api-de-dados](https://portaldatransparencia.gov.br/api-de-dados)
25. [https://dados.gov.br/dados/conjuntos-dados/acervo-judiciario](https://dados.gov.br/dados/conjuntos-dados/acervo-judiciario)
26. [https://www.gov.br/conecta/catalogo/apis/api-portal-de-dados-abertos](https://www.gov.br/conecta/catalogo/apis/api-portal-de-dados-abertos)
27. [https://ww2.trt2.jus.br/transparencia/ranking-da-transparencia/dados-abertos](https://ww2.trt2.jus.br/transparencia/ranking-da-transparencia/dados-abertos)
28. [https://www.trt4.jus.br/portais/trt4/dados-abertos](https://www.trt4.jus.br/portais/trt4/dados-abertos)
