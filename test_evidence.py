from datetime import datetime, timezone, timedelta

from intelligence.evidence import (
    calculate_recency,
    calculate_surprise_strength,
    calculate_evidence_weight,
)


def main():
    print("===== NIFDA EVIDENCE WEIGHT TEST =====")

    assert calculate_surprise_strength(None) == 0.0
    assert calculate_surprise_strength(0.01) == 0.25
    assert calculate_surprise_strength(0.10) == 0.75
    assert calculate_surprise_strength(0.50) == 1.50

    now = datetime.now(timezone.utc)

    assert calculate_recency(
        timestamp=now,
        now=now,
    ) == 1.0

    assert calculate_recency(
        timestamp=now - timedelta(days=15),
        now=now,
    ) == 0.75

    weight = calculate_evidence_weight(
        "HIGH",
        1.0,
        1.0,
    )

    assert weight == 3.0

    print("Surprise thresholds: PASS")
    print("Recency thresholds: PASS")
    print("Evidence weighting: PASS")
    print("All evidence checks passed.")


if __name__ == "__main__":
    main()
