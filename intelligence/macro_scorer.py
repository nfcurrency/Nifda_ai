from intelligence.macro_context import MacroContext


WEIGHTS = {
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1,
}


class MacroScorer:
    """
    Converts multiple economic releases into an aggregate
    macroeconomic assessment.
    """

    def score(self, context: MacroContext) -> dict:

        inflation_score = 0
        growth_score = 0
        fed_score = 0

        for release in context.releases:

            weight = WEIGHTS.get(
                getattr(release, "importance", "MEDIUM"),
                2,
            )

            inflation_score += self._score_direction(
                release.inflationary_pressure,
                weight,
                positive="INFLATIONARY",
                negative="DEFLATIONARY",
            )

            growth_score += self._score_direction(
                release.growth_signal,
                weight,
                positive="POSITIVE",
                negative="NEGATIVE",
            )

            fed_score += self._score_direction(
                release.fed_policy_bias,
                weight,
                positive="HAWKISH",
                negative="DOVISH",
            )

        return {
            "inflation_score": inflation_score,
            "growth_score": growth_score,
            "fed_score": fed_score,
            "inflation_bias": self._bias(inflation_score),
            "growth_bias": self._bias(growth_score),
            "fed_bias": self._bias(fed_score),
        }

    @staticmethod
    def _score_direction(
        value: str | None,
        weight: int,
        positive: str,
        negative: str,
    ) -> int:

        if value == positive:
            return weight

        if value == negative:
            return -weight

        return 0

    @staticmethod
    def _bias(score: int) -> str:

        if score > 0:
            return "POSITIVE"

        if score < 0:
            return "NEGATIVE"

        return "NEUTRAL"