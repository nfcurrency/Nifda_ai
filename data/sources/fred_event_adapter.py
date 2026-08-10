from datetime import datetime

from intelligence.event import MarketEvent
from data.sources.fred_parser import parse_latest_observation


def observation_to_event(
    data: dict,
    series_id: str,
    event_name: str,
) -> MarketEvent:
    """
    Convert a FRED economic observation into a NIFDA MarketEvent.
    """

    observation = parse_latest_observation(data, series_id)

    return MarketEvent(
        event_name=event_name,
        category="Economic Data",
        source="FRED",
        timestamp=datetime.now(),
        actual=observation.value,
        unit="%",
        headline=f"{event_name} latest observation",
        description=(
            f"Latest FRED observation for {event_name}: "
            f"{observation.value}% on {observation.date}."
        ),
        sources=["FRED"],
    )