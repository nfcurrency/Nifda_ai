from dataclasses import dataclass, field

from intelligence.release import ReleaseResult


@dataclass
class MacroContext:
    """
    Combined macroeconomic context from multiple releases.
    """

    releases: list[ReleaseResult] = field(default_factory=list)

    inflation_pressure: str = "NEUTRAL"
    growth_signal: str = "NEUTRAL"
    fed_policy_bias: str = "NEUTRAL"

    def add_release(self, release: ReleaseResult) -> None:
        self.releases.append(release)

    def release_count(self) -> int:
        return len(self.releases)