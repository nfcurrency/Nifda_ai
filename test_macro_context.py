from datetime import datetime, timedelta

from intelligence.event import MarketEvent
from intelligence.release_analyzer import ReleaseAnalyzer
from intelligence.macro_context import MacroContext
from intelligence.macro_assessment import MacroAssessmentEngine


def build_event(
    name,
    actual,
    forecast,
    indicator_id,
    hours_ago,
):
    return (
        MarketEvent(
            event_name=name,
            category="Macro",
            source="TEST",
            timestamp=datetime.now() - timedelta(hours=hours_ago),
            actual=actual,
            forecast=forecast,
        ),
        indicator_id,
    )


def main():
    print("===== NIFDA MULTI-RELEASE MACRO TEST =====")
    print()

    analyzer = ReleaseAnalyzer()
    context = MacroContext()

    test_events = [
        build_event(
            "US Unemployment Rate",
            4.3,
            4.2,
            "UNRATE",
            1,
        ),
        build_event(
            "US Consumer Price Index",
            3.5,
            3.2,
            "CPIAUCSL",
            2,
        ),
        build_event(
            "US Nonfarm Payrolls",
            180.0,
            150.0,
            "PAYEMS",
            3,
        ),
        build_event(
            "US Real GDP",
            2.5,
            2.0,
            "GDPC1",
            4,
        ),
        build_event(
            "US Retail Sales",
            3.0,
            2.5,
            "RSAFS",
            5,
        ),
        build_event(
            "US Industrial Production",
            1.5,
            1.0,
            "INDPRO",
            6,
        ),
        build_event(
            "US Federal Funds Rate",
            4.5,
            4.25,
            "FEDFUNDS",
            7,
        ),
    ]

    print("ADDING RELEASES")
    print("-" * 60)

    for event, indicator_id in test_events:
        release = analyzer.analyze(
            event,
            indicator_id,
        )

        context.add_release(release)

        print(
            f"{indicator_id}: "
            f"{release.economic_direction} | "
            f"{release.inflationary_pressure} | "
            f"{release.growth_signal} | "
            f"{release.fed_policy_bias}"
        )

    print()
    print(f"Release count: {context.release_count()}")

    latest = context.latest_release()

    if latest:
        print(
            f"Latest release: "
            f"{latest.indicator_id} - "
            f"{latest.event_name}"
        )

    print()
    print("INDICATOR COUNTS")
    print("-" * 60)

    for indicator_id in [
        "UNRATE",
        "CPIAUCSL",
        "PAYEMS",
        "GDPC1",
        "RSAFS",
        "INDPRO",
        "FEDFUNDS",
    ]:
        print(
            f"{indicator_id}: "
            f"{len(context.releases_by_indicator(indicator_id))}"
        )

    print()
    print("MACRO ASSESSMENT")
    print("-" * 60)

    engine = MacroAssessmentEngine()
    assessment = engine.assess(context)

    print(f"Inflation Score: {assessment.inflation_score}")
    print(f"Growth Score: {assessment.growth_score}")
    print(f"Fed Score: {assessment.fed_score}")
    print(f"Inflation Bias: {assessment.inflation_bias}")
    print(f"Growth Bias: {assessment.growth_bias}")
    print(f"Fed Bias: {assessment.fed_bias}")
    print(f"Regime: {assessment.regime}")
    print()
    print("Interpretation:")
    print(assessment.interpretation)


if __name__ == "__main__":
    main()
