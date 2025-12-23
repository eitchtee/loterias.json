"""
Federal lottery data collection service.
"""

from base import BaseService


class FederalService(BaseService):
    """Service for collecting Federal lottery results."""

    @property
    def name(self) -> str:
        return "federal"

    @property
    def base_url(self) -> str:
        return "https://servicebus2.caixa.gov.br/portaldeloterias/api/federal"


def main():
    """Entry point called by the orchestrator."""
    service = FederalService()
    service.run()
