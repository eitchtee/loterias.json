"""
Base service class for Loterias data collection.
All lottery services should inherit from this class.
"""

import json
import logging
from abc import ABC, abstractmethod
from datetime import timedelta
from pathlib import Path
from typing import Any

import requests_cache


class BaseService(ABC):
    """
    Abstract base class for lottery data collection services.

    Subclasses must implement:
        - name: The service name (e.g., "mega-sena")
        - base_url: The API endpoint URL

    Optionally override:
        - cache_name: The cache folder name (defaults to service name)

    The run() method is provided by default and handles:
        - Loading existing draws
        - Fetching missing draws (supports gaps)
        - Saving as sorted JSON array
    """

    # Cache expiration: 6 months (approximately 180 days)
    CACHE_EXPIRATION = timedelta(days=180)

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.data_dir = Path(__file__).parent.parent.parent / "data"
        self.cache_dir = Path(__file__).parent.parent.parent / "cache"

        # Set up cached session with JSON file backend
        cache_path = self.cache_dir / self.cache_name
        cache_path.mkdir(parents=True, exist_ok=True)

        self.session = requests_cache.CachedSession(
            cache_name=str(cache_path),
            backend="filesystem",
            serializer="json",
            expire_after=self.CACHE_EXPIRATION,
        )

    @property
    def cache_name(self) -> str:
        """
        Cache folder name. Override this to share cache between services.
        Defaults to the service name.
        """
        return self.name

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

    def fetch(self, url: str | None = None, **kwargs) -> requests_cache.Response:
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

        # Get the latest draw to find the current max concurso
        # Always bypass cache so new concursos can be detected on every run
        with self.session.cache_disabled():
            latest_raw = self.fetch_json()
        latest_concurso = latest_raw["numero"]
        self.logger.info(f"Latest concurso is {latest_concurso}")

        # Fetch all draws (cache handles avoiding redundant requests)
        draws = {}
        draws[latest_concurso] = self.transform_draw(latest_raw)

        for concurso in range(1, latest_concurso):
            try:
                raw_data = self.fetch_json(f"{self.base_url}/{concurso}")
                draws[concurso] = self.transform_draw(raw_data)
            except Exception as e:
                self.logger.warning(
                    f"Could not fetch draw {concurso} for {self.name}: {e}"
                )
                continue

        # Sort by concurso number and save
        sorted_draws = sorted(draws.values(), key=lambda x: x["concurso"])
        self.save_json(sorted_draws)

        self.logger.info(
            f"{self.name} data collection finished. Total: {len(sorted_draws)}"
        )
