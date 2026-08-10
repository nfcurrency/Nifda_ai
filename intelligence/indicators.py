from intelligence.indicator import IndicatorMetadata


INDICATORS = {
    "UNRATE": IndicatorMetadata(
        series_id="UNRATE",
        name="US Unemployment Rate",
        category="Employment",
        unit="%",
        directionality="INVERSE",
        importance="HIGH",
    ),

    "CPIAUCSL": IndicatorMetadata(
        series_id="CPIAUCSL",
        name="US Consumer Price Index",
        category="Inflation",
        unit="Index",
        directionality="DIRECT",
        importance="HIGH",
    ),
}