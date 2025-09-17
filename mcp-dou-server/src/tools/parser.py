"""
Ferramentas MCP para parsing de XML do DOU.

Este módulo implementa funcionalidades para extrair e estruturar
dados dos arquivos XML do Diário Oficial da União.
"""

import asyncio
import json
import logging
import time
import zipfile
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import aiofiles
from bs4 import BeautifulSoup, Tag
from lxml import etree
from mcp.server.fastmcp import FastMCP

from ..models.dou_models import (
    DOUArticle,
    DOUArticleContent,
    DOUArticleMetadata,
    DOUSection,
    FileFormat
)


logger = logging.getLogger(__name__)


class DOUXMLParser:
    """Parser para arquivos XML do DOU."""
    
    def __init__(self):
        self.encoding = 'utf-8'
    
    async def parse_zip_file(self, zip_path: str) -> List[DOUArticle]:
        """
        Parsea um arquivo ZIP contendo XMLs do DOU.
        
        Args:
            zip_path: Caminho para o arquivo ZIP
            
        Returns:
            List[DOUArticle]: Lista de artigos extraídos
        """
        articles = []
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_file:
                xml_files = [f for f in zip_file.namelist() if f.endswith('.xml')]
                
                for xml_file in xml_files:
                    try:
                        xml_content = zip_file.read(xml_file).decode(self.encoding)
                        article = await self.parse_xml_content(xml_content)
                        if article:
                            articles.append(article)
                    except Exception as e:
                        logger.error(f"Erro ao processar {xml_file}: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"Erro ao abrir ZIP {zip_path}: {e}")
            
        return articles
    
    async def parse_xml_content(self, xml_content: str) -> Optional[DOUArticle]:
        """
        Parsea o conteúdo XML de um artigo do DOU.
        
        Args:
            xml_content: Conteúdo XML como string
            
        Returns:
            DOUArticle: Artigo estruturado ou None se erro
        """
        try:
            # Parse com lxml para maior performance
            root = etree.fromstring(xml_content.encode(self.encoding))
            article_elem = root.find('.//article')
            
            if article_elem is None:
                logger.warning("Elemento 'article' não encontrado no XML")
                return None
            
            # Extrai metadados dos atributos
            metadata = self._extract_metadata(article_elem)
            
            # Extrai conteúdo do body
            content = self._extract_content(article_elem)
            
            return DOUArticle(
                metadata=metadata,
                content=content,
                raw_xml=xml_content,
                extracted_at=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Erro ao parsear XML: {e}")
            return None
    
    def _extract_metadata(self, article_elem) -> DOUArticleMetadata:
        """Extrai metadados do elemento article."""
        
        return DOUArticleMetadata(
            id=article_elem.get('id', ''),
            name=article_elem.get('name', ''),
            id_oficio=article_elem.get('idOficio'),
            pub_name=article_elem.get('pubName', ''),
            art_type=article_elem.get('artType'),
            pub_date=article_elem.get('pubDate', ''),
            art_class=article_elem.get('artClass'),
            art_category=article_elem.get('artCategory'),
            art_size=article_elem.get('artSize'),
            number_page=article_elem.get('numberPage'),
            pdf_page=article_elem.get('pdfPage'),
            edition_number=article_elem.get('editionNumber'),
            highlight_type=article_elem.get('highlightType'),
            id_materia=article_elem.get('idMateria')
        )
    
    def _extract_content(self, article_elem) -> DOUArticleContent:
        """Extrai conteúdo do elemento body."""
        
        body = article_elem.find('body')
        if body is None:
            return DOUArticleContent(texto="")
        
        def get_cdata_text(element_name: str) -> Optional[str]:
            """Extrai texto CDATA de um elemento."""
            elem = body.find(element_name)
            if elem is not None and elem.text:
                return elem.text.strip()
            return None
        
        # Remove tags HTML do texto principal para busca
        texto_elem = body.find('Texto')
        texto_clean = ""
        if texto_elem is not None and texto_elem.text:
            # Usa BeautifulSoup para limpar HTML
            soup = BeautifulSoup(texto_elem.text, 'html.parser')
            texto_clean = soup.get_text(separator=' ', strip=True)
        
        return DOUArticleContent(
            identifica=get_cdata_text('Identifica'),
            data=get_cdata_text('Data'),
            ementa=get_cdata_text('Ementa'),
            titulo=get_cdata_text('Titulo'),
            subtitulo=get_cdata_text('SubTitulo'),
            texto=texto_clean
        )


def register_parser_tools(mcp: FastMCP) -> None:
    """Registra as ferramentas de parsing no servidor MCP."""
    
    parser = DOUXMLParser()
    
    @mcp.tool()
    async def parse_xml_content(
        file_path: str,
        extract_metadata: bool = True,
        extract_content: bool = True
    ) -> str:
        """
        Extrai dados estruturados de um arquivo XML ou ZIP do DOU.
        
        Args:
            file_path: Caminho para o arquivo XML ou ZIP
            extract_metadata: Se deve extrair metadados
            extract_content: Se deve extrair conteúdo completo
        """
        start_time = time.time()
        
        try:
            file_path_obj = Path(file_path)
            
            if not file_path_obj.exists():
                return f"❌ Erro: Arquivo não encontrado: {file_path}"
            
            articles = []
            
            if file_path.endswith('.zip'):
                articles = await parser.parse_zip_file(file_path)
            elif file_path.endswith('.xml'):
                async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                    xml_content = await f.read()
                article = await parser.parse_xml_content(xml_content)
                if article:
                    articles = [article]
            else:
                return f"❌ Erro: Formato de arquivo não suportado. Use .xml ou .zip"
            
            execution_time = (time.time() - start_time) * 1000
            
            if not articles:
                return f"⚠️ Nenhum artigo encontrado no arquivo: {file_path}"
            
            # Formata resultado
            result = []
            result.append(f"📄 Parser XML DOU - {file_path_obj.name}")
            result.append(f"✅ Artigos processados: {len(articles)}")
            result.append(f"⏱️ Tempo de processamento: {execution_time:.2f}ms")
            result.append("")
            
            # Mostra primeiros artigos como exemplo
            for i, article in enumerate(articles[:3]):
                result.append(f"📋 Artigo {i+1}:")
                result.append(f"  ID: {article.metadata.id}")
                result.append(f"  Tipo: {article.metadata.art_type}")
                result.append(f"  Categoria: {article.metadata.art_category}")
                result.append(f"  Data: {article.metadata.pub_date}")
                if article.content.identifica:
                    result.append(f"  Identificação: {article.content.identifica[:100]}...")
                if article.content.ementa:
                    result.append(f"  Ementa: {article.content.ementa[:150]}...")
                result.append("")
            
            if len(articles) > 3:
                result.append(f"... e mais {len(articles) - 3} artigos.")
            
            return "\n".join(result)
            
        except Exception as e:
            logger.error(f"Erro no parsing: {e}")
            return f"❌ Erro ao processar arquivo: {str(e)}"
    
    @mcp.tool()
    async def extract_metadata(file_path: str) -> str:
        """
        Extrai apenas metadados de um arquivo XML do DOU.
        
        Args:
            file_path: Caminho para o arquivo XML ou ZIP
        """
        start_time = time.time()
        
        try:
            file_path_obj = Path(file_path)
            
            if not file_path_obj.exists():
                return f"❌ Erro: Arquivo não encontrado: {file_path}"
            
            articles = []
            
            if file_path.endswith('.zip'):
                articles = await parser.parse_zip_file(file_path)
            elif file_path.endswith('.xml'):
                async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                    xml_content = await f.read()
                article = await parser.parse_xml_content(xml_content)
                if article:
                    articles = [article]
            else:
                return f"❌ Erro: Formato de arquivo não suportado. Use .xml ou .zip"
            
            execution_time = (time.time() - start_time) * 1000
            
            if not articles:
                return f"⚠️ Nenhum artigo encontrado no arquivo: {file_path}"
            
            # Agrupa metadados por tipo e categoria
            stats = {
                'por_tipo': {},
                'por_categoria': {},
                'por_secao': {},
                'total': len(articles)
            }
            
            result = []
            result.append(f"📊 Metadados DOU - {file_path_obj.name}")
            result.append(f"📄 Total de artigos: {len(articles)}")
            result.append(f"⏱️ Tempo de processamento: {execution_time:.2f}ms")
            result.append("")
            
            # Estatísticas
            for article in articles:
                # Por tipo
                tipo = article.metadata.art_type or 'Não informado'
                stats['por_tipo'][tipo] = stats['por_tipo'].get(tipo, 0) + 1
                
                # Por categoria (primeiro nível)
                categoria = article.metadata.art_category or 'Não informado'
                categoria_principal = categoria.split('/')[0] if '/' in categoria else categoria
                stats['por_categoria'][categoria_principal] = stats['por_categoria'].get(categoria_principal, 0) + 1
                
                # Por seção
                secao = article.metadata.pub_name or 'Não informado'
                stats['por_secao'][secao] = stats['por_secao'].get(secao, 0) + 1
            
            # Mostra estatísticas
            result.append("📈 Distribuição por Tipo:")
            for tipo, count in sorted(stats['por_tipo'].items(), key=lambda x: x[1], reverse=True)[:5]:
                result.append(f"  {tipo}: {count}")
            result.append("")
            
            result.append("📂 Distribuição por Categoria:")
            for categoria, count in sorted(stats['por_categoria'].items(), key=lambda x: x[1], reverse=True)[:5]:
                result.append(f"  {categoria}: {count}")
            result.append("")
            
            result.append("📑 Distribuição por Seção:")
            for secao, count in stats['por_secao'].items():
                result.append(f"  {secao}: {count}")
            
            return "\n".join(result)
            
        except Exception as e:
            logger.error(f"Erro na extração de metadados: {e}")
            return f"❌ Erro ao extrair metadados: {str(e)}"