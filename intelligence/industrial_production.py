from datetime import date

from data.sources.fred import FREDClient
from intelligence.metrics import MetricResult, calculate_yoy
from intelligence.momentum import determine_momentum


class IndustrialProductionAnalyzer:
    """
    Analyzes US Industrial Production.

    FRED series:
        INDPRO - Industrial Production Index

    NIFDA calculates:
    - YoY industrial production growth
    - Direction
    - Momentum
    - Economic interpretation
    """

    SERIES_ID = "INDPRO"
    NAME = "US Industrial Production"

    def __init__(self, client: FREDClient | None = None):
        self.client = client or FREDClient()

    @staticmethod
    def _get_value(observation: dict) -> float:
        value = observation.get("value")

        if value in (None, "", "."):
            raise ValueError(
                "Industrial Production observation has no valid value."
            )

        return float(value)

    @staticmethod
    def _shift_year(date_string: str, years: int) -> str:
        year, month, day = map(
            int,
            date_string.split("-"),
        )

        try:
            shifted = date(
                year - years,
                month,
                day,
            )
        except ValueError:
            shifted = date(
                year - years,
                month,
                28,
            )

        return shifted.isoformat()

    def _get_latest_observation(self) -> dict:
        data = self.client.get_series(
            self.SERIES_ID
        )

        observations = data.get(
            "observations",
            [],
        )

        if not observations:
            raise ValueError(
                "No latest Industrial Production observation returned."
            )

        return observations[0]

    def analyze_yoy(
        self,
        include_momentum: bool = True,
    ) -> MetricResult:
        """
        Calculate current Industrial Production
        year-over-year growth.
        """

        latest = self._get_latest_observation()

        latest_date = latest["date"]
        current_value = self._get_value(latest)

        previous_date = self._shift_year(
            latest_date,
            1,
        )

        previous = self.client.get_observation(
            self.SERIES_ID,
            previous_date,
        )

        previous_value = self._get_value(
            previous
        )

        result = calculate_yoy(
            current_value=current_value,
            previous_value=previous_value,
            metric_name=self.NAME,
        )

        if not include_momentum:
            result.interpretation = (
                f"{result.interpretation} "
                f"Latest observation: {latest_date}."
            )
            return result

        previous_previous_date = self._shift_year(
            latest_date,
            2,
        )

        previous_previous = self.client.get_observation(
            self.SERIES_ID,
            previous_previous_date,
        )

        previous_previous_value = self._get_value(
            previous_previous
        )

        previous_yoy = calculate_yoy(
            current_value=previous_value,
            previous_value=previous_previous_value,
            metric_name=self.NAME,
        )

        momentum = determine_momentum(
            result.change_percent,
            previous_yoy.change_percent,
        )

        result.momentum = momentum

        if result.direction == "RISING":
            activity_view = (
                "Industrial activity is expanding."
            )

        elif result.direction == "FALLING":
            activity_view = (
                "Industrial activity is contracting."
            )

        else:
            activity_view = (
                "Industrial activity is broadly stable."
            )

        if momentum == "ACCELERATING":
            momentum_view = (
                "Industrial growth is accelerating."
            )

        elif momentum == "DECELERATING":
            momentum_view = (
                "Industrial growth is decelerating."
            )

        else:
            momentum_view = (
                "Industrial growth is broadly stable."
            )

        result.interpretation = (
            f"{result.interpretation} "
            f"{activity_view} "
            f"{momentum_view} "
            f"Latest observation: {latest_date}."
        )

        return result