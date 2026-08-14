from intelligence.metrics import MetricResult, calculate_yoy
from intelligence.momentum import determine_momentum
from data.sources.fred import FREDClient


class UnemploymentAnalyzer:
    """
    Analyzes the US unemployment rate.

    NIFDA retrieves:
    - Latest unemployment rate
    - Unemployment rate approximately 12 months earlier
    - Unemployment rate approximately 24 months earlier

    The analyzer converts the raw metric into a standardized
    MetricResult with direction and momentum.
    """

    SERIES_ID = "UNRATE"
    NAME = "US Unemployment Rate"

    def __init__(self, client: FREDClient | None = None):
        self.client = client or FREDClient()

    @staticmethod
    def _get_value(observation: dict) -> float:
        value = observation.get("value")

        if value in (None, "", "."):
            raise ValueError(
                "Unemployment observation has no valid value."
            )

        return float(value)

    @staticmethod
    def _shift_year(date_string: str, years: int) -> str:
        year, month, day = map(int, date_string.split("-"))

        from datetime import date

        try:
            shifted = date(year - years, month, day)
        except ValueError:
            shifted = date(year - years, month, 28)

        return shifted.isoformat()

    def _get_latest_observation(self) -> dict:
        data = self.client.get_series(self.SERIES_ID)
        observations = data.get("observations", [])

        if not observations:
            raise ValueError(
                "No latest unemployment observation returned."
            )

        return observations[0]

    def analyze_yoy(
        self,
        include_momentum: bool = True,
    ) -> MetricResult:
        """
        Analyze the unemployment rate relative to the
        corresponding period one year earlier.

        Note:
        For unemployment, a FALLING rate is generally
        interpreted as improving labor-market conditions,
        while a RISING rate indicates weakening conditions.
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

        previous_value = self._get_value(previous)

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
            direction_view = (
                "The labor market is showing signs of weakening."
            )
        elif result.direction == "FALLING":
            direction_view = (
                "The labor market is showing signs of improvement."
            )
        else:
            direction_view = (
                "The labor market is broadly stable."
            )

        if momentum == "ACCELERATING":
            momentum_view = (
                "The unemployment trend is accelerating."
            )
        elif momentum == "DECELERATING":
            momentum_view = (
                "The unemployment trend is decelerating."
            )
        else:
            momentum_view = (
                "The unemployment trend is broadly stable."
            )

        result.interpretation = (
            f"{result.interpretation} "
            f"{direction_view} "
            f"{momentum_view} "
            f"Latest observation: {latest_date}."
        )

        return result
