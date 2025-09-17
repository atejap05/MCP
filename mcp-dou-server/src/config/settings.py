"""
Configurações do servidor MCP DOU.

Este módulo gerencia todas as configurações do servidor,
incluindo credenciais, cache, logging e outros parâmetros.
"""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from ..models.dou_models import DOUServerConfig


class Settings(BaseSettings):
    """Configurações do servidor MCP DOU carregadas de variáveis de ambiente."""
    
    # Credenciais INLABS
    inlabs_email: str = "email@dominio.com"
    inlabs_password: str = "senha_exemplo"
    
    # Cache
    dou_cache_dir: str = "./cache"
    dou_max_cache_size: int = 1000
    dou_cache_ttl_hours: int = 24
    
    # Download
    dou_download_timeout: int = 30
    dou_max_concurrent_downloads: int = 5
    dou_retry_attempts: int = 3
    
    # Logging
    log_level: str = "INFO"
    log_file: Optional[str] = None
    
    # Server
    mcp_server_name: str = "dou"
    mcp_server_version: str = "0.1.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


def load_config() -> DOUServerConfig:
    """
    Carrega as configurações do servidor.
    
    Returns:
        DOUServerConfig: Configurações carregadas
    """
    # Carrega o arquivo .env se existir
    env_path = Path(".env")
    if env_path.exists():
        load_dotenv(env_path)
    
    settings = Settings()
    
    # Cria o diretório de cache se não existir
    cache_dir = Path(settings.dou_cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # Cria o diretório de logs se especificado
    if settings.log_file:
        log_path = Path(settings.log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
    
    return DOUServerConfig(
        inlabs_email=settings.inlabs_email,
        inlabs_password=settings.inlabs_password,
        cache_dir=str(cache_dir.absolute()),
        max_cache_size=settings.dou_max_cache_size,
        cache_ttl_hours=settings.dou_cache_ttl_hours,
        download_timeout=settings.dou_download_timeout,
        max_concurrent_downloads=settings.dou_max_concurrent_downloads,
        retry_attempts=settings.dou_retry_attempts,
        log_level=settings.log_level,
        log_file=settings.log_file,
        server_name=settings.mcp_server_name,
        server_version=settings.mcp_server_version,
    )


# Configuração global
config = load_config()


def get_config() -> DOUServerConfig:
    """
    Obtém a configuração global do servidor.
    
    Returns:
        DOUServerConfig: Configuração do servidor
    """
    return config


def update_config(**kwargs) -> DOUServerConfig:
    """
    Atualiza a configuração global.
    
    Args:
        **kwargs: Parâmetros a serem atualizados
        
    Returns:
        DOUServerConfig: Nova configuração
    """
    global config
    current_dict = config.dict()
    current_dict.update(kwargs)
    config = DOUServerConfig(**current_dict)
    return config