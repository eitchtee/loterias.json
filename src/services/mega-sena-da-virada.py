"""
Mega-Sena da Virada lottery data collection service.
Filters Mega-Sena draws where indicadorConcursoEspecial == 2.
Uses cached API responses shared with mega-sena service.
"""

from base import BaseService


class MegaSenaDaViradaService(BaseService):
    """Service for collecting Mega-Sena da Virada lottery results."""

    @property
    def name(self) -> str:
        return "mega-sena-da-virada"

    @property
    def base_url(self) -> str:
        return "https://servicebus2.caixa.gov.br/portaldeloterias/api/megasena"

    @property
    def cache_name(self) -> str:
        # Share cache with mega-sena service
        return "mega-sena"

    def run(self) -> None:
        """Fetch all Mega-Sena draws and filter those with indicadorConcursoEspecial == 2."""
        self.logger.info("Starting Mega-Sena da Virada data collection...")

        # Get the latest draw to find the current max concurso
        latest_raw = self.fetch_json()
        latest_concurso = latest_raw["numero"]
        self.logger.info(f"Latest concurso is {latest_concurso}")

        # Collect all virada draws
        virada_draws = []

        # Check if the latest is a virada
        if latest_raw.get("indicadorConcursoEspecial") == 2:
            virada_draws.append(self.transform_draw(latest_raw))

        # Fetch all draws and filter for virada (indicadorConcursoEspecial == 2)
        # Most requests will be served from cache
        for concurso in range(1, latest_concurso):
            try:
                raw_data = self.fetch_json(f"{self.base_url}/{concurso}")
                if raw_data.get("indicadorConcursoEspecial") == 2:
                    virada_draws.append(self.transform_draw(raw_data))
            except Exception as e:
                self.logger.warning(f"Could not fetch draw {concurso}: {e}")
                continue

        # Sort by concurso
        virada_draws.sort(key=lambda x: x["concurso"])

        self.save_json(virada_draws)

        self.logger.info(
            f"Mega-Sena da Virada data collection finished. "
            f"Found {len(virada_draws)} Virada draws."
        )


def main():
    """Entry point called by the orchestrator."""
    service = MegaSenaDaViradaService()
    service.run()
