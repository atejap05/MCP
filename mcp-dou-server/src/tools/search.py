"""
Ferramentas MCP para busca e consulta no DOU.

Este módulo implementa funcionalidades de busca no conteúdo
dos arquivos do Diário Oficial da União.
"""

import glob
import logging
import re
import time
from datetime import datetime, date
from pathlib import Path
from typing import List, Dict, Optional, Tuple

from mcp.server.fastmcp import FastMCP

from ..config.settings import get_config
from ..models.dou_models import DOUArticle, DOUSection
from .parser import DOUXMLParser


logger = logging.getLogger(__name__)


class DOUSearchEngine:
    """Motor de busca para conteúdo DOU."""
    
    def __init__(self):
        self.parser = DOUXMLParser()
        self.config = get_config()
    
    async def search_content(
        self,
        query: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        sections: Optional[List[str]] = None,
        publication_type: Optional[str] = None,
        organ: Optional[str] = None,
        max_results: int = 100
    ) -> Tuple[List[DOUArticle], Dict]:
        """
        Busca no conteúdo com filtros.
        
        Args:
            query: Texto a ser buscado
            start_date: Data inicial (YYYY-MM-DD)
            end_date: Data final (YYYY-MM-DD)
            sections: Lista de seções (DO1, DO2, DO3)
            publication_type: Tipo de publicação
            organ: Nome do órgão
            max_results: Limite máximo de resultados
            
        Returns:
            Tuple[List[DOUArticle], Dict]: Artigos encontrados e estatísticas
        """
        found_articles = []
        stats = {
            'files_searched': 0,
            'articles_processed': 0,
            'matches_found': 0,
            'search_time_ms': 0
        }
        
        start_time = time.time()
        
        try:
            # Encontra arquivos ZIP na estrutura de cache
            zip_files = self._find_zip_files(start_date, end_date, sections)
            
            for zip_file in zip_files:
                stats['files_searched'] += 1
                
                # Parsea arquivo ZIP
                articles = await self.parser.parse_zip_file(str(zip_file))
                stats['articles_processed'] += len(articles)
                
                # Aplica filtros e busca
                for article in articles:
                    if self._matches_filters(article, query, publication_type, organ):
                        found_articles.append(article)
                        stats['matches_found'] += 1
                        
                        if len(found_articles) >= max_results:
                            break
                
                if len(found_articles) >= max_results:
                    break
            
            stats['search_time_ms'] = (time.time() - start_time) * 1000
            
        except Exception as e:
            logger.error(f"Erro na busca: {e}")
            stats['error'] = str(e)
        
        return found_articles, stats
    
    def _find_zip_files(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        sections: Optional[List[str]] = None
    ) -> List[Path]:
        """Encontra arquivos ZIP baseado nos filtros de data e seção."""
        
        cache_dir = Path(self.config.cache_dir)
        zip_files = []
        
        # Se não há filtros de data, busca todos os ZIPs
        if not start_date and not end_date:
            pattern = str(cache_dir / "**" / "*.zip")
            zip_files = [Path(f) for f in glob.glob(pattern, recursive=True)]
        else:
            # Busca por intervalos de data
            start_dt = datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else date(2020, 1, 1)
            end_dt = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else date.today()
            
            # Varre diretórios de ano/mês
            for year_dir in cache_dir.iterdir():
                if not year_dir.is_dir() or not year_dir.name.isdigit():
                    continue
                
                year = int(year_dir.name)
                
                for month_dir in year_dir.iterdir():
                    if not month_dir.is_dir() or not month_dir.name.isdigit():
                        continue
                    
                    month = int(month_dir.name)
                    
                    # Busca ZIPs neste mês
                    for zip_file in month_dir.glob("*.zip"):
                        # Extrai data do nome do arquivo
                        match = re.match(r'(\d{4}-\d{2}-\d{2})-', zip_file.name)
                        if match:
                            file_date = datetime.strptime(match.group(1), "%Y-%m-%d").date()
                            
                            if start_dt <= file_date <= end_dt:
                                # Filtra por seção se especificado
                                if sections:
                                    for section in sections:
                                        if section in zip_file.name:
                                            zip_files.append(zip_file)
                                            break
                                else:
                                    zip_files.append(zip_file)
        
        return sorted(zip_files)
    
    def _matches_filters(
        self,
        article: DOUArticle,
        query: str,
        publication_type: Optional[str] = None,
        organ: Optional[str] = None
    ) -> bool:
        """Verifica se um artigo atende aos filtros de busca."""
        
        # Filtro por tipo de publicação
        if publication_type:
            if not article.metadata.art_type:
                return False
            if publication_type.lower() not in article.metadata.art_type.lower():
                return False
        
        # Filtro por órgão
        if organ:
            if not article.metadata.art_category:
                return False
            if organ.lower() not in article.metadata.art_category.lower():
                return False
        
        # Busca textual (case-insensitive)
        if query:
            query_lower = query.lower()
            
            # Busca em todos os campos de texto
            search_fields = [
                article.content.identifica or "",
                article.content.ementa or "",
                article.content.titulo or "",
                article.content.subtitulo or "",
                article.content.texto or "",
                article.metadata.name or "",
                article.metadata.art_category or ""
            ]
            
            text_to_search = " ".join(search_fields).lower()
            
            # Busca simples por substring
            if query_lower not in text_to_search:
                return False
        
        return True


def register_search_tools(mcp: FastMCP) -> None:
    """Registra as ferramentas de busca no servidor MCP."""
    
    search_engine = DOUSearchEngine()
    
    @mcp.tool()
    async def search_dou_content(
        query: str,
        start_date: str = "",
        end_date: str = "",
        sections: str = "DO1 DO2 DO3",
        publication_type: str = "",
        organ: str = "",
        max_results: int = 50
    ) -> str:
        """
        Busca por conteúdo específico nos arquivos DOU baixados.
        
        Args:
            query: Texto a ser buscado (ex: "Receita Federal do Brasil")
            start_date: Data inicial (YYYY-MM-DD, opcional)
            end_date: Data final (YYYY-MM-DD, opcional)
            sections: Seções a serem pesquisadas (ex: "DO1 DO2 DO3")
            publication_type: Tipo de publicação (ex: "Portaria", "Decreto")
            organ: Nome do órgão (ex: "Receita Federal")
            max_results: Número máximo de resultados (padrão: 50)
        """
        start_time = time.time()
        
        try:
            # Prepara parâmetros
            sections_list = [s.strip() for s in sections.split()] if sections else None
            start_date_param = start_date if start_date else None
            end_date_param = end_date if end_date else None
            publication_type_param = publication_type if publication_type else None
            organ_param = organ if organ else None
            
            # Executa busca
            articles, stats = await search_engine.search_content(
                query=query,
                start_date=start_date_param,
                end_date=end_date_param,
                sections=sections_list,
                publication_type=publication_type_param,
                organ=organ_param,
                max_results=max_results
            )
            
            execution_time = (time.time() - start_time) * 1000
            
            # Formata resultado
            result = []
            result.append(f"🔍 Busca DOU: \"{query}\"")
            result.append(f"📅 Período: {start_date or 'início'} até {end_date or 'hoje'}")
            result.append(f"📑 Seções: {sections}")
            if publication_type:
                result.append(f"📋 Tipo: {publication_type}")
            if organ:
                result.append(f"🏛️ Órgão: {organ}")
            result.append("")
            
            result.append(f"📊 Estatísticas:")
            result.append(f"  Arquivos pesquisados: {stats['files_searched']}")
            result.append(f"  Artigos analisados: {stats['articles_processed']}")
            result.append(f"  Resultados encontrados: {stats['matches_found']}")
            result.append(f"  Tempo de busca: {stats['search_time_ms']:.2f}ms")
            result.append(f"  Tempo total: {execution_time:.2f}ms")
            result.append("")
            
            if not articles:
                result.append("❌ Nenhum resultado encontrado.")
                result.append("")
                result.append("💡 Dicas:")
                result.append("  - Verifique se há arquivos baixados para o período")
                result.append("  - Tente termos de busca mais simples")
                result.append("  - Remova filtros muito restritivos")
            else:
                result.append(f"✅ Mostrando {min(len(articles), 10)} primeiros resultados:")
                result.append("")
                
                # Mostra os primeiros resultados
                for i, article in enumerate(articles[:10]):
                    result.append(f"📄 Resultado {i+1}:")
                    result.append(f"  ID: {article.metadata.id}")
                    result.append(f"  Tipo: {article.metadata.art_type or 'Não informado'}")
                    result.append(f"  Data: {article.metadata.pub_date}")
                    result.append(f"  Seção: {article.metadata.pub_name}")
                    
                    if article.content.identifica:
                        result.append(f"  Identificação: {article.content.identifica[:150]}...")
                    
                    if article.content.ementa:
                        result.append(f"  Ementa: {article.content.ementa[:200]}...")
                    
                    # Destaca termo buscado no texto
                    if article.content.texto and query:
                        texto = article.content.texto
                        query_pos = texto.lower().find(query.lower())
                        if query_pos >= 0:
                            start = max(0, query_pos - 100)
                            end = min(len(texto), query_pos + len(query) + 100)
                            excerpt = texto[start:end]
                            if start > 0:
                                excerpt = "..." + excerpt
                            if end < len(texto):
                                excerpt = excerpt + "..."
                            result.append(f"  Trecho: {excerpt}")
                    
                    result.append("")
                
                if len(articles) > 10:
                    result.append(f"... e mais {len(articles) - 10} resultados.")
            
            return "\n".join(result)
            
        except Exception as e:
            logger.error(f"Erro na busca: {e}")
            return f"❌ Erro ao executar busca: {str(e)}"
    
    @mcp.tool()
    async def list_publications(
        date_str: str,
        publication_type: str = "",
        organ: str = "",
        sections: str = "DO1 DO2 DO3"
    ) -> str:
        """
        Lista publicações por data, tipo ou órgão.
        
        Args:
            date_str: Data no formato YYYY-MM-DD
            publication_type: Tipo de publicação (portaria, decreto, etc)
            organ: Nome do órgão
            sections: Seções a pesquisar (ex: "DO1 DO2 DO3")
        """
        start_time = time.time()
        
        try:
            # Usa a busca sem query para listar tudo
            sections_list = [s.strip() for s in sections.split()] if sections else None
            publication_type_param = publication_type if publication_type else None
            organ_param = organ if organ else None
            
            articles, stats = await search_engine.search_content(
                query="",  # Sem filtro de texto
                start_date=date_str,
                end_date=date_str,
                sections=sections_list,
                publication_type=publication_type_param,
                organ=organ_param,
                max_results=200
            )
            
            execution_time = (time.time() - start_time) * 1000
            
            # Agrupa por tipo e órgão
            by_type = {}
            by_organ = {}
            
            for article in articles:
                # Por tipo
                tipo = article.metadata.art_type or "Não informado"
                by_type[tipo] = by_type.get(tipo, 0) + 1
                
                # Por órgão (primeiro nível da categoria)
                categoria = article.metadata.art_category or "Não informado"
                orgao = categoria.split('/')[0] if '/' in categoria else categoria
                by_organ[orgao] = by_organ.get(orgao, 0) + 1
            
            # Formata resultado
            result = []
            result.append(f"📋 Publicações DOU - {date_str}")
            result.append(f"📑 Seções: {sections}")
            if publication_type:
                result.append(f"📋 Filtro por tipo: {publication_type}")
            if organ:
                result.append(f"🏛️ Filtro por órgão: {organ}")
            result.append("")
            
            result.append(f"📊 Resumo:")
            result.append(f"  Total de publicações: {len(articles)}")
            result.append(f"  Arquivos analisados: {stats['files_searched']}")
            result.append(f"  Tempo de processamento: {execution_time:.2f}ms")
            result.append("")
            
            if not articles:
                result.append("❌ Nenhuma publicação encontrada para esta data.")
            else:
                # Distribuição por tipo
                result.append("📈 Distribuição por Tipo:")
                for tipo, count in sorted(by_type.items(), key=lambda x: x[1], reverse=True)[:10]:
                    result.append(f"  {tipo}: {count}")
                result.append("")
                
                # Distribuição por órgão
                result.append("🏛️ Distribuição por Órgão:")
                for orgao, count in sorted(by_organ.items(), key=lambda x: x[1], reverse=True)[:10]:
                    result.append(f"  {orgao}: {count}")
                result.append("")
                
                # Lista algumas publicações como exemplo
                result.append("📄 Exemplos de publicações:")
                for i, article in enumerate(articles[:5]):
                    result.append(f"  {i+1}. {article.metadata.art_type or 'Tipo não informado'}")
                    result.append(f"     {article.content.identifica or 'Sem identificação'}")
                    if article.content.ementa:
                        result.append(f"     {article.content.ementa[:100]}...")
                    result.append("")
                
                if len(articles) > 5:
                    result.append(f"... e mais {len(articles) - 5} publicações.")
            
            return "\n".join(result)
            
        except Exception as e:
            logger.error(f"Erro na listagem: {e}")
            return f"❌ Erro ao listar publicações: {str(e)}"