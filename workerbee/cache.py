from collections import OrderedDict
from flask import current_app
from typing import Any


class FIFOCache:
    def __init__(self, maxsize=128) -> None:
        self.cache = OrderedDict()
        self.maxsize = maxsize

    def get(self, key) -> Any | None:
        current_app.logger.info(f"getting {key}")
        return self.cache.get(key)

    def set(self, key, value) -> None:
        if key in self.cache:
            del self.cache[key]
        elif len(self.cache) >= self.maxsize:
            self.cache.popitem(last=False)
        current_app.logger.info(f"setting {key}")
        self.cache[key] = value
