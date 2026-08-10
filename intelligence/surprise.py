from dataclasses import dataclass
from typing import Optional

from intelligence.event import MarketEvent
from intelligence.indicators import INDICATORS


@dataclass
class SurpriseResult:
    """
    Interprets an economic release relative to expectations.
    """

    numerical_surprise: Optional[float]
    direction: str
    interpretation: str


def calculate_surprise(
    event: MarketEvent,
    series_id: str,
) -> SurpriseResult:
    """
    Calculate and interpret an economic surprise using
    indicator metadata.
    """

    if event.actual is None or event.forecast is None:
        return SurpriseResult(
            numerical_surprise=None,
            direction="UNKNOWN",
            interpretation="Insufficient data to calculate surprise.",
        )

    metadata = INDICATORS.get(series_id)

    if metadata is None:
        return SurpriseResult(
            numerical_surprise=None,
            direction="UNKNOWN",
            interpretation=f"No metadata found for series: {series_id}",
        )

    numerical_surprise = event.actual - event.forecast

    if numerical_surprise == 0:
        return SurpriseResult(
            numerical_surprise=0.0,
            direction="INLINE",
            interpretation="Actual result matched expectations.",
        )

    if metadata.directionality == "INVERSE":
        if numerical_surprise > 0:
            direction = "NEGATIVE"
            interpretation = (
                "Actual result was worse than expected "
                "based on the indicator's inverse directionality."
            )
        else:
            direction = "POSITIVE"
            interpretation = (
                "Actual result was better than expected "
                "based on the indicator's inverse directionality."
            )

    elif metadata.directionality == "DIRECT":
        if numerical_surprise > 0:
            direction = "POSITIVE"
            interpretation = (
                "Actual result was better than expected "
                "based on the indicator's direct directionality."
            )
        else:
            direction = "NEGATIVE"
            interpretation = (
                "Actual result was worse than expected "
                "based on the indicator's direct directionality."
            )

    else:
        direction = "UNKNOWN"
        interpretation = (
            "Indicator directionality is not defined."
        )

    return SurpriseResult(
        numerical_surprise=numerical_surprise,
        direction=direction,
        interpretation=interpretation,
    )