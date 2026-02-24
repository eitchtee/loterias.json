import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "services"))
from base import BaseService


class DummyService(BaseService):
    @property
    def name(self) -> str:
        return "dummy"

    @property
    def base_url(self) -> str:
        return "https://example.com"


class BaseServiceRunTests(unittest.TestCase):
    def test_run_fetches_latest_with_cache_bypassed(self):
        service = DummyService()
        service.session = MagicMock()
        cache_ctx = MagicMock()
        service.session.cache_disabled.return_value = cache_ctx
        service.fetch_json = MagicMock(
            return_value={
                "numero": 1,
                "dataApuracao": "01/01/2026",
                "listaDezenas": ["01"],
            }
        )
        service.save_json = MagicMock()

        service.run()

        service.session.cache_disabled.assert_called_once_with()
        cache_ctx.__enter__.assert_called_once_with()
        cache_ctx.__exit__.assert_called_once()
        service.fetch_json.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
