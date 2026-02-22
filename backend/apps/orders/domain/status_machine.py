from __future__ import annotations

from typing import Dict, FrozenSet, List, Optional


class InvalidTransitionError(Exception):
    """Raised when trying to move an order from one status to another invalid status."""
    pass


# Status válidos do domínio
STATUSES: FrozenSet[str] = frozenset(
    {"RECEIVED", "CONFIRMED", "DISPATCHED", "DELIVERED", "CANCELED"}
)

# Transições permitidas
ALLOWED_TRANSITIONS: Dict[str, FrozenSet[str]] = {
    "RECEIVED": frozenset({"CONFIRMED", "CANCELED"}),
    "CONFIRMED": frozenset({"DISPATCHED", "CANCELED"}),
    "DISPATCHED": frozenset({"DELIVERED", "CANCELED"}),
    "DELIVERED": frozenset(),
    "CANCELED": frozenset(),
}


def normalize_status(status: Optional[str]) -> str:
    """Normalize status string to canonical uppercase representation."""
    return (status or "").strip().upper()


def allowed_next_statuses(current_status: Optional[str]) -> List[str]:
    """
    Returns the allowed next statuses (sorted) from the given current status.
    Useful for UI dropdowns/buttons.
    """
    cur = normalize_status(current_status)
    if cur not in STATUSES:
        return []
    return sorted(ALLOWED_TRANSITIONS.get(cur, frozenset()))


def assert_transition(from_status: Optional[str], to_status: Optional[str]) -> None:
    """
    Validates whether a transition is allowed.
    Raises InvalidTransitionError when invalid.
    """
    cur = normalize_status(from_status)
    nxt = normalize_status(to_status)

    if not nxt:
        raise InvalidTransitionError("Target status is required.")

    if cur not in STATUSES:
        raise InvalidTransitionError(f"Unknown current status: {cur!r}")

    if nxt not in STATUSES:
        raise InvalidTransitionError(f"Unknown target status: {nxt!r}")

    if cur == nxt:
        raise InvalidTransitionError(f"Invalid transition: {cur} -> {nxt}")

    allowed = ALLOWED_TRANSITIONS.get(cur, frozenset())
    if nxt not in allowed:
        raise InvalidTransitionError(f"Invalid transition: {cur} -> {nxt}")
    
def allowed_next_statuses(from_status: str) -> list[str]:
    from_status = (from_status or "").upper()
    return sorted(list(ALLOWED_TRANSITIONS.get(from_status, set())))