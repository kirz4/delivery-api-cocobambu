import time
from ..repositories.json_storage import JsonStorage
from ..domain.status_machine import assert_transition, allowed_next_statuses


class OrderService:
    def __init__(self):
        self.storage = JsonStorage()

    def _load_list(self):
        data = self.storage.read()
        if not isinstance(data, list):
            return None, "invalid_storage"
        return data, None

    def _find_index(self, data: list, order_id: str):
        for i, row in enumerate(data):
            if row.get("order_id") == order_id:
                return i
        return None

    def get_allowed_next_statuses(self, order_id: str):
        """
        Retorna o status atual e as transições possíveis.
        Útil para o frontend renderizar apenas botões válidos.
        """
        data, err = self._load_list()
        if err:
            return None, err

        index = self._find_index(data, order_id)
        if index is None:
            return None, "not_found"

        row = data[index]
        order = row.get("order", {})
        current = order.get("last_status_name")

        return {
            "order_id": order_id,
            "current": (current or "").upper(),
            "allowed": allowed_next_statuses(current),
        }, None

    def change_status(self, order_id: str, new_status: str, origin: str = "SYSTEM"):
        data, err = self._load_list()
        if err:
            return None, err

        index = self._find_index(data, order_id)
        if index is None:
            return None, "not_found"

        row = data[index]
        order = row.get("order", {})
        current = order.get("last_status_name")

        # valida transição
        assert_transition(current, new_status)

        event = {
            "created_at": int(time.time() * 1000),
            "name": (new_status or "").upper(),
            "order_id": order_id,
            "origin": origin,
        }

        statuses = order.get("statuses")
        if not isinstance(statuses, list):
            statuses = []

        statuses.append(event)

        order["statuses"] = statuses
        order["last_status_name"] = (new_status or "").upper()
        row["order"] = order
        data[index] = row

        self.storage.write_atomic(data)
        return row, None