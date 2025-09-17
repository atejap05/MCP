"""
Modelos de dados para o servidor MCP DOU.

Este módulo define os modelos Pydantic para estruturar os dados
do Diário Oficial da União (DOU).
"""

from datetime import date as Date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, field_validator


class DOUSection(str, Enum):
    """Seções do Diário Oficial da União."""
    
    # Seções principais
    DO1 = "DO1"  # Seção 1 - Atos normativos
    DO2 = "DO2"  # Seção 2 - Atos de pessoal
    DO3 = "DO3"  # Seção 3 - Contratos e editais
    
    # Edições extras
    DO1E = "DO1E"  # Seção 1 - Edição extra
    DO2E = "DO2E"  # Seção 2 - Edição extra
    DO3E = "DO3E"  # Seção 3 - Edição extra


class FileFormat(str, Enum):
    """Formatos de arquivo disponíveis."""
    
    XML = "xml"
    PDF = "pdf"


class ArticleType(str, Enum):
    """Tipos de artigos/matérias do DOU."""
    
    PORTARIA = "Portaria"
    DECRETO = "Decreto"
    LEI = "Lei"
    RESOLUCAO = "Resolução"
    INSTRUCAO_NORMATIVA = "Instrução Normativa"
    AVISO = "Aviso"
    EDITAL = "Edital"
    EXTRATO = "Extrato"
    TERMO_ADITIVO = "Termo Aditivo"
    CONTRATO = "Contrato"
    CONVENIO = "Convênio"
    OUTROS = "Outros"


class DOUCredentials(BaseModel):
    """Credenciais para autenticação no sistema INLABS."""
    
    email: str = Field(..., description="Email de login no INLABS")
    password: str = Field(..., description="Senha do INLABS")
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if '@' not in v or '.' not in v:
            raise ValueError('Email inválido')
        return v


class DOUDownloadRequest(BaseModel):
    """Solicitação de download de arquivos do DOU."""
    
    date: Date = Field(..., description="Data da publicação (YYYY-MM-DD)")
    sections: List[DOUSection] = Field(
        default=[DOUSection.DO1, DOUSection.DO2, DOUSection.DO3],
        description="Seções do DOU para download"
    )
    file_format: FileFormat = Field(
        default=FileFormat.XML,
        description="Formato do arquivo (XML ou PDF)"
    )
    force_download: bool = Field(
        default=False,
        description="Forçar novo download mesmo se já existir no cache"
    )


class DOUSearchCriteria(BaseModel):
    """Critérios de busca no DOU."""
    
    text: Optional[str] = Field(None, description="Texto a ser buscado")
    start_date: Optional[Date] = Field(None, description="Data inicial")
    end_date: Optional[Date] = Field(None, description="Data final")
    sections: Optional[List[DOUSection]] = Field(None, description="Seções específicas")
    article_type: Optional[ArticleType] = Field(None, description="Tipo de artigo")
    organ: Optional[str] = Field(None, description="Órgão publicador")
    category: Optional[str] = Field(None, description="Categoria da matéria")
    limit: int = Field(default=100, description="Limite de resultados", ge=1, le=1000)


class DOUArticleMetadata(BaseModel):
    """Metadados de um artigo do DOU extraído do XML."""
    
    id: str = Field(..., description="ID único da matéria")
    name: str = Field(..., description="Nome da matéria")
    id_oficio: Optional[str] = Field(None, description="ID do ofício")
    pub_name: str = Field(..., description="Nome da sessão (DOU1, DOU2, DOU3)")
    art_type: Optional[str] = Field(None, description="Tipo da matéria")
    pub_date: str = Field(..., description="Data de publicação")
    art_class: Optional[str] = Field(None, description="Código de ordenação")
    art_category: Optional[str] = Field(None, description="Categoria completa")
    art_size: Optional[str] = Field(None, description="Largura da matéria")
    number_page: Optional[str] = Field(None, description="Número da página")
    pdf_page: Optional[str] = Field(None, description="URL da página PDF")
    edition_number: Optional[str] = Field(None, description="Número da edição")
    highlight_type: Optional[str] = Field(None, description="Tipo de destaque")
    id_materia: Optional[str] = Field(None, description="ID da matéria no Portal")


class DOUArticleContent(BaseModel):
    """Conteúdo de um artigo do DOU."""
    
    identifica: Optional[str] = Field(None, description="Identificação da norma")
    data: Optional[str] = Field(None, description="Data da matéria")
    ementa: Optional[str] = Field(None, description="Ementa")
    titulo: Optional[str] = Field(None, description="Título")
    subtitulo: Optional[str] = Field(None, description="Subtítulo")
    texto: str = Field(..., description="Conteúdo completo da matéria")


class DOUArticle(BaseModel):
    """Artigo completo do DOU com metadados e conteúdo."""
    
    metadata: DOUArticleMetadata
    content: DOUArticleContent
    raw_xml: Optional[str] = Field(None, description="XML original da matéria")
    extracted_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp da extração"
    )


class DOUFileInfo(BaseModel):
    """Informações sobre um arquivo do DOU."""
    
    filename: str = Field(..., description="Nome do arquivo")
    date: Date = Field(..., description="Data da publicação")
    section: DOUSection = Field(..., description="Seção do DOU")
    file_format: FileFormat = Field(..., description="Formato do arquivo")
    file_size: Optional[int] = Field(None, description="Tamanho do arquivo em bytes")
    file_path: Optional[str] = Field(None, description="Caminho local do arquivo")
    download_url: Optional[str] = Field(None, description="URL de download")
    is_cached: bool = Field(default=False, description="Se está em cache local")
    last_modified: Optional[datetime] = Field(None, description="Última modificação")


class DOUSearchResult(BaseModel):
    """Resultado de uma busca no DOU."""
    
    articles: List[DOUArticle] = Field(..., description="Artigos encontrados")
    total_count: int = Field(..., description="Total de artigos encontrados")
    search_criteria: DOUSearchCriteria = Field(..., description="Critérios utilizados")
    search_time_ms: float = Field(..., description="Tempo de busca em milissegundos")
    cached_results: bool = Field(default=False, description="Se os resultados vieram do cache")


class DOUStatistics(BaseModel):
    """Estatísticas sobre publicações do DOU."""
    
    date_range: Dict[str, Date] = Field(..., description="Intervalo de datas")
    total_publications: int = Field(..., description="Total de publicações")
    publications_by_section: Dict[DOUSection, int] = Field(
        ..., description="Publicações por seção"
    )
    publications_by_type: Dict[str, int] = Field(
        ..., description="Publicações por tipo"
    )
    publications_by_organ: Dict[str, int] = Field(
        ..., description="Publicações por órgão (top 20)"
    )
    cache_stats: Dict[str, Any] = Field(..., description="Estatísticas do cache")


class MCPToolResult(BaseModel):
    """Resultado de uma ferramenta MCP."""
    
    success: bool = Field(..., description="Se a operação foi bem-sucedida")
    message: str = Field(..., description="Mensagem de resultado")
    data: Optional[Any] = Field(None, description="Dados retornados")
    error: Optional[str] = Field(None, description="Mensagem de erro, se houver")
    execution_time_ms: float = Field(..., description="Tempo de execução")


class DOUServerConfig(BaseModel):
    """Configuração do servidor MCP DOU."""
    
    # Credenciais
    inlabs_email: str = Field(..., description="Email INLABS")
    inlabs_password: str = Field(..., description="Senha INLABS")
    
    # Cache
    cache_dir: str = Field(default="./cache", description="Diretório de cache")
    max_cache_size: int = Field(default=1000, description="Tamanho máximo do cache")
    cache_ttl_hours: int = Field(default=24, description="TTL do cache em horas")
    
    # Download
    download_timeout: int = Field(default=30, description="Timeout de download")
    max_concurrent_downloads: int = Field(
        default=5, description="Downloads simultâneos máximos"
    )
    retry_attempts: int = Field(default=3, description="Tentativas de retry")
    
    # Logging
    log_level: str = Field(default="INFO", description="Nível de log")
    log_file: Optional[str] = Field(None, description="Arquivo de log")
    
    # Server
    server_name: str = Field(default="dou", description="Nome do servidor MCP")
    server_version: str = Field(default="0.1.0", description="Versão do servidor")