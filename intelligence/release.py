from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ReleaseResult:
    """
    Standardized interpretation of an economic release.
    """

    event_name: str
    indicator_id: str
    timestamp: datetime

    actual: float
    forecast: Optional[float] = None
    previous: Optional[float] = None

    surprise: Optional[float] = None

    economic_direction: Optional[str] = None

    inflationary_pressure: Optional[str] = None
    growth_signal: Optional[str] = None
    fed_policy_bias: Optional[str] = None

    importance: str = "MEDIUM"

    interpretation: Optional[str] = None