from intelligence.metrics import MetricResult
from intelligence.macro_aggregator import MacroAggregator


def metric(
    name,
    current,
    previous,
    direction,
    momentum,
):
    change = current - previous

    return MetricResult(
        metric=name,
        current_value=current,
        previous_value=previous,
        change=change,
        change_percent=(
            (change / previous) * 100
            if previous != 0
            else 0.0
        ),
        direction=direction,
        interpretation=f"{name} test result.",
        momentum=momentum,
    )


def main():
    print("===== NIFDA MACRO STATE INTELLIGENCE TEST =====")
    print()

    inflation = metric(
        "US Inflation",
        3.0,
        3.5,
        "FALLING",
        "DECELERATING",
    )

    unemployment = metric(
        "US Unemployment",
        4.3,
        4.1,
        "RISING",
        "ACCELERATING",
    )

    payrolls = metric(
        "US Payrolls",
        180.0,
        150.0,
        "RISING",
        "ACCELERATING",
    )

    retail_sales = metric(
        "US Retail Sales",
        3.0,
        2.5,
        "RISING",
        "DECELERATING",
    )

    industrial_production = metric(
        "US Industrial Production",
        1.5,
        1.0,
        "RISING",
        "STABLE",
    )

    gdp = metric(
        "US GDP",
        2.5,
        2.0,
        "RISING",
        "ACCELERATING",
    )

    fed_policy = metric(
        "Federal Reserve Policy",
        4.5,
        4.75,
        "FALLING",
        "DECELERATING",
    )

    aggregator = MacroAggregator()

    snapshot = aggregator.build_snapshot(
        inflation=inflation,
        unemployment=unemployment,
        payrolls=payrolls,
        retail_sales=retail_sales,
        industrial_production=industrial_production,
        gdp=gdp,
        fed_policy=fed_policy,
    )

    print("MACRO STATES")
    print("-" * 60)

    for state in snapshot.states():
        print(
            f"{state.factor}: "
            f"{state.direction} | "
            f"{state.momentum}"
        )

    print()
    print("RISING FACTORS")
    print(snapshot.rising_factors())

    print()
    print("FALLING FACTORS")
    print(snapshot.falling_factors())

    print()
    print("ACCELERATING FACTORS")
    print(snapshot.accelerating_factors())

    print()
    print("DECELERATING FACTORS")
    print(snapshot.decelerating_factors())

    print()
    print("MACRO INTERPRETATION")
    print("-" * 60)
    print(snapshot.interpretation())


if __name__ == "__main__":
    main()
