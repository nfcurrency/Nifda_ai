from dataclasses import dataclass, field

from intelligence.release import ReleaseResult


@dataclass
class MacroContext:
    """
    Combined macroeconomic context from multiple economic releases.

    MacroContext is responsible for collecting standardized
    ReleaseResult objects. Scoring and regime classification are
    handled by MacroScorer and MacroRegimeAnalyzer.
    """

    releases: list[ReleaseResult] = field(default_factory=list)

    def add_release(self, release: ReleaseResult) -> None:
        """Add a standardized economic release to the context."""
        self.releases.append(release)

    def add_releases(
        self,
        releases: list[ReleaseResult],
    ) -> None:
        """Add multiple standardized releases to the context."""
        self.releases.extend(releases)

    def release_count(self) -> int:
        """Return the number of releases currently in context."""
        return len(self.releases)

    def latest_release(self) -> ReleaseResult | None:
        """Return the most recent release, if one exists."""
        if not self.releases:
            return None

        return max(
            self.releases,
            key=lambda release: release.timestamp,
        )

    def releases_by_indicator(
        self,
        indicator_id: str,
    ) -> list[ReleaseResult]:
        """Return all releases belonging to an indicator."""
        return [
            release
            for release in self.releases
            if release.indicator_id == indicator_id
        ]
