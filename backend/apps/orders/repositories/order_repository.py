from .json_storage import JsonStorage

class OrderRepository:
    def __init__(self):
        self.storage = JsonStorage()

    def list(self):
        data = self.storage.read()

        if isinstance(data, list):
            return data

        if isinstance(data, dict):
            return data.get("orders", [])

        return []

    def get_by_id(self, order_id: str):
        for row in self.list():
            if row.get("order_id") == order_id:
                return row
        return None

    def exists(self, order_id: str) -> bool:
        return self.get_by_id(order_id) is not None

    def create(self, order_row: dict):
        data = self.storage.read()
        if not isinstance(data, list):
            data = []
        data.append(order_row)
        self.storage.write_atomic(data)
        return order_row

    def delete(self, order_id: str) -> bool:
        data = self.storage.read()
        if not isinstance(data, list):
            return False
        new_data = [row for row in data if row.get("order_id") != order_id]
        if len(new_data) == len(data):
            return False
        self.storage.write_atomic(new_data)
        return True