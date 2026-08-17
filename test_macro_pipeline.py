from datetime import datetime, timezone

from intelligence.event import MarketEvent
from intelligence.release_analyzer import ReleaseAnalyzer
from intelligence.macro_context import MacroContext
from intelligence.macro_assessment import MacroAssessmentEngine
from intelligence.macro_narrative import MacroNarrativeEngine


def main():
    print("===== NIFDA MACRO PIPELINE SMOKE TEST =====")

    event = MarketEvent(
        event_name="US Unemployment Rate",
        category="Employment",
        source="BLS",
        timestamp=datetime.now(timezone.utc),
        actual=4.3,
        forecast=4.2,
        previous=4.1,
        unit="%",
    )

    release = ReleaseAnalyzer().analyze(
        event,
        "UNRATE",
    )

    context = MacroContext()
    context.add_release(release)

    assessment = MacroAssessmentEngine().assess(context)
    narrative = MacroNarrativeEngine().generate(assessment)

    assert context.release_count() == 1
    assert release.economic_direction == "NEGATIVE"
    assert release.inflationary_pressure == "DEFLATIONARY"
    assert release.growth_signal == "NEGATIVE"
    assert release.fed_policy_bias == "DOVISH"
    assert assessment.regime == "DISINFLATIONARY_SLOWDOWN"
    assert narrative.regime == assessment.regime
    assert narrative.summary

    print("Release:", release.economic_direction)
    print("Inflation:", release.inflationary_pressure)
    print("Growth:", release.growth_signal)
    print("Fed:", release.fed_policy_bias)
    print("Regime:", assessment.regime)
    print("Narrative generated: YES")
    print("Full pipeline check passed.")


if __name__ == "__main__":
    main()
