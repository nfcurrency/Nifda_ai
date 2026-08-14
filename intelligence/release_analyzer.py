from intelligence.event import MarketEvent
from intelligence.release import ReleaseResult
from intelligence.surprise import calculate_surprise
from intelligence.impact import IMPACTS
from intelligence.indicators import INDICATORS

class ReleaseAnalyzer:
    """
    Converts a MarketEvent into a macroeconomic interpretation.
    """

    def analyze(self, event: MarketEvent, indicator_id: str) -> ReleaseResult:

        if indicator_id not in IMPACTS:
            raise ValueError(
                f"No economic impact metadata found for {indicator_id}"
            )

        if event.actual is None:
            raise ValueError(
                f"{event.event_name} does not have an actual value."
            )

        surprise_result = calculate_surprise(
            event,
            indicator_id,
        )

        result = ReleaseResult(
    event_name=event.event_name,
    indicator_id=indicator_id,
    timestamp=event.timestamp,
    actual=event.actual,
    forecast=event.forecast,
    previous=event.previous,
    surprise=surprise_result.numerical_surprise,
    economic_direction=surprise_result.direction,
    importance=INDICATORS[indicator_id].importance,
)

        if surprise_result.direction is None:
            return result

        impact = IMPACTS[indicator_id]

        if surprise_result.direction == "POSITIVE":
            result.inflationary_pressure = impact.inflationary_pressure
            result.growth_signal = impact.growth_signal
            result.fed_policy_bias = impact.fed_policy_bias

        else:
            result.inflationary_pressure = self._reverse(
                impact.inflationary_pressure
            )
            result.growth_signal = self._reverse(
                impact.growth_signal
            )
            result.fed_policy_bias = self._reverse(
                impact.fed_policy_bias
            )

        result.interpretation = (
            f"{event.event_name} surprised to the "
            f"{surprise_result.direction.lower()} side. "
            f"Inflation pressure: {result.inflationary_pressure}. "
            f"Growth signal: {result.growth_signal}. "
            f"Fed policy bias: {result.fed_policy_bias}."
        )

        return result

    @staticmethod
    def _reverse(value: str) -> str:

        reversals = {
            "INFLATIONARY": "DEFLATIONARY",
            "DEFLATIONARY": "INFLATIONARY",
            "POSITIVE": "NEGATIVE",
            "NEGATIVE": "POSITIVE",
            "HAWKISH": "DOVISH",
            "DOVISH": "HAWKISH",
            "NEUTRAL": "NEUTRAL",
        }

        return reversals.get(value, value)