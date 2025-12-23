"""
Base service class for Loterias data collection.
All lottery services should inherit from this class.
"""

import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import requests


class BaseService(ABC):
    """
    Abstract base class for lottery data collection services.

    Subclasses must implement:
        - name: The service name (e.g., "mega-sena")
        - base_url: The API endpoint URL

    The run() method is provided by default and handles:
        - Loading existing draws
        - Fetching missing draws (supports gaps)
        - Saving as sorted JSON array
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.session = requests.Session()
        self.data_dir = Path(__file__).parent.parent.parent / "data"

    @property
    @abstractmethod
    def name(self) -> str:
        """Service identifier name (used for file naming)."""
        pass

    @property
    @abstractmethod
    def base_url(self) -> str:
        """Base API endpoint URL."""
        pass

    def fetch(self, url: str | None = None, **kwargs) -> requests.Response:
        """
        Make a GET request to the API.

        Args:
            url: Full URL or endpoint path. If None, uses base_url.
            **kwargs: Additional arguments passed to requests.get()

        Returns:
            Response object from the request.
        """
        target_url = url or self.base_url
        self.logger.debug(f"Fetching: {target_url}")

        response = self.session.get(target_url, **kwargs)
        response.raise_for_status()

        return response

    def fetch_json(self, url: str | None = None, **kwargs) -> Any:
        """
        Make a GET request and return JSON data.

        Args:
            url: Full URL or endpoint path. If None, uses base_url.
            **kwargs: Additional arguments passed to requests.get()

        Returns:
            Parsed JSON data.
        """
        response = self.fetch(url, **kwargs)
        return response.json()

    def save_json(self, data: Any, filename: str | None = None) -> Path:
        """
        Save data as a JSON file in the data directory.

        Args:
            data: Data to save (must be JSON serializable).
            filename: Output filename. Defaults to "{service_name}.json".

        Returns:
            Path to the saved file.
        """
        if filename is None:
            filename = f"{self.name}.json"

        output_path = self.data_dir / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        self.logger.info(f"Saved data to {output_path}")
        return output_path

    def load_existing_data(self) -> dict[int, dict]:
        """
        Load existing draws from the JSON file.

        Returns:
            Dictionary mapping concurso number to draw data.
        """
        output_path = self.data_dir / f"{self.name}.json"

        if not output_path.exists():
            return {}

        try:
            with open(output_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Handle both single object (old format) and array (new format)
            if isinstance(data, dict):
                return {data["concurso"]: data}
            else:
                return {draw["concurso"]: draw for draw in data}
        except (json.JSONDecodeError, KeyError) as e:
            self.logger.warning(f"Could not load existing data: {e}")
            return {}

    def transform_draw(self, raw_data: dict) -> dict:
        """
        Transform raw API data to our desired format.
        Override this method in subclasses if needed.
        """
        return {
            "concurso": raw_data["numero"],
            "data": raw_data["dataApuracao"],
            "resultado": raw_data["listaDezenas"],
        }

    def run(self) -> None:
        """Collect all lottery results for this service."""
        self.logger.info(f"Starting {self.name} data collection...")

        # Load existing draws
        existing_draws = self.load_existing_data()
        self.logger.info(f"Found {len(existing_draws)} existing draws")

        # Get the latest draw to find the current max concurso
        latest_raw = self.fetch_json()
        latest_concurso = latest_raw["numero"]
        self.logger.info(f"Latest concurso is {latest_concurso}")

        # Add latest if not exists
        if latest_concurso not in existing_draws:
            existing_draws[latest_concurso] = self.transform_draw(latest_raw)

        # Iterate from 1 to latest, fetching any missing draws
        new_draws_count = 0
        for concurso in range(1, latest_concurso + 1):
            if concurso in existing_draws:
                continue  # Skip - already have this one

            # Fetch the missing draw
            try:
                raw_data = self.fetch_json(f"{self.base_url}/{concurso}")
                existing_draws[concurso] = self.transform_draw(raw_data)
                new_draws_count += 1
            except Exception as e:
                self.logger.warning(
                    f"Could not fetch draw {concurso} for {self.name}: {e}"
                )
                continue

            if new_draws_count % 100 == 0:
                self.logger.info(f"Fetched {new_draws_count} new draws...")

        # Sort by concurso number and save
        sorted_draws = sorted(existing_draws.values(), key=lambda x: x["concurso"])
        self.save_json(sorted_draws)

        self.logger.info(
            f"{self.name} data collection finished. "
            f"Added {new_draws_count} new draws. Total: {len(sorted_draws)}"
        )
