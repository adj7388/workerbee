import logging

from typing import Any
from collections import OrderedDict

_logger = logging.getLogger(__name__)


class FIFOCache:
    def __init__(self, name, maxsize=10) -> None:
        self.name = name
        self.maxsize: int = maxsize
        self.cache: OrderedDict = OrderedDict()
        _logger.debug(f"'{self.name}' initialized with maxsize {maxsize}")

    @property
    def cache_size(self):
        return len(self.cache)

    def _evict_cache_items(self, denominator=2):
        _logger.warning(
            f"'{self.name}' size {self.cache_size} exceeds maxsize {self.maxsize}"
        )
        number_to_evict = self.cache_size // denominator
        for _ in range(number_to_evict):
            self.cache.popitem(last=False)
        _logger.warning(
            f"'{self.name}' evicted {number_to_evict} items from cache. Size now {self.cache_size}"
        )

    def get(self, key: frozenset) -> Any | None:
        _logger.info(f"GET:  '{self.name}' size: {self.cache_size}")
        result = self.cache.get(key, None)
        (
            _logger.debug(f"'{self.name}' get key successful: {key}")
            if result
            else _logger.debug(f"'{self.name}' get key returned None: {key} ")
        )
        return result

    def set(self, key: frozenset, value: Any) -> None:
        if key not in self.cache:
            self.cache[key] = value
            _logger.debug(f"SET '{self.name}' new item with key: {key}")
            if self.cache_size > self.maxsize:
                self._evict_cache_items()
        else:
            # found key. replace value
            self.cache[key] = value
            _logger.debug(f"SET '{self.name}' replaced item with key: {key}")


_beewords_cache: FIFOCache | None = None
_summaries_cache: FIFOCache | None = None


def init_cache(cache_size: int):
    global _beewords_cache, _summaries_cache
    _beewords_cache = FIFOCache(name="beewords cache", maxsize=cache_size)
    _summaries_cache = FIFOCache(name="summaries cache", maxsize=cache_size)


def get_beewords_cache() -> FIFOCache:
    if _beewords_cache is None:
        raise RuntimeError("BeeWords cache not initialized")
    return _beewords_cache


def get_summaries_cache() -> FIFOCache:
    if _summaries_cache is None:
        raise RuntimeError("Summaries cache not initialized")
    return _summaries_cache
