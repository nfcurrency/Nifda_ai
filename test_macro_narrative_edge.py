from intelligence.macro_narrative import MacroNarrativeEngine
from intelligence.macro_assessment import MacroAssessment


def main():
    print("===== NIFDA MACRO NARRATIVE EDGE TEST =====")

    assessment = MacroAssessment(
        inflation_score=0.0,
        growth_score=0.0,
        fed_score=0.0,
        inflation_bias="NEUTRAL",
        growth_bias="NEUTRAL",
        fed_bias="NEUTRAL",
        regime="MIXED",
        interpretation="Mixed macro signals.",
    )

    narrative = MacroNarrativeEngine().generate(assessment)

    assert narrative.regime == "MIXED"

    assert narrative.inflation_view == (
        "Inflation conditions are mixed."
    )

    assert narrative.growth_view == (
        "Growth conditions are mixed."
    )

    assert narrative.policy_view == (
        "Policy conditions provide no clear directional signal."
    )

    assert narrative.market_implication == (
        "The macro environment contains mixed signals."
    )

    print("Regime:", narrative.regime)
    print("Inflation:", narrative.inflation_view)
    print("Growth:", narrative.growth_view)
    print("Policy:", narrative.policy_view)
    print("Market:", narrative.market_implication)
    print("All narrative edge checks passed.")


if __name__ == "__main__":
    main()
