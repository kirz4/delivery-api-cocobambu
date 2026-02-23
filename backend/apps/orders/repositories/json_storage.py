import json
import os
from pathlib import Path
from django.conf import settings

class JsonStorage:
    def __init__(self):
        self.path = Path(settings.ORDERS_JSON_PATH)

    def read(self):
        print(">>> ORDERS_JSON_PATH =", settings.ORDERS_JSON_PATH)
        print(">>> RESOLVED =", self.path.resolve())
        print(">>> EXISTS? =", self.path.exists())
        if self.path.exists():
            print(">>> SIZE =", self.path.stat().st_size)
        if not self.path.exists() or self.path.stat().st_size == 0:
            return []
        try:
            with self.path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def write_atomic(self, data: dict) -> None:
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, self.path)