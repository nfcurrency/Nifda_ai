from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class RawData:
    source: str
    data_type: str
    timestamp: datetime
    payload: Any


class DataCollector:
    """
    Base interface for collecting external market intelligence.
    """

    def collect(self) -> RawData:
        raise NotImplementedError(
            "Each data source must implement its own collector."
        )