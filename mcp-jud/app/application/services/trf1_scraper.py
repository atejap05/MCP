import logging
import re
from typing import Dict, List, Optional

import bs4
import httpx

from app.core.config import LOGGER_NAME, TRF1_BASE_URLS, TRF1_CONSULTA_URLS

logger = logging.getLogger(LOGGER_NAME)

REGEX_EVENT = re.compile(r":processoEvento:\d+:[^:]+$")


class TRF1Scraper:
    """Scraper para consultar processos no TRF1."""

    def __init__(self):
        self.base_urls = TRF1_BASE_URLS
        self.consulta_urls = TRF1_CONSULTA_URLS

    async def get_all_events(self, numero_processo: str, grau: str = "G1") -> List[str]:
        """
        Obtém todos os andamentos de um processo.

        Args:
            numero_processo: Número do processo no formato CNJ
            grau: Grau do processo (G1 ou G2)

        Returns:
            Lista de strings com os andamentos formatados
        """
        try:
            logger.info(f"Consultando processo {numero_processo} grau {grau}")

            # Obter página inicial
            consulta_url = self.consulta_urls.get(grau, self.consulta_urls["G1"])
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(consulta_url)
                response.raise_for_status()

                # Extrair ViewState
                viewstate = self._get_viewstate(response.text)

                # Preparar dados do formulário
                form_data = self._prepare_form_data(numero_processo, viewstate)

                # Headers
                headers = {
                    "Faces-Request": "partial/ajax",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
                    "Referer": consulta_url
                }

                # Fazer requisição de busca
                logger.info("Fazendo requisição de busca")
                response = await client.post(
                    consulta_url,
                    data=form_data,
                    headers=headers
                )
                response.raise_for_status()

                # Extrair URL do processo
                processo_url = self._extract_processo_url(response.text)
                if not processo_url:
                    return []

                # Acessar página do processo
                logger.info(f"Acessando página do processo: {processo_url}")
                response = await client.get(processo_url)
                response.raise_for_status()

                # Extrair andamentos
                andamentos = self._extract_andamentos(response.text)
                return andamentos

        except Exception as e:
            logger.error(f"Erro ao consultar processo {numero_processo}: {str(e)}")
            return []

    def _get_viewstate(self, html: str) -> str:
        """Extrai o ViewState do HTML."""
        soup = bs4.BeautifulSoup(html, "lxml")
        viewstate = soup.find("input", attrs={"name": "javax.faces.ViewState"})
        if not viewstate or not isinstance(viewstate, bs4.Tag):
            raise ValueError("ViewState não encontrado")
        return str(viewstate.get("value"))

    def _prepare_form_data(self, numero_processo: str, viewstate: str) -> Dict[str, str]:
        """Prepara dados do formulário para busca."""
        return {
            "AJAXREQUEST": "_viewRoot",
            "formConsulta": "formConsulta",
            "formConsulta:numeroProcesso": numero_processo,
            "formConsulta:j_id150": "Buscar",
            "javax.faces.ViewState": viewstate,
            "formConsulta:modal": "false"
        }

    def _extract_processo_url(self, html: str) -> Optional[str]:
        """Extrai URL da página do processo do HTML de resposta."""
        soup = bs4.BeautifulSoup(html, "lxml")

        # Procurar por links de processo
        links = soup.find_all("a", href=True)
        for link in links:
            if isinstance(link, bs4.Tag):
                href = link.get("href")
                if href and isinstance(href, str) and "DetalheProcessoConsultaPublica" in href:
                    # Construir URL completa
                    if href.startswith("/"):
                        base_url = "https://pje1g.trf1.jus.br"
                        return f"{base_url}{href}"
                    return href
        return None

    def _extract_andamentos(self, html: str) -> List[str]:
        """Extrai andamentos do HTML da página do processo."""
        soup = bs4.BeautifulSoup(html, "lxml")
        andamentos = []

        # Procurar tabela de andamentos
        table = soup.find("table", {"class": "rich-table"})
        if not table or not isinstance(table, bs4.Tag):
            return andamentos

        rows = table.find_all("tr")
        for row in rows[1:]:  # Pular header
            if isinstance(row, bs4.Tag):
                cols = row.find_all("td")
                if len(cols) >= 2:
                    data = cols[0].get_text(strip=True)
                    titulo = cols[1].get_text(strip=True)
                    if data and titulo:
                        andamentos.append(f"{data} - {titulo}")

        return andamentos