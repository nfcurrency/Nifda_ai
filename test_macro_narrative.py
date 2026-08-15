from datetime import datetime

from intelligence.event import MarketEvent
from intelligence.release_analyzer import ReleaseAnalyzer
from intelligence.macro_context import MacroContext
from intelligence.macro_assessment import MacroAssessmentEngine
from intelligence.macro_narrative import MacroNarrativeEngine


def build_release(
    event_name,
    indicator_id,
    actual,
    forecast,
    previous,
):
    event = MarketEvent(
        event_name=event_name,
        category="Macro",
        source="TEST",
        timestamp=datetime.now(),
        actual=actual,
        forecast=forecast,
        previous=previous,
        unit="%",
        headline=event_name,
    )

    return ReleaseAnalyzer().analyze(
        event,
        indicator_id,
    )


def main():
    print("===== NIFDA MACRO NARRATIVE TEST =====")
    print()

    releases = [
        build_release(
            "US Unemployment Rate",
            "UNRATE",
            4.3,
            4.2,
            4.1,
        ),
        build_release(
            "US Consumer Price Index",
            "CPIAUCSL",
            3.5,
            3.2,
            3.1,
        ),
        build_release(
            "US Nonfarm Payrolls",
            "PAYEMS",
            180.0,
            150.0,
            140.0,
        ),
        build_release(
            "US Real GDP",
            "GDPC1",
            2.5,
            2.0,
            1.8,
        ),
    ]

    context = MacroContext()

    for release in releases:
        context.add_release(release)

    assessment = MacroAssessmentEngine().assess(context)

    narrative = MacroNarrativeEngine().generate(
        assessment
    )

    print("MACRO ASSESSMENT")
    print("-" * 60)
    print(f"Inflation Score: {assessment.inflation_score}")
    print(f"Growth Score: {assessment.growth_score}")
    print(f"Fed Score: {assessment.fed_score}")
    print(f"Inflation Bias: {assessment.inflation_bias}")
    print(f"Growth Bias: {assessment.growth_bias}")
    print(f"Fed Bias: {assessment.fed_bias}")
    print(f"Regime: {assessment.regime}")

    print()
    print("MACRO NARRATIVE")
    print("-" * 60)
    print(f"Summary: {narrative.summary}")
    print(f"Inflation View: {narrative.inflation_view}")
    print(f"Growth View: {narrative.growth_view}")
    print(f"Policy View: {narrative.policy_view}")
    print(f"Market Implication: {narrative.market_implication}")


if __name__ == "__main__":
    main()
