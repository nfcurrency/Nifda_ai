from dataclasses import dataclass


@dataclass(frozen=True)
class IndicatorMetadata:
    """
    Defines how NIFDA should interpret an economic indicator.
    """

    series_id: str
    name: str
    category: str
    unit: str
    directionality: str
    importance: str