from .json_storage import JsonStorage

class OrderRepository:
    def __init__(self):
        self.storage = JsonStorage()

    def list(self):
        data = self.storage.read()

        # Formato A: arquivo é uma lista direta
        if isinstance(data, list):
            return data

        # Formato B: arquivo é {"orders": [...]}
        if isinstance(data, dict):
            return data.get("orders", [])

        # Qualquer outro caso
        return []

    def get_by_id(self, order_id: str):
        for row in self.list():
            if row.get("order_id") == order_id:
                return row
        return None