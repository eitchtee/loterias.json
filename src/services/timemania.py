"""
Timemania lottery data collection service.
"""

from base import BaseService


class TimemaniaService(BaseService):
    """Service for collecting Timemania lottery results."""

    @property
    def name(self) -> str:
        return "timemania"

    @property
    def base_url(self) -> str:
        return "https://servicebus2.caixa.gov.br/portaldeloterias/api/timemania"

    def transform_draw(self, raw_data: dict) -> dict:
        """Transform raw API data - includes time do coração."""
        # Normalize the team name by removing tabs and extra whitespace
        time_coracao = raw_data.get("nomeTimeCoracaoMesSorte", "")
        if time_coracao:
            time_coracao = " ".join(time_coracao.replace("\t", " ").split())

        return {
            "concurso": raw_data["numero"],
            "data": raw_data["dataApuracao"],
            "resultado": raw_data["listaDezenas"],
            "time_do_coracao": time_coracao,
        }


def main():
    """Entry point called by the orchestrator."""
    service = TimemaniaService()
    service.run()
