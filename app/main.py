from datetime import datetime

from intelligence.event import MarketEvent
from data.collector import RawData


def main():
    print("NIFDA AI is online.")
    print("Market Intelligence System — V0.3")
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