"""
Dupla Sena lottery data collection service.
"""

from base import BaseService


class DuplaSenaService(BaseService):
    """Service for collecting Dupla Sena lottery results."""

    @property
    def name(self) -> str:
        return "dupla-sena"

    @property
    def base_url(self) -> str:
        return "https://servicebus2.caixa.gov.br/portaldeloterias/api/duplasena"

    def transform_draw(self, raw_data: dict) -> dict:
        """Transform raw API data - Dupla Sena has two draws."""
        return {
            "concurso": raw_data["numero"],
            "data": raw_data["dataApuracao"],
            "resultado_1": raw_data["listaDezenas"],
            "resultado_2": raw_data["listaDezenasSegundoSorteio"],
        }


def main():
    """Entry point called by the orchestrator."""
    service = DuplaSenaService()
    service.run()
