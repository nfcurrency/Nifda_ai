from intelligence.macro_context import MacroContext
from intelligence.evidence import (
    calculate_recency,
    calculate_surprise_strength,
    calculate_evidence_weight,
)


class MacroScorer:
    """
    Converts multiple economic releases into an aggregate
    macroeconomic assessment using evidence strength.
    """

    def score(self, context: MacroContext) -> dict:
        inflation_score = 0.0
        growth_score = 0.0
        fed_score = 0.0

        for release in context.releases:
            surprise_strength = calculate_surprise_strength(
                release.surprise
            )

            recency_multiplier = calculate_recency(
                release.timestamp
            )

            evidence_weight = calculate_evidence_weight(
                release.importance,
                surprise_strength,
                recency_multiplier,
            )

            inflation_score += self._score_direction(
                release.inflationary_pressure,
                evidence_weight,
                positive="INFLATIONARY",
                negative="DEFLATIONARY",
            )

            growth_score += self._score_direction(
                release.growth_signal,
                evidence_weight,
                positive="POSITIVE",
                negative="NEGATIVE",
            )

            fed_score += self._score_direction(
                release.fed_policy_bias,
                evidence_weight,
                positive="HAWKISH",
                negative="DOVISH",
            )

        return {
            "inflation_score": round(inflation_score, 2),
            "growth_score": round(growth_score, 2),
            "fed_score": round(fed_score, 2),
            "inflation_bias": self._bias(inflation_score),
            "growth_bias": self._bias(growth_score),
            "fed_bias": self._policy_bias(fed_score),
        }

    @staticmethod
    def _policy_bias(score: float) -> str:
        if score > 0:
            return "HAWKISH"

        if score < 0:
            return "DOVISH"

        return "NEUTRAL"

    @staticmethod
    def _score_direction(
        value: str | None,
        weight: float,
        positive: str,
        negative: str,
    ) -> float:
        if value == positive:
            return weight

        if value == negative:
            return -weight

        return 0.0

    @staticmethod
    def _bias(score: float) -> str:
        if score > 0:
            return "POSITIVE"

        if score < 0:
            return "NEGATIVE"

        return "NEUTRAL"
