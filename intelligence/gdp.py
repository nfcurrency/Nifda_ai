
from intelligence.metrics import MetricResult, calculate_yoy
from intelligence.momentum import determine_momentum
from data.sources.fred import FREDClient


class GDPAnalyzer:
    """
    Analyzes US real GDP growth using FRED.

    NIFDA retrieves:
    - Latest GDP observation
    - GDP approximately 12 months earlier
    - GDP approximately 24 months earlier

    The engine calculates YoY GDP growth and its momentum.
    """

    SERIES_ID = "GDPC1"
    NAME = "US Real GDP"

    def __init__(self, client: FREDClient | None = None):
        self.client = client or FREDClient()

    @staticmethod
    def _get_value(observation: dict) -> float:
        value = observation.get("value")

        if value in (None, "", "."):
            raise ValueError("GDP observation has no valid value.")

        return float(value)

    @staticmethod
    def _shift_year(date_string: str, years: int) -> str:
        year, month, day = map(int, date_string.split("-"))
        return f"{year - years:04d}-{month:02d}-{day:02d}"

    def _get_latest_observation(self) -> dict:
        data = self.client.get_series(self.SERIES_ID)
        observations = data.get("observations", [])

        if not observations:
            raise ValueError("No latest GDP observation returned.")

        return observations[0]

    def analyze_yoy(self) -> MetricResult:
        latest = self._get_latest_observation()

        latest_date = latest["date"]
        current_value = self._get_value(latest)

        previous_date = self._shift_year(latest_date, 1)
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
            growth_view = "Economic output is expanding."

        elif result.direction == "FALLING":
            growth_view = "Economic output is contracting."

        else:
            growth_view = "Economic output is broadly unchanged."

        if momentum == "ACCELERATING":
            momentum_view = "GDP growth is accelerating."

        elif momentum == "DECELERATING":
            momentum_view = "GDP growth is decelerating."

        else:
            momentum_view = "GDP growth is broadly stable."

        result.interpretation = (
            f"{result.interpretation} "
            f"{growth_view} "
            f"{momentum_view} "
            f"Latest observation: {latest_date}."
        )

        return result