import pytest

from apps.orders.domain.status_machine import InvalidTransitionError
from apps.orders.services import order_service as order_service_module
from apps.orders.services.order_service import OrderService


class FakeStorage:
    def __init__(self, initial):
        self._data = initial
        self.written = None

    def read(self):
        return self._data

    def write_atomic(self, data):
        self.written = data
        self._data = data


def _order_row(order_id="order-1", last="RECEIVED"):
    return {
        "store_id": "store-1",
        "order_id": order_id,
        "order": {
            "last_status_name": last,
            "statuses": [],
            "total_price": 10.0,
            "store": {"name": "Loja", "id": "store-1"},
            "customer": {"name": "Cliente", "temporary_phone": "+5500000000"},
            "items": [],
            "payments": [],
            "created_at": 1770000000000,
            "delivery_address": {},
        },
    }


def test_change_status_updates_last_status_and_appends_event(monkeypatch):
    storage = FakeStorage([_order_row(last="RECEIVED")])

    # patcha a classe JsonStorage usada dentro do OrderService
    monkeypatch.setattr(order_service_module, "JsonStorage", lambda: storage)

    svc = OrderService()
    updated, err = svc.change_status("order-1", "CONFIRMED", origin="STORE")

    assert err is None
    assert updated["order"]["last_status_name"] == "CONFIRMED"
    assert len(updated["order"]["statuses"]) == 1

    event = updated["order"]["statuses"][0]
    assert event["name"] == "CONFIRMED"
    assert event["order_id"] == "order-1"
    assert event["origin"] == "STORE"
    assert isinstance(event["created_at"], int)

    # confirma que gravou
    assert storage.written is not None
    assert isinstance(storage.written, list)


def test_change_status_returns_not_found(monkeypatch):
    storage = FakeStorage([_order_row(order_id="other")])
    monkeypatch.setattr(order_service_module, "JsonStorage", lambda: storage)

    svc = OrderService()
    updated, err = svc.change_status("missing", "CONFIRMED", origin="STORE")

    assert updated is None
    assert err == "not_found"


def test_change_status_returns_invalid_storage_when_not_list(monkeypatch):
    storage = FakeStorage({"orders": []})  # formato inválido p/ service atual
    monkeypatch.setattr(order_service_module, "JsonStorage", lambda: storage)

    svc = OrderService()
    updated, err = svc.change_status("order-1", "CONFIRMED", origin="STORE")

    assert updated is None
    assert err == "invalid_storage"


def test_change_status_raises_on_invalid_transition(monkeypatch):
    storage = FakeStorage([_order_row(last="DELIVERED")])
    monkeypatch.setattr(order_service_module, "JsonStorage", lambda: storage)

    svc = OrderService()
    with pytest.raises(InvalidTransitionError):
        svc.change_status("order-1", "CONFIRMED", origin="STORE")