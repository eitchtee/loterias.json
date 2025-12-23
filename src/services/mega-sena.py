"""
Mega-Sena lottery data collection service.
"""

from base import BaseService


class MegaSenaService(BaseService):
    """Service for collecting Mega-Sena lottery results."""

    @property
    def name(self) -> str:
        return "mega-sena"

    @property
    def base_url(self) -> str:
        return "https://servicebus2.caixa.gov.br/portaldeloterias/api/megasena"


def main():
    """Entry point called by the orchestrator."""
    service = MegaSenaService()
    service.run()
