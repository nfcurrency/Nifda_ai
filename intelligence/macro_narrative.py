from dataclasses import dataclass

from intelligence.macro_assessment import MacroAssessment


@dataclass
class MacroNarrative:
    """
    Human-readable interpretation of the current
    macroeconomic environment.
    """

    regime: str
    summary: str
    inflation_view: str
    growth_view: str
    policy_view: str
    market_implication: str


class MacroNarrativeEngine:
    """
    Converts a MacroAssessment into a structured
    macroeconomic narrative.
    """

    def generate(
        self,
        assessment: MacroAssessment,
    ) -> MacroNarrative:

        inflation_view = self._inflation_view(
            assessment.inflation_bias
        )

        growth_view = self._growth_view(
            assessment.growth_bias
        )

        policy_view = self._policy_view(
            assessment.fed_bias
        )

        market_implication = self._market_implication(
            assessment.regime
        )

        summary = self._summary(
            assessment.regime,
            assessment.inflation_bias,
            assessment.growth_bias,
            assessment.fed_bias,
        )

        return MacroNarrative(
            regime=assessment.regime,
            summary=summary,
            inflation_view=inflation_view,
            growth_view=growth_view,
            policy_view=policy_view,
            market_implication=market_implication,
        )

    @staticmethod
    def _inflation_view(bias: str) -> str:

        if bias == "POSITIVE":
            return "Inflationary pressure is elevated."

        if bias == "NEGATIVE":
            return "Inflationary pressure is easing."

        return "Inflation conditions are mixed."

    @staticmethod
    def _growth_view(bias: str) -> str:

        if bias == "POSITIVE":
            return "Growth conditions are strengthening."

        if bias == "NEGATIVE":
            return "Growth conditions are weakening."

        return "Growth conditions are mixed."

    @staticmethod
    def _policy_view(bias: str) -> str:

        if bias == "HAWKISH":
            return "Policy conditions favor a more restrictive Fed stance."

        if bias == "DOVISH":
            return "Policy conditions favor a more accommodative Fed stance."

        return "Policy conditions provide no clear directional signal."

    @staticmethod
    def _market_implication(regime: str) -> str:

        implications = {
            "STAGFLATIONARY": (
                "The environment is challenging for risk assets "
                "because inflation remains elevated while growth weakens."
            ),
            "DISINFLATIONARY_SLOWDOWN": (
                "Falling inflation alongside weaker growth may increase "
                "expectations for future monetary easing."
            ),
            "REFLATIONARY": (
                "Rising inflation alongside stronger growth may increase "
                "expectations for tighter monetary policy."
            ),
            "GOLDILOCKS": (
                "Falling inflation with stronger growth creates a "
                "generally supportive macro environment."
            ),
            "HAWKISH": (
                "The macro environment favors tighter monetary policy."
            ),
            "DOVISH": (
                "The macro environment favors easier monetary policy."
            ),
        }

        return implications.get(
            regime,
            "The macro environment contains mixed signals."
        )

    @staticmethod
    def _summary(
        regime: str,
        inflation_bias: str,
        growth_bias: str,
        fed_bias: str,
    ) -> str:

        return (
            f"Macro regime is {regime}. "
            f"Inflation is {inflation_bias.lower()}, "
            f"growth is {growth_bias.lower()}, "
            f"and the Fed signal is {fed_bias.lower()}."
        )
