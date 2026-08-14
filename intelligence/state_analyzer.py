from intelligence.metrics import MetricResult
from intelligence.macro_state import MacroState


class StateAnalyzer:
    """
    Converts a MetricResult into a standardized MacroState.
    """

    def analyze(
        self,
        metric: MetricResult,
        factor: str,
        momentum: str,
    ) -> MacroState:

        interpretation = self._interpret(
            factor=factor,
            direction=metric.direction,
            momentum=momentum,
        )

        return MacroState(
            factor=factor,
            current_value=metric.current_value,
            direction=metric.direction,
            momentum=momentum,
            interpretation=interpretation,
        )

    @staticmethod
    def _interpret(
        factor: str,
        direction: str,
        momentum: str,
    ) -> str:

        if direction == "RISING" and momentum == "ACCELERATING":
            return f"{factor} is rising and accelerating."

        if direction == "RISING" and momentum == "DECELERATING":
            return f"{factor} is rising but decelerating."

        if direction == "RISING" and momentum == "STABLE":
            return f"{factor} is rising with stable momentum."

        if direction == "FALLING" and momentum == "ACCELERATING":
            return f"{factor} is falling and accelerating."

        if direction == "FALLING" and momentum == "DECELERATING":
            return f"{factor} is falling but decelerating."

        if direction == "FALLING" and momentum == "STABLE":
            return f"{factor} is falling with stable momentum."

        if direction == "UNCHANGED":
            return f"{factor} is unchanged."

        return (
            f"{factor} is {direction.lower()} "
            f"with {momentum.lower()} momentum."
        )
