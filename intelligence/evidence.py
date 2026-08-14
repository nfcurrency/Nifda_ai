from datetime import datetime, timezone


IMPORTANCE_WEIGHTS = {
    "HIGH": 3.0,
    "MEDIUM": 2.0,
    "LOW": 1.0,
}


def calculate_recency(
    timestamp: datetime,
    now: datetime | None = None,
) -> float:
    """
    Calculate a recency multiplier.

    Recent releases receive more influence than older releases.

    <= 7 days:   1.00
    <= 30 days:  0.75
    <= 90 days:  0.50
    > 90 days:   0.25
    """

    if now is None:
        now = datetime.now(timezone.utc)

    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)

    age_days = max(
        (now - timestamp).total_seconds() / 86400,
        0,
    )

    if age_days <= 7:
        return 1.0

    if age_days <= 30:
        return 0.75

    if age_days <= 90:
        return 0.50

    return 0.25


def calculate_surprise_strength(
    surprise: float | None,
) -> float:
    """
    Convert surprise magnitude into an evidence multiplier.

    This is a V1 heuristic. It measures the magnitude of the
    surprise without assuming that different indicators have
    identical statistical distributions.
    """

    if surprise is None:
        return 0.0

    magnitude = abs(surprise)

    if magnitude < 0.05:
        return 0.25

    if magnitude < 0.10:
        return 0.50

    if magnitude < 0.25:
        return 0.75

    if magnitude < 0.50:
        return 1.00

    return 1.50


def calculate_evidence_weight(
    importance: str,
    surprise_strength: float,
    recency_multiplier: float,
) -> float:
    """
    Combine importance, surprise strength, and recency
    into a single evidence weight.
    """

    importance_weight = IMPORTANCE_WEIGHTS.get(
        importance.upper(),
        2.0,
    )

    return (
        importance_weight
        * surprise_strength
        * recency_multiplier
    )