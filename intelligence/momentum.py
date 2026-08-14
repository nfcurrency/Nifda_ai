def determine_momentum(
    current_change: float,
    previous_change: float,
) -> str:
    """
    Determine whether a macroeconomic metric is
    accelerating, decelerating, or stable.
    """

    if current_change > previous_change:
        return "ACCELERATING"

    if current_change < previous_change:
        return "DECELERATING"

    return "STABLE"