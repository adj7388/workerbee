import logging
from typing import Any, OrderedDict
from collections import OrderedDict

_logger = logging.getLogger(__name__)


class FIFOCache:
    def __init__(self, maxsize=10) -> None:
        self.maxsize = maxsize
        self.cache = OrderedDict()

    @property
    def cache_size(self):
        return len(self.cache)

    def _evict_cache_items(self, denominator=2):
        _logger.warning(f"Cache size {self.cache_size} exceeds maxsize {self.maxsize}")
        number_to_evict = self.cache_size // denominator
        for _ in range(number_to_evict):
            self.cache.popitem(last=False)
        _logger.warning(
            f"Evicted {number_to_evict} items from cache. Cache size now {self.cache_size}"
        )

    def get(self, key: frozenset) -> Any | None:
        return self.cache.get(key, None)

    def set(self, key: frozenset, value: Any) -> None:
        if key not in self.cache:
            self.cache[key] = value
            if self.cache_size > self.maxsize:
                self._evict_cache_items()
