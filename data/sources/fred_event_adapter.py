from datetime import datetime

from intelligence.event import MarketEvent
from intelligence.indicators import INDICATORS
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

    metadata = INDICATORS.get(series_id)

    if metadata is None:
        raise ValueError(
            f"No indicator metadata found for series: {series_id}"
        )

    return MarketEvent(
        event_name=event_name,
        category=metadata.category,
        source="FRED",
        timestamp=datetime.now(),
        actual=observation.value,
        unit=metadata.unit,
        headline=f"{event_name} latest observation",
        description=(
            f"Latest FRED observation for {event_name}: "
            f"{observation.value} {metadata.unit} "
            f"on {observation.date}."
        ),
        sources=["FRED"],
    )