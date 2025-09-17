"""
Sistema de autenticação para INLABS (Imprensa Nacional).

Este módulo gerencia a autenticação segura com o sistema INLABS,
incluindo login, gerenciamento de sessão e renovação de tokens.
"""

import logging
import time
from typing import Dict, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..models.dou_models import DOUCredentials, MCPToolResult
from ..config.settings import get_config


class INLABSAuthenticationError(Exception):
    """Exceção para erros de autenticação INLABS."""
    pass


class INLABSAuth:
    """
    Classe para gerenciar autenticação com o sistema INLABS.
    
    Baseada nos scripts originais, mas com melhorias em:
    - Gerenciamento seguro de sessões
    - Retry automático em caso de falhas
    - Validação de credenciais
    - Cache de sessão
    """
    
    def __init__(self, credentials: Optional[DOUCredentials] = None):
        self.config = get_config()
        self.logger = logging.getLogger(__name__)
        
        # URLs do sistema INLABS
        self.login_url = "https://inlabs.in.gov.br/logar.php"
        self.base_url = "https://inlabs.in.gov.br"
        
        # Credenciais
        if credentials:
            self.credentials = credentials
        else:
            self.credentials = DOUCredentials(
                email=self.config.inlabs_email,
                password=self.config.inlabs_password
            )
        
        # Configuração da sessão HTTP
        self.session = requests.Session()
        self._setup_session()
        
        # Estado da autenticação
        self._authenticated = False
        self._auth_time = 0
        self._session_cookie = None
        
    def _setup_session(self) -> None:
        """Configura a sessão HTTP com retry e timeouts."""
        
        # Headers padrão
        self.session.headers.update({
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (compatible; MCP-DOU-Server/1.0)"
        })
        
        # Configuração de retry
        retry_strategy = Retry(
            total=self.config.retry_attempts,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    async def authenticate(self, force_refresh: bool = False) -> bool:
        """
        Realiza autenticação no sistema INLABS.
        
        Args:
            force_refresh: Força nova autenticação mesmo se já autenticado
            
        Returns:
            bool: True se autenticação foi bem-sucedida
            
        Raises:
            INLABSAuthenticationError: Se a autenticação falhar
        """
        
        # Verifica se já está autenticado e não precisa renovar
        if self._authenticated and not force_refresh and not self._needs_refresh():
            self.logger.debug("Já autenticado, usando sessão existente")
            return True
        
        self.logger.info("Iniciando autenticação INLABS")
        
        try:
            # Dados de login
            payload = {
                "email": self.credentials.email,
                "password": self.credentials.password
            }
            
            # Realiza login
            response = self.session.post(
                self.login_url,
                data=payload,
                timeout=self.config.download_timeout
            )
            
            response.raise_for_status()
            
            # Verifica se obteve o cookie de sessão
            session_cookie = self.session.cookies.get('inlabs_session_cookie')
            
            if not session_cookie:
                self.logger.error("Falha na autenticação: cookie de sessão não encontrado")
                raise INLABSAuthenticationError(
                    "Credenciais inválidas ou problema no servidor INLABS"
                )
            
            # Salva estado da autenticação
            self._session_cookie = session_cookie
            self._authenticated = True
            self._auth_time = time.time()
            
            self.logger.info("Autenticação INLABS realizada com sucesso")
            return True
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Erro de rede durante autenticação: {e}")
            raise INLABSAuthenticationError(f"Erro de conexão: {e}")
        
        except Exception as e:
            self.logger.error(f"Erro inesperado durante autenticação: {e}")
            raise INLABSAuthenticationError(f"Erro de autenticação: {e}")
    
    def _needs_refresh(self) -> bool:
        """Verifica se a sessão precisa ser renovada."""
        
        # Considera que a sessão expira em 4 horas (conservador)
        session_max_age = 4 * 3600  # 4 horas em segundos
        
        return (time.time() - self._auth_time) > session_max_age
    
    async def test_connection(self) -> MCPToolResult:
        """
        Testa a conexão com o sistema INLABS.
        
        Returns:
            MCPToolResult: Resultado do teste
        """
        start_time = time.time()
        
        try:
            # Tenta autenticar
            success = await self.authenticate()
            
            execution_time = (time.time() - start_time) * 1000
            
            if success:
                return MCPToolResult(
                    success=True,
                    message="Conexão com INLABS estabelecida com sucesso",
                    data={
                        "authenticated": True,
                        "session_cookie": bool(self._session_cookie),
                        "auth_time": self._auth_time
                    },
                    error=None,
                    execution_time_ms=execution_time
                )
            else:
                return MCPToolResult(
                    success=False,
                    message="Falha na conexão com INLABS",
                    data=None,
                    error="Não foi possível autenticar",
                    execution_time_ms=execution_time
                )
                
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            return MCPToolResult(
                success=False,
                message="Erro ao testar conexão com INLABS",
                data=None,
                error=str(e),
                execution_time_ms=execution_time
            )
    
    def get_authenticated_session(self) -> requests.Session:
        """
        Retorna uma sessão HTTP autenticada.
        
        Returns:
            requests.Session: Sessão HTTP configurada e autenticada
            
        Raises:
            INLABSAuthenticationError: Se não estiver autenticado
        """
        if not self._authenticated or not self._session_cookie:
            raise INLABSAuthenticationError("Não autenticado. Execute authenticate() primeiro.")
        
        return self.session
    
    def get_session_headers(self) -> Dict[str, str]:
        """
        Retorna headers HTTP com cookie de sessão.
        
        Returns:
            Dict[str, str]: Headers HTTP com autenticação
            
        Raises:
            INLABSAuthenticationError: Se não estiver autenticado
        """
        if not self._authenticated or not self._session_cookie:
            raise INLABSAuthenticationError("Não autenticado. Execute authenticate() primeiro.")
        
        return {
            'Cookie': f'inlabs_session_cookie={self._session_cookie}',
            'origem': '736372697074'  # Código específico do INLABS
        }
    
    def is_authenticated(self) -> bool:
        """
        Verifica se está autenticado.
        
        Returns:
            bool: True se autenticado
        """
        return self._authenticated and bool(self._session_cookie)
    
    def logout(self) -> None:
        """Realiza logout e limpa a sessão."""
        self._authenticated = False
        self._session_cookie = None
        self._auth_time = 0
        self.session.cookies.clear()
        self.logger.info("Logout realizado")


# Instância global de autenticação
_auth_instance: Optional[INLABSAuth] = None


def get_auth_instance(credentials: Optional[DOUCredentials] = None) -> INLABSAuth:
    """
    Obtém a instância global de autenticação INLABS.
    
    Args:
        credentials: Credenciais opcionais (usa configuração se não fornecidas)
        
    Returns:
        INLABSAuth: Instância de autenticação
    """
    global _auth_instance
    
    if _auth_instance is None or credentials is not None:
        _auth_instance = INLABSAuth(credentials)
    
    return _auth_instance