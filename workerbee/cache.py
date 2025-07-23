import logging

from typing import Any, cast
from collections import OrderedDict

_logger = logging.getLogger(__name__)


class FIFOCache:
    def __init__(self, tag: str, maxsize=10) -> None:
        self.tag: str = tag
        self.maxsize: int = maxsize
        self.cache: OrderedDict = OrderedDict()
        _logger.debug(f"'{self.tag}' initialized with maxsize {maxsize}")

    @property
    def cache_size(self):
        return len(self.cache)

    def _evict(self, denominator=2) -> None:
        if self.cache_size > self.maxsize:
            number_to_evict = self.cache_size // denominator
            for _ in range(number_to_evict):
                self.cache.popitem(last=False)
            _logger.info(
                f"'{self.tag}' evicted {number_to_evict} items from cache. Size now {self.cache_size}"
            )
        else:
            _logger.warning(
                f"Skipping eviction in '{self.tag}': cache_size {self.cache_size} < maxsize {self.maxsize}"
            )

    def get(self, key: Any) -> Any | None:
        result = self.cache.get(key, None)
        (
            _logger.debug(
                f"GET '{self.tag}' ({self.cache_size}) get key successful: {key}"
            )
            if result
            else _logger.debug(
                f"GET '{self.tag}' ({self.cache_size}) get key returned None: {key}"
            )
        )
        return result

    def set(self, key: Any, value: Any) -> None:
        if key not in self.cache:
            self.cache[key] = value
            _logger.debug(f"SET '{self.tag}' ({self.cache_size}) new item key: {key}")
            if self.cache_size > self.maxsize:
                _logger.info(
                    f"'{self.tag}' size {self.cache_size} exceeds maxsize {self.maxsize}"
                )
                self._evict()
        else:
            self.cache[key] = value
            _logger.debug(
                f"SET '{self.tag}' ({self.cache_size}) replace item key: {key}"
            )


FIND_WORDS: str = "findwords"
SUMMARIES: str = "showsummaries"

_caches: dict[str, FIFOCache | None] = {
    FIND_WORDS: None,
    SUMMARIES: None,
}


def init_caches(cache_size: int = 30) -> None:
    global _caches
    for key in _caches:
        _caches[key] = FIFOCache(tag=key, maxsize=cache_size)


def get_cache(key: str) -> FIFOCache:
    if _caches[key] is None or key not in _caches:
        raise RuntimeError(f"cache {key} does not exist or is not initialized")
    return cast(FIFOCache, _caches[key])
