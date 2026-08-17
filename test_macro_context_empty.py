from intelligence.macro_context import MacroContext


def main():
    print("===== NIFDA EMPTY MACRO CONTEXT TEST =====")

    context = MacroContext()

    assert context.releases_by_indicator("UNRATE") == []
    assert context.latest_release() is None
    assert context.release_count() == 0

    print("UNRATE releases:", context.releases_by_indicator("UNRATE"))
    print("Latest release:", context.latest_release())
    print("Release count:", context.release_count())
    print("All empty-context checks passed.")


if __name__ == "__main__":
    main()
