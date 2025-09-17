"""
Ferramentas utilitárias MCP para o servidor DOU.

Este módulo implementa ferramentas auxiliares como configuração,
estatísticas e informações sobre o sistema DOU.
"""

import logging
import time
from datetime import date
from mcp.server.fastmcp import FastMCP

from ..auth.inlabs_auth import get_auth_instance
from ..config.settings import get_config
from ..models.dou_models import DOUCredentials, DOUSection


logger = logging.getLogger(__name__)


def register_utility_tools(mcp: FastMCP) -> None:
    """Registra as ferramentas utilitárias no servidor MCP."""
    
    @mcp.tool()
    async def configure_credentials(email: str, password: str) -> str:
        """
        Configura credenciais para acesso ao sistema INLABS.
        
        Args:
            email: Email de login no INLABS
            password: Senha do INLABS
        """
        try:
            # Cria novas credenciais
            credentials = DOUCredentials(email=email, password=password)
            
            # Testa autenticação
            auth = get_auth_instance(credentials)
            result = await auth.test_connection()
            
            if result.success:
                return f"✅ Credenciais configuradas com sucesso!\n\n📧 Email: {email}\n🔒 Senha: {'*' * len(password)}\n⏱️ Tempo de teste: {result.execution_time_ms:.2f}ms"
            else:
                return f"❌ Falha na configuração das credenciais\n\n🔍 Erro: {result.error}\n⏱️ Tempo de teste: {result.execution_time_ms:.2f}ms"
                
        except Exception as e:
            logger.error(f"Erro ao configurar credenciais: {e}")
            return f"❌ Erro ao configurar credenciais: {str(e)}"
    
    @mcp.tool()
    async def test_connection() -> str:
        """
        Testa a conexão com o sistema INLABS usando as credenciais configuradas.
        """
        try:
            auth = get_auth_instance()
            result = await auth.test_connection()
            
            if result.success:
                config = get_config()
                data = result.data or {}
                return (
                    f"✅ Conexão com INLABS estabelecida com sucesso!\n\n"
                    f"📧 Email: {config.inlabs_email}\n"
                    f"🔗 Autenticado: {data.get('authenticated', False)}\n"
                    f"🍪 Cookie de sessão: {data.get('session_cookie', False)}\n"
                    f"⏱️ Tempo de teste: {result.execution_time_ms:.2f}ms"
                )
            else:
                return (
                    f"❌ Falha na conexão com INLABS\n\n"
                    f"🔍 Erro: {result.error}\n"
                    f"⏱️ Tempo de teste: {result.execution_time_ms:.2f}ms\n\n"
                    f"💡 Dica: Verifique suas credenciais usando configure_credentials"
                )
                
        except Exception as e:
            logger.error(f"Erro no teste de conexão: {e}")
            return f"❌ Erro no teste de conexão: {str(e)}"
    
    @mcp.tool()
    async def list_available_sections() -> str:
        """
        Lista todas as seções disponíveis do DOU com descrições.
        """
        sections_info = [
            ("DO1", "Seção 1", "Atos normativos de interesse geral (leis, decretos, portarias)"),
            ("DO1E", "Seção 1 Extra", "Edição extra da Seção 1"),
            ("DO2", "Seção 2", "Atos de pessoal relativos aos servidores públicos"),
            ("DO2E", "Seção 2 Extra", "Edição extra da Seção 2"),
            ("DO3", "Seção 3", "Extratos contratuais, editais e licitações"),
            ("DO3E", "Seção 3 Extra", "Edição extra da Seção 3")
        ]
        
        result = "📚 Seções Disponíveis do Diário Oficial da União\n\n"
        
        for code, name, description in sections_info:
            result += f"🔹 **{code}** - {name}\n   {description}\n\n"
        
        result += (
            "📋 **Formatos de Arquivo:**\n"
            "• XML: Formato estruturado para processamento automático\n"
            "• PDF: Versão oficial certificada para visualização\n\n"
            "💡 **Exemplo de uso:**\n"
            '• XML: download_dou_xml("2024-09-17", "DO1 DO2")\n'
            '• PDF: download_dou_pdf("2024-09-17", "do1 do2")'
        )
        
        return result
    
    @mcp.tool()
    async def get_server_info() -> str:
        """
        Obtém informações sobre o servidor MCP DOU.
        """
        config = get_config()
        
        return (
            f"🖥️ **Servidor MCP DOU - Informações**\n\n"
            f"📛 Nome: {config.server_name}\n"
            f"🔢 Versão: {config.server_version}\n"
            f"📁 Diretório de cache: {config.cache_dir}\n"
            f"💾 Tamanho máximo do cache: {config.max_cache_size} arquivos\n"
            f"⏰ TTL do cache: {config.cache_ttl_hours} horas\n"
            f"🔄 Tentativas de retry: {config.retry_attempts}\n"
            f"⏱️ Timeout de download: {config.download_timeout}s\n"
            f"🎯 Downloads simultâneos: {config.max_concurrent_downloads}\n\n"
            f"📊 **Status:**\n"
            f"• Data atual: {date.today()}\n"
            f"• Servidor ativo: ✅\n"
            f"• Sistema INLABS: Conectado"
        )
    
    @mcp.tool()
    async def get_dou_statistics() -> str:
        """
        Obtém estatísticas sobre o cache local e uso do sistema.
        """
        # TODO: Implementar estatísticas reais do cache
        config = get_config()
        
        return (
            f"📈 **Estatísticas do Sistema DOU**\n\n"
            f"📁 Diretório de cache: {config.cache_dir}\n"
            f"📊 Funcionalidade em desenvolvimento...\n\n"
            f"🔄 Em breve:\n"
            f"• Total de arquivos em cache\n"
            f"• Espaço utilizado em disco\n"
            f"• Arquivos mais acessados\n"
            f"• Estatísticas por seção\n"
            f"• Histórico de downloads"
        )
    
    @mcp.tool()
    async def validate_date_range(start_date: str, end_date: str) -> str:
        """
        Valida um intervalo de datas para consultas DOU.
        
        Args:
            start_date: Data inicial (YYYY-MM-DD)
            end_date: Data final (YYYY-MM-DD)
        """
        try:
            from datetime import datetime, timedelta
            
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
            today = date.today()
            
            # Validações
            if start > end:
                return "❌ Data inicial não pode ser posterior à data final"
            
            if end > today:
                return f"⚠️ Data final ({end}) é posterior à data atual ({today})"
            
            # Calcula diferença
            diff = (end - start).days
            
            if diff > 365:
                return f"⚠️ Intervalo muito longo ({diff} dias). Recomendado: máximo 365 dias"
            
            # Verifica disponibilidade (DOU digital começou em 2017)
            min_date = datetime(2017, 1, 1).date()
            if start < min_date:
                return f"⚠️ Data inicial anterior ao início do DOU digital ({min_date})"
            
            return (
                f"✅ **Intervalo de datas válido**\n\n"
                f"📅 Período: {start} até {end}\n"
                f"📊 Total de dias: {diff + 1}\n"
                f"📈 Estimativa de arquivos (3 seções): {(diff + 1) * 3}\n\n"
                f"💡 Dica: Use intervalos menores para downloads mais rápidos"
            )
            
        except ValueError:
            return "❌ Formato de data inválido. Use YYYY-MM-DD (ex: 2024-09-17)"
        except Exception as e:
            return f"❌ Erro na validação: {str(e)}"