from dataclasses import dataclass


@dataclass
class EconomicObservation:
    series_id: str
    date: str
    value: float
    source: str


def parse_latest_observation(
    data: dict,
    series_id: str,
) -> EconomicObservation:
    """
    Parse the latest valid observation from a FRED response.
    """

    observations = data.get("observations", [])

    if not observations:
        raise ValueError(f"No observations returned for {series_id}")

    for observation in reversed(observations):
        value = observation.get("value")

        if value not in (None, ".", ""):
            return EconomicObservation(
                series_id=series_id,
                date=observation["date"],
                value=float(value),
                source="FRED",
            )

    raise ValueError(
        f"No valid observations found for {series_id}"
    )


def parse_observations(
    data: dict,
    series_id: str,
) -> list[EconomicObservation]:
    """
    Parse all valid observations from a FRED response.
    """

    observations = data.get("observations", [])

    if not observations:
        raise ValueError(f"No observations returned for {series_id}")

    parsed = []

    for observation in observations:
        value = observation.get("value")

        if value in (None, ".", ""):
            continue

        parsed.append(
            EconomicObservation(
                series_id=series_id,
                date=observation["date"],
                value=float(value),
                source="FRED",
            )
        )

    if not parsed:
        raise ValueError(
            f"No valid observations found for {series_id}"
        )

    return parsed