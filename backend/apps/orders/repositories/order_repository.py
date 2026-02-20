from .json_storage import JsonStorage

class OrderRepository:
    def __init__(self):
        self.storage = JsonStorage()

    def list(self):
        data = self.storage.read()
        return data.get("orders", [])

    def get_by_id(self, order_id: str):
        for row in self.list():
            if row.get("order_id") == order_id:
                return row
        return None

    def save_all(self, orders: list):
        self.storage.write_atomic({"orders": orders})