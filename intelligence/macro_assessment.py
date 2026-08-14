from dataclasses import dataclass

from intelligence.macro_context import MacroContext
from intelligence.macro_regime import MacroRegimeAnalyzer
from intelligence.macro_scorer import MacroScorer


@dataclass
class MacroAssessment:
    """
    Complete macroeconomic assessment produced by NIFDA.
    """

    inflation_score: float
    growth_score: float
    fed_score: float

    inflation_bias: str
    growth_bias: str
    fed_bias: str

    regime: str
    interpretation: str


class MacroAssessmentEngine:
    """
    Combines macro scoring and macro regime analysis
    into one unified assessment.
    """

    def __init__(
        self,
        scorer: MacroScorer | None = None,
        regime_analyzer: MacroRegimeAnalyzer | None = None,
    ):
        self.scorer = scorer or MacroScorer()
        self.regime_analyzer = (
            regime_analyzer or MacroRegimeAnalyzer()
        )

    def assess(self, context: MacroContext) -> MacroAssessment:
        """
        Produce a complete macroeconomic assessment
        from the supplied MacroContext.
        """

        scores = self.scorer.score(context)

        regime_result = self.regime_analyzer.analyze(
            inflation_bias=scores["inflation_bias"],
            growth_bias=scores["growth_bias"],
            fed_bias=scores["fed_bias"],
        )

        return MacroAssessment(
            inflation_score=scores["inflation_score"],
            growth_score=scores["growth_score"],
            fed_score=scores["fed_score"],
            inflation_bias=scores["inflation_bias"],
            growth_bias=scores["growth_bias"],
            fed_bias=scores["fed_bias"],
            regime=regime_result.regime,
            interpretation=regime_result.interpretation,
        )