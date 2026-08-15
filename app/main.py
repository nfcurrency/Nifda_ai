from datetime import datetime

from intelligence.event import MarketEvent
from intelligence.release_analyzer import ReleaseAnalyzer
from intelligence.macro_context import MacroContext
from intelligence.macro_assessment import MacroAssessmentEngine
from intelligence.macro_narrative import MacroNarrativeEngine
from data.collector import RawData


def main():
    print("NIFDA AI is online.")
    print("Market Intelligence System - V0.4")
    print()

    unemployment = MarketEvent(
        event_name="US Unemployment Rate",
        category="Employment",
        source="BLS",
        timestamp=datetime.now(),
        actual=4.3,
        forecast=4.2,
        previous=4.1,
        unit="%",
        headline="US unemployment rate rises above expectations",
    )

    print("EVENT")
    print(f"Name: {unemployment.event_name}")
    print(f"Actual: {unemployment.actual}%")
    print(f"Forecast: {unemployment.forecast}%")
    print(f"Previous: {unemployment.previous}%")

    surprise = unemployment.surprise()

    print(f"Surprise: {surprise:+.2f} percentage points")

    analyzer = ReleaseAnalyzer()

    release = analyzer.analyze(
        unemployment,
        "UNRATE",
    )

    context = MacroContext()
    context.add_release(release)

    assessment = MacroAssessmentEngine().assess(context)

    narrative = MacroNarrativeEngine().generate(
        assessment
    )

    print()
    print("RELEASE INTELLIGENCE")
    print(f"Direction: {release.economic_direction}")
    print(f"Inflation Pressure: {release.inflationary_pressure}")
    print(f"Growth Signal: {release.growth_signal}")
    print(f"Fed Policy Bias: {release.fed_policy_bias}")
    print(f"Importance: {release.importance}")

    print()
    print("MACRO ASSESSMENT")
    print(f"Inflation Score: {assessment.inflation_score}")
    print(f"Growth Score: {assessment.growth_score}")
    print(f"Fed Score: {assessment.fed_score}")
    print(f"Inflation Bias: {assessment.inflation_bias}")
    print(f"Growth Bias: {assessment.growth_bias}")
    print(f"Fed Bias: {assessment.fed_bias}")
    print(f"Regime: {assessment.regime}")

    print()
    print("MACRO NARRATIVE")
    print(narrative.summary)
    print(narrative.inflation_view)
    print(narrative.growth_view)
    print(narrative.policy_view)
    print(f"Market Implication: {narrative.market_implication}")

    raw_data = RawData(
        source="BLS",
        data_type="economic_release",
        timestamp=datetime.now(),
        payload={
            "event": "US Unemployment Rate",
            "actual": 4.3,
            "forecast": 4.2,
            "previous": 4.1,
        },
    )

    print()
    print("RAW DATA")
    print(f"Source: {raw_data.source}")
    print(f"Type: {raw_data.data_type}")
    print(f"Timestamp: {raw_data.timestamp}")
    print(f"Payload: {raw_data.payload}")


if __name__ == "__main__":
    main()
