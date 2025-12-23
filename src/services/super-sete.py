"""
Super Sete lottery data collection service.
"""

from base import BaseService


class SuperSeteService(BaseService):
    """Service for collecting Super Sete lottery results."""

    @property
    def name(self) -> str:
        return "super-sete"

    @property
    def base_url(self) -> str:
        return "https://servicebus2.caixa.gov.br/portaldeloterias/api/supersete"


def main():
    """Entry point called by the orchestrator."""
    service = SuperSeteService()
    service.run()
