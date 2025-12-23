"""
Quina lottery data collection service.
"""

from base import BaseService


class QuinaService(BaseService):
    """Service for collecting Quina lottery results."""

    @property
    def name(self) -> str:
        return "quina"

    @property
    def base_url(self) -> str:
        return "https://servicebus2.caixa.gov.br/portaldeloterias/api/quina"


def main():
    """Entry point called by the orchestrator."""
    service = QuinaService()
    service.run()
