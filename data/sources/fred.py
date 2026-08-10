import os
from datetime import date, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE, override=True)


class FREDClient:
    """
    Client for retrieving economic time-series data from FRED.

    NIFDA data policy:
    - No historical window requested -> latest observation only.
    - Historical window requested -> maximum 6 months.
    - Specific observation requested -> retrieve only that observation.
    """

    BASE_URL = "https://api.stlouisfed.org/fred"
    MAX_HISTORY_DAYS = 183

    def __init__(self):
        api_key = os.getenv("FRED_API_KEY")

        if not api_key:
            raise RuntimeError(
                f"FRED_API_KEY was not found. "
                f"Expected environment file at: {ENV_FILE}"
            )

        self.api_key = api_key

    def get_series(
        self,
        series_id: str,
        start_date: str | None = None,
    ) -> dict:
        """
        Retrieve observations for a FRED series.

        If start_date is omitted:
            Return only the latest observation.

        If start_date is provided:
            Return historical observations from that date,
            limited to approximately the most recent 6 months.
        """

        url = f"{self.BASE_URL}/series/observations"

        params = {
            "series_id": series_id,
            "api_key": self.api_key,
            "file_type": "json",
        }

        if start_date:
            requested_start = date.fromisoformat(start_date)

            earliest_allowed = date.today() - timedelta(
                days=self.MAX_HISTORY_DAYS
            )

            if requested_start < earliest_allowed:
                requested_start = earliest_allowed

            params["observation_start"] = requested_start.isoformat()
            params["sort_order"] = "asc"

        else:
            params["limit"] = 1
            params["sort_order"] = "desc"

        response = requests.get(
            url,
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        return response.json()

    def get_observation(
        self,
        series_id: str,
        observation_date: str,
    ) -> dict:
        """
        Retrieve one specific FRED observation.

        Used when NIFDA needs a targeted historical value,
        such as the CPI value from approximately 12 months ago
        for a YoY calculation.
        """

        url = f"{self.BASE_URL}/series/observations"

        params = {
            "series_id": series_id,
            "api_key": self.api_key,
            "file_type": "json",
            "observation_start": observation_date,
            "observation_end": observation_date,
            "limit": 1,
        }

        response = requests.get(
            url,
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        observations = data.get("observations", [])

        if not observations:
            raise ValueError(
                f"No observation found for {series_id} "
                f"on {observation_date}."
            )

        return observations[0]