"""
Dia de Sorte lottery data collection service.
"""

from base import BaseService


class DiaDeSorteService(BaseService):
    """Service for collecting Dia de Sorte lottery results."""

    @property
    def name(self) -> str:
        return "dia-de-sorte"

    @property
    def base_url(self) -> str:
        return "https://servicebus2.caixa.gov.br/portaldeloterias/api/diadesorte"


def main():
    """Entry point called by the orchestrator."""
    service = DiaDeSorteService()
    service.run()
