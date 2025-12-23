"""
Mega-Sena da Virada lottery data collection service.
Filters Mega-Sena draws that happened on December 31st.
"""

import json

from base import BaseService


class MegaSenaDaViradaService(BaseService):
    """Service for collecting Mega-Sena da Virada lottery results."""

    @property
    def name(self) -> str:
        return "mega-sena-da-virada"

    @property
    def base_url(self) -> str:
        # Not used - we read from mega-sena.json instead
        return ""

    def run(self) -> None:
        """Filter Mega-Sena draws that happened on December 31st."""
        self.logger.info("Starting Mega-Sena da Virada data collection...")

        # Read from mega-sena.json
        mega_sena_path = self.data_dir / "mega-sena.json"

        if not mega_sena_path.exists():
            self.logger.warning("mega-sena.json not found, skipping")
            return

        with open(mega_sena_path, "r", encoding="utf-8") as f:
            mega_sena_draws = json.load(f)

        # Filter draws that happened on December 31st
        # Date format is DD/MM/YYYY
        virada_draws = [
            draw for draw in mega_sena_draws if draw["data"].startswith("31/12")
        ]

        # Sort by concurso
        virada_draws.sort(key=lambda x: x["concurso"])

        self.save_json(virada_draws)

        self.logger.info(
            f"Mega-Sena da Virada data collection finished. "
            f"Found {len(virada_draws)} draws on December 31st."
        )


def main():
    """Entry point called by the orchestrator."""
    service = MegaSenaDaViradaService()
    service.run()
