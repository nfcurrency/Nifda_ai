from intelligence.metrics import MetricResult
from intelligence.momentum import determine_momentum


class FedPolicyAnalyzer:
    """
    Analyzes the Federal Funds Rate as a policy signal.

    Rising rates -> tighter / more hawkish policy.
    Falling rates -> easier / more dovish policy.
    Unchanged rates -> stable policy.
    """

    SERIES_ID = "FEDFUNDS"
    NAME = "US Federal Funds Rate"

    def __init__(self, client=None):
        if client is None:
            from data.sources.fred import FREDClient
            client = FREDClient()

        self.client = client

    @staticmethod
    def _get_value(observation: dict) -> float:
        value = observation.get("value")

        if value in (None, "", "."):
            raise ValueError("Federal Funds Rate observation has no valid value.")

        return float(value)

    def analyze(self) -> MetricResult:
        latest = self.client.get_series(self.SERIES_ID)
        observations = latest.get("observations", [])

        if not observations:
            raise ValueError("No Federal Funds Rate observation returned.")

        current_observation = observations[0]
        current_value = self._get_value(current_observation)
        latest_date = current_observation["date"]

        previous_data = self.client.get_series(
            self.SERIES_ID,
            start_date="2025-01-01",
        )

        previous_observations = previous_data.get("observations", [])

        if len(previous_observations) < 2:
            raise ValueError("Not enough Federal Funds Rate observations.")

        previous_observation = previous_observations[-2]
        previous_value = self._get_value(previous_observation)

        change = current_value - previous_value

        if change > 0:
            direction = "RISING"
            interpretation = (
                "The Federal Funds Rate is rising, "
                "indicating tighter monetary policy."
            )
        elif change < 0:
            direction = "FALLING"
            interpretation = (
                "The Federal Funds Rate is falling, "
                "indicating easier monetary policy."
            )
        else:
            direction = "UNCHANGED"
            interpretation = (
                "The Federal Funds Rate is unchanged, "
                "indicating stable policy conditions."
            )

        momentum = determine_momentum(
            current_value,
            previous_value,
        )

        if momentum == "ACCELERATING":
            policy_momentum = "The policy-rate movement is accelerating."
        elif momentum == "DECELERATING":
            policy_momentum = "The policy-rate movement is decelerating."
        else:
            policy_momentum = "The policy-rate movement is stable."

        interpretation = (
            f"{interpretation} "
            f"{policy_momentum} "
            f"Latest observation: {latest_date}."
        )

        return MetricResult(
            metric=self.NAME,
            current_value=current_value,
            previous_value=previous_value,
            change=change,
            change_percent=(
                (change / previous_value) * 100
                if previous_value != 0
                else 0.0
            ),
            direction=direction,
            interpretation=interpretation,
            momentum=momentum,
        )