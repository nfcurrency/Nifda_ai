from dataclasses import dataclass


@dataclass
class MetricResult:
    metric: str
    current_value: float
    previous_value: float
    change: float
    change_percent: float
    direction: str
    interpretation: str


def calculate_yoy(
    current_value: float,
    previous_value: float,
    metric_name: str = "CPI",
) -> MetricResult:
    """
    Calculate year-over-year percentage change.

    Example:
        Current CPI = 332.568
        Previous CPI = 321.435

        YoY = ((332.568 - 321.435) / 321.435) * 100
    """

    if previous_value == 0:
        raise ValueError("Previous value cannot be zero.")

    change = current_value - previous_value

    change_percent = (change / previous_value) * 100

    if change > 0:
        direction = "RISING"
        interpretation = (
            f"{metric_name} is rising year-over-year."
        )

    elif change < 0:
        direction = "FALLING"
        interpretation = (
            f"{metric_name} is falling year-over-year."
        )

    else:
        direction = "UNCHANGED"
        interpretation = (
            f"{metric_name} is unchanged year-over-year."
        )

    return MetricResult(
        metric=metric_name,
        current_value=current_value,
        previous_value=previous_value,
        change=change,
        change_percent=change_percent,
        direction=direction,
        interpretation=interpretation,
    )