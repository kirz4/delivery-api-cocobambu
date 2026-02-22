import pytest

from apps.orders.domain.status_machine import assert_transition, InvalidTransitionError


@pytest.mark.parametrize(
    "from_status,to_status",
    [
        ("RECEIVED", "CONFIRMED"),
        ("RECEIVED", "CANCELED"),
        ("CONFIRMED", "DISPATCHED"),
        ("CONFIRMED", "CANCELED"),
        ("DISPATCHED", "DELIVERED"),
        ("DISPATCHED", "CANCELED"),
        # normalização (lowercase -> uppercase)
        ("received", "confirmed"),
    ],
)
def test_valid_transitions(from_status, to_status):
    assert_transition(from_status, to_status)  # não deve levantar exceção


@pytest.mark.parametrize(
    "from_status,to_status",
    [
        ("DELIVERED", "CONFIRMED"),
        ("CANCELED", "DISPATCHED"),
        ("RECEIVED", "DELIVERED"),
        ("CONFIRMED", "RECEIVED"),
        ("DISPATCHED", "CONFIRMED"),
        ("UNKNOWN", "CONFIRMED"),
    ],
)
def test_invalid_transitions(from_status, to_status):
    with pytest.raises(InvalidTransitionError):
        assert_transition(from_status, to_status)