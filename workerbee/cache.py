from collections import OrderedDict
from typing import Any


class FIFOCache:
    def __init__(self, maxsize=128) -> None:
        self.cache = OrderedDict()
        self.maxsize = maxsize

    def get(self, key) -> Any | None:
        return self.cache.get(key)

    def set(self, key, value) -> None:
        if key in self.cache:
            del self.cache[key]
        elif len(self.cache) >= self.maxsize:
            self.cache.popitem(last=False)
        self.cache[key] = value
