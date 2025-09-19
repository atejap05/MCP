import logging

# URLs do TRF1 para scraping
TRF1_BASE_URLS = {"G1": "https://pje1g.trf1.jus.br", "G2": "https://pje2g.trf1.jus.br"}

TRF1_CONSULTA_URLS = {
    "G1": "https://pje1g.trf1.jus.br/consultapublica/ConsultaPublica/listView.seam",
    "G2": "https://pje2g.trf1.jus.br/consultapublica/ConsultaPublica/listView.seam",
}

# Configure logging
LOG_LEVEL = logging.INFO
LOGGER_NAME = "mcp-jud"


def setup_logging():
    """Configura logging básico para o MCP Server."""
    logging.basicConfig(
        level=LOG_LEVEL,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )