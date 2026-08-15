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

    "PAYEMS": IndicatorMetadata(
        series_id="PAYEMS",
        name="US Nonfarm Payrolls",
        category="Employment",
        unit="Thousands of jobs",
        directionality="DIRECT",
        importance="HIGH",
    ),

    "GDPC1": IndicatorMetadata(
        series_id="GDPC1",
        name="US Real GDP",
        category="Growth",
        unit="Billions of dollars",
        directionality="DIRECT",
        importance="HIGH",
    ),

    "RSAFS": IndicatorMetadata(
        series_id="RSAFS",
        name="US Retail Sales",
        category="Consumption",
        unit="Millions of dollars",
        directionality="DIRECT",
        importance="MEDIUM",
    ),

    "INDPRO": IndicatorMetadata(
        series_id="INDPRO",
        name="US Industrial Production",
        category="Production",
        unit="Index",
        directionality="DIRECT",
        importance="MEDIUM",
    ),

    "FEDFUNDS": IndicatorMetadata(
        series_id="FEDFUNDS",
        name="US Federal Funds Rate",
        category="Monetary Policy",
        unit="%",
        directionality="DIRECT",
        importance="HIGH",
    ),
}
