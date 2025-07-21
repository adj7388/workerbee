import logging
from typing import Any, OrderedDict
from collections import OrderedDict

_logger = logging.getLogger(__name__)


class FIFOCache:
    def __init__(self, maxsize=10) -> None:
        self.maxsize = maxsize
        self.cache = OrderedDict()

    def _evict_cache_items(self, denominator=2):
        half = len(self.cache) // denominator
        for _ in range(half):
            self.cache.popitem(last=False)
        _logger.info(f"Evicted {half} items from cache")

    def _show_cache_size(self, where: str):
        _logger.debug(f"++{where.upper()}++++ cache:{len(self.cache)}===========>: ")

    def get(self, key: frozenset) -> Any | None:
        self._show_cache_size(where="GET")
        return self.cache.get(key, None)

    def set(self, key: frozenset, value: Any) -> None:
        self._show_cache_size(where="set")
        if key not in self.cache:
            self.cache[key] = value
            self._show_cache_size(where="POST SET")
            if len(self.cache) > self.maxsize:
                _logger.debug(f"size of cache {len(self.cache)} exceeds {self.maxsize}")
                self._evict_cache_items()
                self._show_cache_size(where="after eviction")
