import os
from pathlib import Path

import requests
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE, override=True)


class FREDClient:
    """
    Client for retrieving economic time-series data from FRED.
    """

    BASE_URL = "https://api.stlouisfed.org/fred"

    def __init__(self):
        api_key = os.getenv("FRED_API_KEY")

        if not api_key:
            raise RuntimeError(
                f"FRED_API_KEY was not found. "
                f"Expected environment file at: {ENV_FILE}"
            )

        self.api_key = api_key

    def get_series(self, series_id: str):
        url = f"{self.BASE_URL}/series/observations"

        params = {
            "series_id": series_id,
            "api_key": self.api_key,
            "file_type": "json",
        }

        response = requests.get(
            url,
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        return response.json()