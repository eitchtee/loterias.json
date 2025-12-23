"""
Lotofácil lottery data collection service.
"""

from base import BaseService


class LotofacilService(BaseService):
    """Service for collecting Lotofácil lottery results."""

    @property
    def name(self) -> str:
        return "lotofacil"

    @property
    def base_url(self) -> str:
        return "https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil"


def main():
    """Entry point called by the orchestrator."""
    service = LotofacilService()
    service.run()
