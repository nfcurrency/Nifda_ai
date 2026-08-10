from datetime import datetime

from data.collector import DataCollector, RawData
from data.sources.fred import FREDClient


class FREDCollector(DataCollector):
    """
    Collects economic time-series data from FRED
    and converts it into NIFDA's RawData format.
    """

    def __init__(self, series_id: str):
        self.series_id = series_id
        self.client = FREDClient()

    def collect(self) -> RawData:
        data = self.client.get_series(self.series_id)

        return RawData(
            source="FRED",
            data_type="economic_series",
            timestamp=datetime.now(),
            payload=data,
        )