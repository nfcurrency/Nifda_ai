from dataclasses import dataclass

from intelligence.metrics import MetricResult
from intelligence.macro_state import MacroState
from intelligence.state_analyzer import StateAnalyzer


@dataclass
class MacroSnapshot:
    """
    Unified snapshot of the current macroeconomic environment.
    """

    inflation: MacroState
    unemployment: MacroState
    payrolls: MacroState
    retail_sales: MacroState
    industrial_production: MacroState
    gdp: MacroState
    fed_policy: MacroState

    def states(self) -> list[MacroState]:
        """
        Return all macro states in a consistent order.
        """

        return [
            self.inflation,
            self.unemployment,
            self.payrolls,
            self.retail_sales,
            self.industrial_production,
            self.gdp,
            self.fed_policy,
        ]

    def rising_factors(self) -> list[str]:
        """
        Return factors currently rising.
        """

        return [
            state.factor
            for state in self.states()
            if state.direction == "RISING"
        ]

    def falling_factors(self) -> list[str]:
        """
        Return factors currently falling.
        """

        return [
            state.factor
            for state in self.states()
            if state.direction == "FALLING"
        ]

    def accelerating_factors(self) -> list[str]:
        """
        Return factors with accelerating momentum.
        """

        return [
            state.factor
            for state in self.states()
            if state.momentum == "ACCELERATING"
        ]

    def decelerating_factors(self) -> list[str]:
        """
        Return factors with decelerating momentum.
        """

        return [
            state.factor
            for state in self.states()
            if state.momentum == "DECELERATING"
        ]

    def interpretation(self) -> str:
        """
        Produce a concise description of the current macro state.
        """

        rising = self.rising_factors()
        falling = self.falling_factors()
        accelerating = self.accelerating_factors()
        decelerating = self.decelerating_factors()

        parts = []

        if rising:
            parts.append(
                "Rising factors: "
                + ", ".join(rising)
                + "."
            )

        if falling:
            parts.append(
                "Falling factors: "
                + ", ".join(falling)
                + "."
            )

        if accelerating:
            parts.append(
                "Accelerating factors: "
                + ", ".join(accelerating)
                + "."
            )

        if decelerating:
            parts.append(
                "Decelerating factors: "
                + ", ".join(decelerating)
                + "."
            )

        if not parts:
            return "Macro conditions are broadly stable."

        return " ".join(parts)


class MacroAggregator:
    """
    Converts individual intelligence engines into one
    unified macroeconomic snapshot.
    """

    def __init__(self):
        self.state_analyzer = StateAnalyzer()

    def build_snapshot(
        self,
        inflation: MetricResult,
        unemployment: MetricResult,
        payrolls: MetricResult,
        retail_sales: MetricResult,
        industrial_production: MetricResult,
        gdp: MetricResult,
        fed_policy: MetricResult,
    ) -> MacroSnapshot:

        return MacroSnapshot(
            inflation=self.state_analyzer.analyze(
                inflation,
                "US Inflation",
                inflation.momentum or "STABLE",
            ),
            unemployment=self.state_analyzer.analyze(
                unemployment,
                "US Unemployment",
                unemployment.momentum or "STABLE",
            ),
            payrolls=self.state_analyzer.analyze(
                payrolls,
                "US Payrolls",
                payrolls.momentum or "STABLE",
            ),
            retail_sales=self.state_analyzer.analyze(
                retail_sales,
                "US Retail Sales",
                retail_sales.momentum or "STABLE",
            ),
            industrial_production=self.state_analyzer.analyze(
                industrial_production,
                "US Industrial Production",
                industrial_production.momentum or "STABLE",
            ),
            gdp=self.state_analyzer.analyze(
                gdp,
                "US GDP",
                gdp.momentum or "STABLE",
            ),
            fed_policy=self.state_analyzer.analyze(
                fed_policy,
                "Federal Reserve Policy",
                fed_policy.momentum or "STABLE",
            ),
        )
