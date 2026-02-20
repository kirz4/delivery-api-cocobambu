import time
from ..repositories.order_repository import OrderRepository
from ..domain.status_machine import assert_transition

class OrderService:
    def __init__(self):
        self.repo = OrderRepository()

    def change_status(self, order_id: str, new_status: str, origin: str = "SYSTEM"):
        orders = self.repo.list()
        idx = next((i for i, o in enumerate(orders) if o.get("order_id") == order_id), None)
        if idx is None:
            return None, "not_found"

        row = orders[idx]
        current = row["order"].get("last_status_name")

        assert_transition(current, new_status)

        event = {
            "created_at": int(time.time() * 1000),
            "name": new_status.upper(),
            "order_id": order_id,
            "origin": origin,
        }

        row["order"]["statuses"].append(event)
        row["order"]["last_status_name"] = new_status.upper()

        orders[idx] = row
        self.repo.save_all(orders)

        return row, None