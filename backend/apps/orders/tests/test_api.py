import json
import pytest

from apps.orders import views as views_module


class FakeRepo:
    def __init__(self, initial=None):
        self.data = list(initial or [])

    def list(self):
        return self.data

    def get_by_id(self, order_id):
        for row in self.data:
            if row.get("order_id") == order_id:
                return row
        return None

    def create(self, payload):
        self.data.append(payload)
        return payload

    def delete(self, order_id):
        before = len(self.data)
        self.data = [r for r in self.data if r.get("order_id") != order_id]
        return len(self.data) != before


class FakeService:
    def __init__(self, updated_row=None, err=None, exc=None):
        self._updated_row = updated_row
        self._err = err
        self._exc = exc
        self.called_with = None

    def change_status(self, order_id, new_status, origin="SYSTEM"):
        self.called_with = (order_id, new_status, origin)
        if self._exc:
            raise self._exc
        return self._updated_row, self._err


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


@pytest.mark.django_db
def test_get_orders_collection(client, monkeypatch):
    repo = FakeRepo([_order_row("a"), _order_row("b")])
    monkeypatch.setattr(views_module, "OrderRepository", lambda: repo)

    res = client.get("/api/orders/")
    assert res.status_code == 200
    body = res.json()
    assert isinstance(body, list)
    assert len(body) == 2


@pytest.mark.django_db
def test_get_order_resource_found(client, monkeypatch):
    repo = FakeRepo([_order_row("x")])
    monkeypatch.setattr(views_module, "OrderRepository", lambda: repo)

    res = client.get("/api/orders/x/")
    assert res.status_code == 200
    assert res.json()["order_id"] == "x"


@pytest.mark.django_db
def test_get_order_resource_not_found(client, monkeypatch):
    repo = FakeRepo([])
    monkeypatch.setattr(views_module, "OrderRepository", lambda: repo)

    res = client.get("/api/orders/missing/")
    assert res.status_code == 404
    assert res.json()["error"] == "Order not found"


@pytest.mark.django_db
def test_post_orders_collection_creates(client, monkeypatch):
    repo = FakeRepo([])
    monkeypatch.setattr(views_module, "OrderRepository", lambda: repo)

    payload = _order_row("new-1")
    res = client.post(
        "/api/orders/",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert res.status_code == 201
    assert repo.get_by_id("new-1") is not None


@pytest.mark.django_db
def test_post_orders_collection_conflict(client, monkeypatch):
    repo = FakeRepo([_order_row("dup")])
    monkeypatch.setattr(views_module, "OrderRepository", lambda: repo)

    payload = _order_row("dup")
    res = client.post(
        "/api/orders/",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert res.status_code == 409
    assert res.json()["error"] == "Order already exists"


@pytest.mark.django_db
def test_delete_order_resource(client, monkeypatch):
    repo = FakeRepo([_order_row("del")])
    monkeypatch.setattr(views_module, "OrderRepository", lambda: repo)

    res = client.delete("/api/orders/del/")
    assert res.status_code == 200
    assert res.json()["deleted"] is True
    assert repo.get_by_id("del") is None


@pytest.mark.django_db
def test_patch_change_status_success(client, monkeypatch):
    updated = _order_row("p1", last="CONFIRMED")
    service = FakeService(updated_row=updated, err=None, exc=None)
    monkeypatch.setattr(views_module, "OrderService", lambda: service)

    res = client.patch(
        "/api/orders/p1/status/",
        data=json.dumps({"status": "CONFIRMED", "origin": "STORE"}),
        content_type="application/json",
    )
    assert res.status_code == 200
    assert res.json()["order"]["last_status_name"] == "CONFIRMED"
    assert service.called_with == ("p1", "CONFIRMED", "STORE")


@pytest.mark.django_db
def test_patch_change_status_not_found(client, monkeypatch):
    service = FakeService(updated_row=None, err="not_found", exc=None)
    monkeypatch.setattr(views_module, "OrderService", lambda: service)

    res = client.patch(
        "/api/orders/missing/status/",
        data=json.dumps({"status": "CONFIRMED"}),
        content_type="application/json",
    )
    assert res.status_code == 404
    assert res.json()["error"] == "Order not found"


@pytest.mark.django_db
def test_patch_change_status_invalid_json(client, monkeypatch):
    monkeypatch.setattr(views_module, "OrderService", lambda: FakeService())

    res = client.patch(
        "/api/orders/p1/status/",
        data="{invalid",
        content_type="application/json",
    )
    assert res.status_code == 400
    assert res.json()["error"] == "Invalid JSON"


@pytest.mark.django_db
def test_patch_change_status_missing_status_field(client, monkeypatch):
    monkeypatch.setattr(views_module, "OrderService", lambda: FakeService())

    res = client.patch(
        "/api/orders/p1/status/",
        data=json.dumps({"origin": "STORE"}),
        content_type="application/json",
    )
    assert res.status_code == 400
    assert res.json()["error"] == "Field 'status' is required"