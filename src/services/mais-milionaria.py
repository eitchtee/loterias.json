"""
+Milionária lottery data collection service.
"""

from base import BaseService


class MaisMilionariaService(BaseService):
    """Service for collecting +Milionária lottery results."""

    @property
    def name(self) -> str:
        return "mais-milionaria"

    @property
    def base_url(self) -> str:
        return "https://servicebus2.caixa.gov.br/portaldeloterias/api/maismilionaria"

    def transform_draw(self, raw_data: dict) -> dict:
        """Transform raw API data - includes trevos."""
        return {
            "concurso": raw_data["numero"],
            "data": raw_data["dataApuracao"],
            "resultado": raw_data["listaDezenas"],
            "trevos": raw_data["trevosSorteados"],
        }


def main():
    """Entry point called by the orchestrator."""
    service = MaisMilionariaService()
    service.run()
