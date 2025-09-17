"""
Ferramentas MCP para download de arquivos do DOU.

Este módulo implementa as ferramentas para baixar arquivos XML e PDF
do Diário Oficial da União através do sistema INLABS.
"""

import asyncio
import logging
import os
import time
from datetime import date, datetime
from pathlib import Path
from typing import List, Optional

import aiofiles
import httpx
from mcp.server.fastmcp import FastMCP

from ..auth.inlabs_auth import get_auth_instance, INLABSAuthenticationError
from ..config.settings import get_config
from ..models.dou_models import (
    DOUDownloadRequest,
    DOUFileInfo,
    DOUSection,
    FileFormat,
    MCPToolResult
)


logger = logging.getLogger(__name__)


async def download_file_from_url(
    url: str,
    file_path: Path,
    headers: dict,
    timeout: int = 30
) -> bool:
    """
    Baixa um arquivo de uma URL usando httpx assíncrono.
    
    Args:
        url: URL para download
        file_path: Caminho onde salvar o arquivo
        headers: Headers HTTP
        timeout: Timeout em segundos
        
    Returns:
        bool: True se download foi bem-sucedido
    """
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url, headers=headers)
            
            if response.status_code == 200:
                # Garante que o diretório existe
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                async with aiofiles.open(file_path, 'wb') as f:
                    await f.write(response.content)
                
                logger.info(f"Arquivo baixado: {file_path}")
                return True
            elif response.status_code == 404:
                logger.warning(f"Arquivo não encontrado: {url}")
                return False
            else:
                logger.error(f"Erro HTTP {response.status_code} ao baixar: {url}")
                return False
                
    except Exception as e:
        logger.error(f"Erro ao baixar arquivo {url}: {e}")
        return False


def build_download_url(
    base_date: date,
    section: DOUSection,
    file_format: FileFormat
) -> str:
    """
    Constrói URL de download baseada na data, seção e formato.
    
    Args:
        base_date: Data da publicação
        section: Seção do DOU
        file_format: Formato do arquivo (XML ou PDF)
        
    Returns:
        str: URL de download
    """
    base_url = "https://inlabs.in.gov.br/index.php?p="
    
    # Formata data
    date_str = base_date.strftime("%Y-%m-%d")
    
    if file_format == FileFormat.XML:
        # Para XML: formato YYYY-MM-DD-SECAO.zip
        filename = f"{date_str}-{section.value}.zip"
        url = f"{base_url}{date_str}&dl={filename}"
    else:
        # Para PDF: formato YYYY_MM_DD_ASSINADO_secao.pdf
        date_pdf = base_date.strftime("%Y_%m_%d")
        section_lower = section.value.lower().replace('e', '')  # DO1E -> do1
        filename = f"{date_pdf}_ASSINADO_{section_lower}.pdf"
        url = f"{base_url}{date_str}&dl={filename}"
    
    return url


def get_local_file_path(
    base_date: date,
    section: DOUSection,
    file_format: FileFormat,
    cache_dir: str
) -> Path:
    """
    Gera caminho local para arquivo baseado na data, seção e formato.
    
    Args:
        base_date: Data da publicação
        section: Seção do DOU
        file_format: Formato do arquivo
        cache_dir: Diretório de cache
        
    Returns:
        Path: Caminho local do arquivo
    """
    date_str = base_date.strftime("%Y-%m-%d")
    
    if file_format == FileFormat.XML:
        filename = f"{date_str}-{section.value}.zip"
    else:
        filename = f"{date_str}-{section.value}.pdf"
    
    return Path(cache_dir) / str(base_date.year) / f"{base_date.month:02d}" / filename


async def download_dou_file(
    base_date: date,
    section: DOUSection,
    file_format: FileFormat,
    force_download: bool = False
) -> DOUFileInfo:
    """
    Baixa um arquivo específico do DOU.
    
    Args:
        base_date: Data da publicação
        section: Seção do DOU
        file_format: Formato do arquivo
        force_download: Forçar novo download
        
    Returns:
        DOUFileInfo: Informações do arquivo baixado
    """
    config = get_config()
    auth = get_auth_instance()
    
    # Autentica se necessário
    if not auth.is_authenticated():
        await auth.authenticate()
    
    # Determina caminho local
    file_path = get_local_file_path(base_date, section, file_format, config.cache_dir)
    
    # Verifica se arquivo já existe e não deve forçar download
    if file_path.exists() and not force_download:
        logger.info(f"Arquivo já existe em cache: {file_path}")
        return DOUFileInfo(
            filename=file_path.name,
            date=base_date,
            section=section,
            file_format=file_format,
            file_size=file_path.stat().st_size,
            file_path=str(file_path),
            is_cached=True,
            last_modified=datetime.fromtimestamp(file_path.stat().st_mtime)
        )
    
    # Constrói URL e faz download
    download_url = build_download_url(base_date, section, file_format)
    headers = auth.get_session_headers()
    
    success = await download_file_from_url(
        download_url,
        file_path,
        headers,
        config.download_timeout
    )
    
    if success and file_path.exists():
        return DOUFileInfo(
            filename=file_path.name,
            date=base_date,
            section=section,
            file_format=file_format,
            file_size=file_path.stat().st_size,
            file_path=str(file_path),
            download_url=download_url,
            is_cached=False,
            last_modified=datetime.now()
        )
    else:
        # Retorna info mesmo se download falhou
        return DOUFileInfo(
            filename=f"{base_date}-{section.value}.{file_format.value}",
            date=base_date,
            section=section,
            file_format=file_format,
            download_url=download_url,
            is_cached=False
        )


def register_download_tools(mcp: FastMCP) -> None:
    """Registra as ferramentas de download no servidor MCP."""
    
    @mcp.tool()
    async def download_dou_xml(
        date_str: str,
        sections: Optional[str] = "DO1 DO2 DO3",
        force_download: bool = False
    ) -> str:
        """
        Baixa arquivos XML do DOU para uma data específica.
        
        Args:
            date_str: Data no formato YYYY-MM-DD (ex: 2024-09-17)
            sections: Seções separadas por espaço (ex: "DO1 DO2 DO3" ou "DO1E DO2E")
            force_download: Forçar novo download mesmo se arquivo existir
        """
        start_time = time.time()
        
        try:
            # Valida e converte data
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            
            # Processa seções
            section_list = [DOUSection(s.strip()) for s in sections.split()]
            
            # Autentica
            auth = get_auth_instance()
            await auth.authenticate()
            
            results = []
            successful_downloads = 0
            
            # Download de cada seção
            for section in section_list:
                try:
                    file_info = await download_dou_file(
                        target_date,
                        section,
                        FileFormat.XML,
                        force_download
                    )
                    
                    if file_info.file_path and Path(file_info.file_path).exists():
                        successful_downloads += 1
                        status = "✅ Sucesso"
                        details = f"Tamanho: {file_info.file_size} bytes"
                    else:
                        status = "❌ Não encontrado"
                        details = "Arquivo não disponível para esta data"
                    
                    results.append(
                        f"Seção {section.value}: {status}\n"
                        f"  Arquivo: {file_info.filename}\n"
                        f"  {details}"
                    )
                    
                except Exception as e:
                    logger.error(f"Erro ao baixar seção {section}: {e}")
                    results.append(f"Seção {section.value}: ❌ Erro - {str(e)}")
            
            execution_time = (time.time() - start_time) * 1000
            
            summary = (
                f"📥 Download DOU XML - {date_str}\n\n"
                f"✅ Downloads bem-sucedidos: {successful_downloads}/{len(section_list)}\n"
                f"⏱️ Tempo de execução: {execution_time:.2f}ms\n\n"
                f"📋 Resultados detalhados:\n" +
                "\n\n".join(results)
            )
            
            return summary
            
        except ValueError:
            return "❌ Erro: Data inválida. Use formato YYYY-MM-DD (ex: 2024-09-17)"
        except Exception as e:
            logger.error(f"Erro no download XML: {e}")
            return f"❌ Erro: {str(e)}"
    
    @mcp.tool()
    async def download_dou_pdf(
        date_str: str,
        sections: Optional[str] = "do1 do2 do3",
        force_download: bool = False
    ) -> str:
        """
        Baixa arquivos PDF do DOU para uma data específica.
        
        Args:
            date_str: Data no formato YYYY-MM-DD (ex: 2024-09-17)
            sections: Seções separadas por espaço (ex: "do1 do2 do3")
            force_download: Forçar novo download mesmo se arquivo existir
        """
        start_time = time.time()
        
        try:
            # Valida e converte data
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            
            # Mapeia seções PDF para enum
            section_map = {"do1": DOUSection.DO1, "do2": DOUSection.DO2, "do3": DOUSection.DO3}
            
            try:
                section_list = [section_map[s.strip().lower()] for s in sections.split()]
            except KeyError as e:
                return f"❌ Erro: Seção inválida {e}. Use: do1, do2, do3"
            
            # Autentica
            auth = get_auth_instance()
            await auth.authenticate()
            
            results = []
            successful_downloads = 0
            
            # Download de cada seção
            for section in section_list:
                try:
                    file_info = await download_dou_file(
                        target_date,
                        section,
                        FileFormat.PDF,
                        force_download
                    )
                    
                    if file_info.file_path and Path(file_info.file_path).exists():
                        successful_downloads += 1
                        status = "✅ Sucesso"
                        details = f"Tamanho: {file_info.file_size} bytes"
                    else:
                        status = "❌ Não encontrado"
                        details = "Arquivo não disponível para esta data"
                    
                    results.append(
                        f"Seção {section.value}: {status}\n"
                        f"  Arquivo: {file_info.filename}\n"
                        f"  {details}"
                    )
                    
                except Exception as e:
                    logger.error(f"Erro ao baixar seção {section}: {e}")
                    results.append(f"Seção {section.value}: ❌ Erro - {str(e)}")
            
            execution_time = (time.time() - start_time) * 1000
            
            summary = (
                f"📄 Download DOU PDF - {date_str}\n\n"
                f"✅ Downloads bem-sucedidos: {successful_downloads}/{len(section_list)}\n"
                f"⏱️ Tempo de execução: {execution_time:.2f}ms\n\n"
                f"📋 Resultados detalhados:\n" +
                "\n\n".join(results)
            )
            
            return summary
            
        except ValueError:
            return "❌ Erro: Data inválida. Use formato YYYY-MM-DD (ex: 2024-09-17)"
        except Exception as e:
            logger.error(f"Erro no download PDF: {e}")
            return f"❌ Erro: {str(e)}"
    
    @mcp.tool()
    async def check_file_availability(
        date_str: str,
        sections: Optional[str] = "DO1 DO2 DO3",
        file_format: str = "xml"
    ) -> str:
        """
        Verifica disponibilidade de arquivos DOU sem baixá-los.
        
        Args:
            date_str: Data no formato YYYY-MM-DD (ex: 2024-09-17)
            sections: Seções separadas por espaço (ex: "DO1 DO2 DO3")
            file_format: Formato do arquivo ("xml" ou "pdf")
        """
        start_time = time.time()
        
        try:
            # Valida parâmetros
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            format_enum = FileFormat.XML if file_format.lower() == "xml" else FileFormat.PDF
            
            section_list = [DOUSection(s.strip()) for s in sections.split()]
            
            # Autentica
            auth = get_auth_instance()
            await auth.authenticate()
            
            results = []
            available_count = 0
            
            # Verifica cada seção
            for section in section_list:
                try:
                    download_url = build_download_url(target_date, section, format_enum)
                    headers = auth.get_session_headers()
                    
                    # Faz apenas um HEAD request para verificar
                    async with httpx.AsyncClient() as client:
                        response = await client.head(download_url, headers=headers)
                    
                    if response.status_code == 200:
                        available_count += 1
                        status = "✅ Disponível"
                        size = response.headers.get('content-length', 'Desconhecido')
                        details = f"Tamanho: {size} bytes" if size != 'Desconhecido' else "Tamanho: Não informado"
                    elif response.status_code == 404:
                        status = "❌ Não disponível"
                        details = "Arquivo não encontrado no servidor"
                    else:
                        status = "⚠️ Incerto"
                        details = f"Status HTTP: {response.status_code}"
                    
                    results.append(
                        f"Seção {section.value}: {status}\n"
                        f"  URL: {download_url}\n"
                        f"  {details}"
                    )
                    
                except Exception as e:
                    logger.error(f"Erro ao verificar seção {section}: {e}")
                    results.append(f"Seção {section.value}: ❌ Erro - {str(e)}")
            
            execution_time = (time.time() - start_time) * 1000
            
            summary = (
                f"🔍 Verificação DOU {format_enum.value.upper()} - {date_str}\n\n"
                f"✅ Arquivos disponíveis: {available_count}/{len(section_list)}\n"
                f"⏱️ Tempo de verificação: {execution_time:.2f}ms\n\n"
                f"📋 Resultados detalhados:\n" +
                "\n\n".join(results)
            )
            
            return summary
            
        except ValueError:
            return "❌ Erro: Data inválida. Use formato YYYY-MM-DD (ex: 2024-09-17)"
        except Exception as e:
            logger.error(f"Erro na verificação: {e}")
            return f"❌ Erro: {str(e)}"