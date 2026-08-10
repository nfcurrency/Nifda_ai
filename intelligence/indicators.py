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
}