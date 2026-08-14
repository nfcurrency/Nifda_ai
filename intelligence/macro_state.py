from dataclasses import dataclass


@dataclass
class MacroState:
    """
    Represents the current state and momentum
    of a macroeconomic factor.
    """

    factor: str
    current_value: float
    direction: str
    momentum: str
    interpretation: str