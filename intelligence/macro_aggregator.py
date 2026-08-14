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