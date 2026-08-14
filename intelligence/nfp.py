from datetime import date

from data.sources.fred import FREDClient
from intelligence.metrics import MetricResult


class NFPAnalyzer:
    """
    Analyzes US Nonfarm Payrolls (NFP).

    NIFDA retrieves:
    - Latest NFP level
    - Previous month's NFP level
    - Two-months-ago NFP level

    From these observations NIFDA calculates:
    - Monthly payroll change
    - Direction
    - Momentum
    - Interpretation

    FRED series:
        PAYEMS - All Employees, Total Nonfarm
    """

    SERIES_ID = "PAYEMS"
    NAME = "US Nonfarm Payrolls"

    def __init__(self, client: FREDClient | None = None):
        self.client = client or FREDClient()

    @staticmethod
    def _get_value(observation: dict) -> float:
        value = observation.get("value")

        if value in (None, "", "."):
            raise ValueError(
                "NFP observation has no valid value."
            )

        return float(value)

    @staticmethod
    def _shift_month(date_string: str, months: int) -> str:
        """
        Shift an observation date backward by a number of months.
        """

        year, month, day = map(
            int,
            date_string.split("-"),
        )

        month -= months

        while month <= 0:
            month += 12
            year -= 1

        return date(
            year,
            month,
            1,
        ).isoformat()

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
                "No latest NFP observation returned."
            )

        return observations[0]

    def analyze_monthly(
        self,
        include_momentum: bool = True,
    ) -> MetricResult:
        """
        Analyze the latest monthly change in US
        nonfarm payrolls.
        """

        latest = self._get_latest_observation()

        latest_date = latest["date"]
        current_value = self._get_value(latest)

        previous_date = self._shift_month(
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

        current_change = (
            current_value - previous_value
        )

        previous_previous_date = self._shift_month(
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

        previous_change = (
            previous_value
            - previous_previous_value
        )

        if current_change > 0:
            direction = "RISING"
            interpretation = (
                f"{self.NAME} increased by "
                f"{current_change:.0f} thousand jobs."
            )

        elif current_change < 0:
            direction = "FALLING"
            interpretation = (
                f"{self.NAME} decreased by "
                f"{abs(current_change):.0f} thousand jobs."
            )

        else:
            direction = "UNCHANGED"
            interpretation = (
                f"{self.NAME} was unchanged."
            )

        if current_change > previous_change:
            momentum = "ACCELERATING"

        elif current_change < previous_change:
            momentum = "DECELERATING"

        else:
            momentum = "STABLE"

        if include_momentum:
            if momentum == "ACCELERATING":
                momentum_text = (
                    "Payroll growth is accelerating "
                    "compared with the previous month."
                )

            elif momentum == "DECELERATING":
                momentum_text = (
                    "Payroll growth is decelerating "
                    "compared with the previous month."
                )

            else:
                momentum_text = (
                    "Payroll growth is broadly stable "
                    "compared with the previous month."
                )

            interpretation = (
                f"{interpretation} "
                f"{momentum_text} "
                f"Latest observation: {latest_date}."
            )

        else:
            interpretation = (
                f"{interpretation} "
                f"Latest observation: {latest_date}."
            )

        return MetricResult(
            metric=self.NAME,
            current_value=current_value,
            previous_value=previous_value,
            change=current_change,
            change_percent=(
                (current_change / previous_value) * 100
                if previous_value != 0
                else 0.0
            ),
            direction=direction,
            interpretation=interpretation,
            momentum=momentum,
        )