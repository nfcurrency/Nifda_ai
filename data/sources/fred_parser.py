from dataclasses import dataclass


@dataclass
class EconomicObservation:
    series_id: str
    date: str
    value: float
    source: str


def parse_latest_observation(data: dict, series_id: str) -> EconomicObservation:
    observations = data.get("observations", [])

    if not observations:
        raise ValueError(f"No observations returned for {series_id}")

    latest = observations[-1]

    value = latest.get("value")

    if value in (None, ".", ""):
        raise ValueError(
            f"Latest observation for {series_id} has no valid value."
        )

    return EconomicObservation(
        series_id=series_id,
        date=latest["date"],
        value=float(value),
    )