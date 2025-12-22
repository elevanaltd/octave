"""Repair log structures (P1.6)."""

from dataclasses import dataclass
from enum import Enum


class RepairTier(Enum):
    """Repair classification tiers."""

    NORMALIZATION = "NORMALIZATION"  # Always applied
    REPAIR = "REPAIR"  # Only when fix=true
    FORBIDDEN = "FORBIDDEN"  # Never automatic


@dataclass
class RepairEntry:
    """Single repair log entry."""

    rule_id: str
    before: str
    after: str
    tier: RepairTier
    safe: bool
    semantics_changed: bool


@dataclass
class RepairLog:
    """Complete repair log."""

    repairs: list[RepairEntry]

    def add(
        self,
        rule_id: str,
        before: str,
        after: str,
        tier: RepairTier,
        safe: bool = True,
        semantics_changed: bool = False,
    ) -> None:
        """Add a repair entry."""
        self.repairs.append(RepairEntry(rule_id, before, after, tier, safe, semantics_changed))

    def has_repairs(self) -> bool:
        """Check if any repairs were made."""
        return len(self.repairs) > 0
