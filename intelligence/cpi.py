from data.sources.fred import FREDClient
from intelligence.metrics import MetricResult, calculate_yoy


class CPIAnalyzer:
    """
    Retrieves the minimum CPI data required for fundamental analysis.

    NIFDA retrieves:
    - Latest CPI
    - CPI approximately 12 months earlier
    - Previous CPI
    - CPI approximately 12 months before that

    No large historical dataset is downloaded.
    """

    SERIES_ID = "CPIAUCSL"
    NAME = "US Consumer Price Index"

    def __init__(self, client: FREDClient | None = None):
        self.client = client or FREDClient()

    def _get_value(self, observation: dict) -> float:
        value = observation.get("value")

        if value in (None, "", "."):
            raise ValueError("CPI observation has no valid value.")

        return float(value)

    def analyze_yoy(
        self,
        previous_date: str,
        previous_previous_date: str | None = None,
    ) -> MetricResult:
        """
        Calculate CPI year-over-year change.

        previous_date:
            CPI observation approximately 12 months before latest.

        previous_previous_date:
            CPI observation approximately 12 months before previous_date.
            Required when calculating inflation momentum.
        """

        # Latest CPI
        latest_data = self.client.get_series(self.SERIES_ID)
        latest_observations = latest_data.get("observations", [])

        if not latest_observations:
            raise ValueError("No latest CPI observation returned.")

        current_value = self._get_value(latest_observations[0])

        # CPI approximately 12 months ago
        previous = self.client.get_observation(
            self.SERIES_ID,
            previous_date,
        )

        previous_value = self._get_value(previous)

        # Current YoY inflation
        result = calculate_yoy(
            current_value=current_value,
            previous_value=previous_value,
            metric_name=self.NAME,
        )

        # If we don't have the older comparison, return basic YoY.
        if previous_previous_date is None:
            return result

        # CPI approximately 24 months ago
        previous_previous = self.client.get_observation(
            self.SERIES_ID,
            previous_previous_date,
        )

        previous_previous_value = self._get_value(previous_previous)

        # Previous year's YoY inflation
        previous_yoy = calculate_yoy(
            current_value=previous_value,
            previous_value=previous_previous_value,
            metric_name=self.NAME,
        )

        # Compare current YoY against previous YoY.
        momentum_change = (
            result.change_percent - previous_yoy.change_percent
        )

        if momentum_change > 0:
            momentum = "ACCELERATING"
            inflation_interpretation = (
                "Inflation is accelerating compared with the "
                "previous year-over-year reading."
            )

        elif momentum_change < 0:
            momentum = "DECELERATING"
            inflation_interpretation = (
                "Inflation is decelerating compared with the "
                "previous year-over-year reading."
            )

        else:
            momentum = "STABLE"
            inflation_interpretation = (
                "Inflation is broadly stable compared with the "
                "previous year-over-year reading."
            )

        # Attach useful interpretation information to the result.
        result.interpretation = (
            f"{result.interpretation} "
            f"Momentum: {momentum}. "
            f"{inflation_interpretation}"
        )

        return result