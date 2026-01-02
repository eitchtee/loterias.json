"""
Mega-Sena da Virada lottery data collection service.
Filters Mega-Sena draws where indicadorConcursoEspecial == 2 or date is 31/12 (2008+).
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

    def _is_virada(self, raw_data: dict) -> bool:
        """
        Check if a draw is a Mega-Sena da Virada.

        A draw is considered Virada if:
        - indicadorConcursoEspecial == 2 (official API indicator), OR
        - Date is 31/12 and year is 2008 or later (first Virada was 2008)
        """
        # Check official indicator
        if raw_data.get("indicadorConcursoEspecial") == 2:
            return True

        # Fallback: check date (DD/MM/YYYY format)
        date_str = raw_data.get("dataApuracao", "")
        if date_str.startswith("31/12"):
            try:
                year = int(date_str.split("/")[2])
                if year >= 2008:
                    return True
            except (IndexError, ValueError):
                pass

        return False

    def run(self) -> None:
        """Fetch all Mega-Sena draws and filter Virada draws."""
        self.logger.info("Starting Mega-Sena da Virada data collection...")

        # Get the latest draw to find the current max concurso
        latest_raw = self.fetch_json()
        latest_concurso = latest_raw["numero"]
        self.logger.info(f"Latest concurso is {latest_concurso}")

        # Collect all virada draws
        virada_draws = []

        # Check if the latest is a virada
        if self._is_virada(latest_raw):
            virada_draws.append(self.transform_draw(latest_raw))

        # Fetch all draws and filter for virada
        # Most requests will be served from cache
        for concurso in range(1, latest_concurso):
            try:
                raw_data = self.fetch_json(f"{self.base_url}/{concurso}")
                if self._is_virada(raw_data):
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
