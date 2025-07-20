from typing import Any
import diskcache


class FIFOCache:
    def __init__(self, path="/tmp/workerbee-cache", maxsize=128) -> None:
        self.cache = diskcache.Cache(path)
        self.maxsize = maxsize

    def get(self, key: frozenset) -> Any | None:
        return self.cache.get(key, default=None)

    def set(self, key: frozenset, value: Any) -> None:
        # If key is new, insert; else update
        if key not in self.cache:
            self.cache.set(key, value)
            # Enforce FIFO: if over maxsize, delete oldest
            if len(self.cache) > self.maxsize:  # type: ignore
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]
        else:
            self.cache.set(key, value)
