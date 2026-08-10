from dataclasses import dataclass


@dataclass(frozen=True)
class EconomicImpact:
    """
    Defines the macroeconomic impact of a POSITIVE
    economic surprise for an indicator.

    POSITIVE means the result was economically better
    than expected, taking the indicator's directionality
    into account.
    """

    inflationary_pressure: str
    growth_signal: str
    fed_policy_bias: str


IMPACTS = {
    "UNRATE": EconomicImpact(
        inflationary_pressure="INFLATIONARY",
        growth_signal="POSITIVE",
        fed_policy_bias="HAWKISH",
    ),

    "CPIAUCSL": EconomicImpact(
        inflationary_pressure="INFLATIONARY",
        growth_signal="NEUTRAL",
        fed_policy_bias="HAWKISH",
    ),
}