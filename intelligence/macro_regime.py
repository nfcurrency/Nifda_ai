from dataclasses import dataclass


@dataclass
class MacroRegimeResult:
    """
    Overall macroeconomic regime derived from
    inflation, growth, and Fed policy signals.
    """

    regime: str
    inflation_bias: str
    growth_bias: str
    fed_bias: str
    interpretation: str


class MacroRegimeAnalyzer:
    """
    Converts aggregate macro biases into a broader
    macroeconomic regime.
    """

    def analyze(
        self,
        inflation_bias: str,
        growth_bias: str,
        fed_bias: str,
    ) -> MacroRegimeResult:

        regime = self._determine_regime(
            inflation_bias,
            growth_bias,
            fed_bias,
        )

        interpretation = self._interpret(
            regime,
            inflation_bias,
            growth_bias,
            fed_bias,
        )

        return MacroRegimeResult(
            regime=regime,
            inflation_bias=inflation_bias,
            growth_bias=growth_bias,
            fed_bias=fed_bias,
            interpretation=interpretation,
        )

    @staticmethod
    def _determine_regime(
        inflation_bias: str,
        growth_bias: str,
        fed_bias: str,
    ) -> str:

        # High inflation + weak growth
        if (
            inflation_bias == "POSITIVE"
            and growth_bias == "NEGATIVE"
        ):
            return "STAGFLATIONARY"

        # Low inflation + weak growth
        if (
            inflation_bias == "NEGATIVE"
            and growth_bias == "NEGATIVE"
        ):
            return "DISINFLATIONARY_SLOWDOWN"

        # Strong growth + inflation
        if (
            inflation_bias == "POSITIVE"
            and growth_bias == "POSITIVE"
        ):
            return "REFLATIONARY"

        # Strong growth + lower inflation
        if (
            inflation_bias == "NEGATIVE"
            and growth_bias == "POSITIVE"
        ):
            return "GOLDILOCKS"

        # Policy direction can provide additional context
        if fed_bias == "HAWKISH":
            return "HAWKISH"

        if fed_bias == "DOVISH":
            return "DOVISH"

        return "MIXED"

    @staticmethod
    def _interpret(
        regime: str,
        inflation_bias: str,
        growth_bias: str,
        fed_bias: str,
    ) -> str:

        interpretations = {
            "STAGFLATIONARY": (
                "Inflationary pressure is elevated while "
                "growth conditions are weakening. This creates "
                "a difficult policy environment for the Fed."
            ),

            "DISINFLATIONARY_SLOWDOWN": (
                "Inflationary pressure is easing while growth "
                "is weakening. This environment can increase "
                "the case for monetary easing."
            ),

            "REFLATIONARY": (
                "Both inflationary pressure and growth are "
                "positive, suggesting a reflationary environment."
            ),

            "GOLDILOCKS": (
                "Growth is positive while inflationary pressure "
                "is easing, creating a relatively favorable "
                "macro environment."
            ),

            "HAWKISH": (
                "The aggregate evidence currently points toward "
                "a hawkish monetary-policy environment."
            ),

            "DOVISH": (
                "The aggregate evidence currently points toward "
                "a dovish monetary-policy environment."
            ),

            "MIXED": (
                "The macroeconomic signals are mixed and do not "
                "currently point toward a dominant regime."
            ),
        }

        return interpretations.get(
            regime,
            (
                f"Macro signals are mixed. "
                f"Inflation: {inflation_bias}. "
                f"Growth: {growth_bias}. "
                f"Fed: {fed_bias}."
            ),
        )