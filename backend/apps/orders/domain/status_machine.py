class InvalidTransitionError(Exception):
    pass

ALLOWED = {
    "RECEIVED": {"CONFIRMED", "CANCELED"},
    "CONFIRMED": {"DISPATCHED", "CANCELED"},
    "DISPATCHED": {"DELIVERED", "CANCELED"},
    "DELIVERED": set(),
    "CANCELED": set(),
}

def assert_transition(from_status: str, to_status: str) -> None:
    from_status = (from_status or "").upper()
    to_status = (to_status or "").upper()
    if to_status not in ALLOWED.get(from_status, set()):
        raise InvalidTransitionError(f"Invalid transition: {from_status} -> {to_status}")