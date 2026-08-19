from intelligence.metrics import MetricResult
from intelligence.macro_aggregator import MacroAggregator


def stable_metric(name):
    return MetricResult(
        metric=name,
        current_value=100.0,
        previous_value=100.0,
        change=0.0,
        change_percent=0.0,
        direction="UNCHANGED",
        interpretation=f"{name} is stable.",
        momentum="STABLE",
    )


def main():
    print("===== NIFDA STABLE MACRO STATE TEST =====")
    print()

    aggregator = MacroAggregator()

    snapshot = aggregator.build_snapshot(
        inflation=stable_metric("US Inflation"),
        unemployment=stable_metric("US Unemployment"),
        payrolls=stable_metric("US Payrolls"),
        retail_sales=stable_metric("US Retail Sales"),
        industrial_production=stable_metric(
            "US Industrial Production"
        ),
        gdp=stable_metric("US GDP"),
        fed_policy=stable_metric("Federal Reserve Policy"),
    )

    print("RISING:", snapshot.rising_factors())
    print("FALLING:", snapshot.falling_factors())
    print("ACCELERATING:", snapshot.accelerating_factors())
    print("DECELERATING:", snapshot.decelerating_factors())
    print()
    print("INTERPRETATION:")
    print(snapshot.interpretation())

    assert snapshot.rising_factors() == []
    assert snapshot.falling_factors() == []
    assert snapshot.accelerating_factors() == []
    assert snapshot.decelerating_factors() == []

    assert snapshot.interpretation() == (
        "Macro conditions are broadly stable."
    )

    print()
    print("All stable-state checks passed.")


if __name__ == "__main__":
    main()
