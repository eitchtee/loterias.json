"""
Lotomania lottery data collection service.
"""

from base import BaseService


class LotomaniaService(BaseService):
    """Service for collecting Lotomania lottery results."""

    @property
    def name(self) -> str:
        return "lotomania"

    @property
    def base_url(self) -> str:
        return "https://servicebus2.caixa.gov.br/portaldeloterias/api/lotomania"


def main():
    """Entry point called by the orchestrator."""
    service = LotomaniaService()
    service.run()
