import time
from ..repositories.json_storage import JsonStorage
from ..domain.status_machine import assert_transition


class OrderService:
    def __init__(self):
        self.storage = JsonStorage()

    def change_status(self, order_id: str, new_status: str, origin: str = "SYSTEM"):
        data = self.storage.read()

        # data deve ser LISTA (seu caso)
        if not isinstance(data, list):
            return None, "invalid_storage"

        index = None
        for i, row in enumerate(data):
            if row.get("order_id") == order_id:
                index = i
                break

        if index is None:
            return None, "not_found"

        row = data[index]
        order = row.get("order", {})
        current = order.get("last_status_name")

        assert_transition(current, new_status)

        event = {
            "created_at": int(time.time() * 1000),
            "name": new_status.upper(),
            "order_id": order_id,
            "origin": origin,
        }

        statuses = order.get("statuses", [])
        statuses.append(event)

        order["statuses"] = statuses
        order["last_status_name"] = new_status.upper()
        row["order"] = order
        data[index] = row

        self.storage.write_atomic(data)
        return row, None