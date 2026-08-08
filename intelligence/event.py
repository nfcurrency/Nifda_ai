from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class MarketEvent:
    """
    Standardized representation of a market-relevant event.
    """

    event_name: str
    category: str
    source: str
    timestamp: datetime

    actual: Optional[float] = None
    forecast: Optional[float] = None
    previous: Optional[float] = None

    unit: Optional[str] = None

    headline: Optional[str] = None
    description: Optional[str] = None

    sources: list[str] = field(default_factory=list)

    def surprise(self) -> Optional[float]:
        """
        Calculate the difference between actual and forecast.
        """

        if self.actual is None or self.forecast is None:
            return None

        return self.actual - self.forecast