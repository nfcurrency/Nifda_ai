from intelligence.macro_regime import MacroRegimeAnalyzer


def main():
    print("===== NIFDA MACRO REGIME TEST =====")

    analyzer = MacroRegimeAnalyzer()

    cases = [
        ("POSITIVE", "NEGATIVE", "HAWKISH", "STAGFLATIONARY"),
        ("NEGATIVE", "NEGATIVE", "DOVISH", "DISINFLATIONARY_SLOWDOWN"),
        ("POSITIVE", "POSITIVE", "HAWKISH", "REFLATIONARY"),
        ("NEGATIVE", "POSITIVE", "DOVISH", "GOLDILOCKS"),
        ("NEUTRAL", "NEUTRAL", "HAWKISH", "HAWKISH"),
        ("NEUTRAL", "NEUTRAL", "DOVISH", "DOVISH"),
        ("NEUTRAL", "NEUTRAL", "NEUTRAL", "MIXED"),
    ]

    for inflation, growth, fed, expected in cases:
        result = analyzer.analyze(
            inflation_bias=inflation,
            growth_bias=growth,
            fed_bias=fed,
        )

        print(
            f"{inflation} | {growth} | {fed} -> "
            f"{result.regime}"
        )

        assert result.regime == expected

    print("All regime checks passed.")


if __name__ == "__main__":
    main()
