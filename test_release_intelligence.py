from datetime import datetime

from intelligence.event import MarketEvent
from intelligence.release_analyzer import ReleaseAnalyzer
from intelligence.indicators import INDICATORS


def main():
    analyzer = ReleaseAnalyzer()

    print("===== NIFDA RELEASE INTELLIGENCE TEST =====")
    print()

    test_values = {
        "UNRATE": (4.3, 4.2),
        "CPIAUCSL": (3.5, 3.2),
        "PAYEMS": (180.0, 150.0),
        "GDPC1": (2.5, 2.0),
        "RSAFS": (3.0, 2.5),
        "INDPRO": (1.5, 1.0),
        "FEDFUNDS": (4.5, 4.25),
    }

    for indicator_id, (actual, forecast) in test_values.items():

        metadata = INDICATORS[indicator_id]

        event = MarketEvent(
            event_name=metadata.name,
            category=metadata.category,
            source="TEST",
            timestamp=datetime.now(),
            actual=actual,
            forecast=forecast,
            previous=None,
            unit=metadata.unit,
        )

        result = analyzer.analyze(
            event,
            indicator_id,
        )

        print(f"--- {indicator_id} ---")
        print(f"Indicator: {metadata.name}")
        print(f"Actual: {actual}")
        print(f"Forecast: {forecast}")
        print(f"Economic Direction: {result.economic_direction}")
        print(f"Inflation Pressure: {result.inflationary_pressure}")
        print(f"Growth Signal: {result.growth_signal}")
        print(f"Fed Policy Bias: {result.fed_policy_bias}")
        print(f"Importance: {result.importance}")
        print(f"Interpretation: {result.interpretation}")
        print()


if __name__ == "__main__":
    main()
