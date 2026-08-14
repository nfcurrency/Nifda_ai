from datetime import date

from data.sources.fred import FREDClient
from intelligence.metrics import MetricResult, calculate_yoy


class CPIAnalyzer:
    """
    Retrieves the minimum CPI data required for fundamental analysis.

    NIFDA retrieves only:
    - Latest CPI
    - CPI approximately 12 months earlier
    - CPI approximately 24 months earlier

    No large historical dataset is downloaded.
    """

    SERIES_ID = "CPIAUCSL"
    NAME = "US Consumer Price Index"

    def __init__(self, client: FREDClient | None = None):
        self.client = client or FREDClient()

    @staticmethod
    def _get_value(observation: dict) -> float:
        value = observation.get("value")

        if value in (None, "", "."):
            raise ValueError("CPI observation has no valid value.")

        return float(value)

    @staticmethod
    def _shift_year(date_string: str, years: int) -> str:
        """
        Shift an observation date backward by a number of years.

        CPI observations are monthly and normally use the first
        day of the month, so preserving month/day is sufficient.
        """

        year, month, day = map(int, date_string.split("-"))

        try:
            shifted = date(year - years, month, day)
        except ValueError:
            # Handles February 29 when shifting to a non-leap year.
            shifted = date(year - years, month, 28)

        return shifted.isoformat()

    def _get_latest_observation(self) -> dict:
        data = self.client.get_series(self.SERIES_ID)
        observations = data.get("observations", [])

        if not observations:
            raise ValueError("No latest CPI observation returned.")

        return observations[0]

    def analyze_yoy(
        self,
        include_momentum: bool = True,
    ) -> MetricResult:
        """
        Calculate current CPI year-over-year inflation automatically.

        If include_momentum is True, NIFDA also compares the current
        YoY reading with the previous year's YoY reading.

        Only the specific observations required for the calculation
        are requested from FRED.
        """

        # Get latest CPI.
        latest = self._get_latest_observation()

        latest_date = latest["date"]
        current_value = self._get_value(latest)

        # Determine the corresponding month one year earlier.
        previous_date = self._shift_year(
            latest_date,
            1,
        )

        previous = self.client.get_observation(
            self.SERIES_ID,
            previous_date,
        )

        previous_value = self._get_value(previous)

        # Calculate current CPI YoY.
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

        # Determine the corresponding month two years earlier.
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

        # Calculate the previous year's YoY inflation.
        previous_yoy = calculate_yoy(
            current_value=previous_value,
            previous_value=previous_previous_value,
            metric_name=self.NAME,
        )

        # Compare current YoY with previous YoY.
        momentum_change = (
            result.change_percent
            - previous_yoy.change_percent
        )

        if momentum_change > 0:
            momentum = "ACCELERATING"
            inflation_interpretation = (
                "Inflation is accelerating compared with "
                "the previous year-over-year reading."
            )

        elif momentum_change < 0:
            momentum = "DECELERATING"
            inflation_interpretation = (
                "Inflation is decelerating compared with "
                "the previous year-over-year reading."
            )

        else:
            momentum = "STABLE"
            inflation_interpretation = (
                "Inflation is broadly stable compared with "
                "the previous year-over-year reading."
            )

        result.interpretation = (
            f"{result.interpretation} "
            f"Momentum: {momentum}. "
            f"{inflation_interpretation} "
            f"Latest observation: {latest_date}."
        )

        return result