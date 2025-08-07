import logging

from typing import Any, cast
from collections import OrderedDict


_logger = logging.getLogger(__name__)


class FIFOCache:
    def __init__(self, tag: str, maxsize) -> None:
        self.tag: str = tag
        self.maxsize: int = maxsize
        self.cache: OrderedDict = OrderedDict()
        _logger.info(f"{self.log_prefix} initialized w/ maxsize {maxsize}")

    @property
    def cache_size(self):
        return len(self.cache)

    @property
    def log_prefix(self):
        return f"[cache: {self.tag} size: {self.cache_size}  max: {self.maxsize}]"

    def _evict(self, denominator=2) -> None:
        _logger.info(f"{self.log_prefix} EVICT ")
        if self.cache_size > self.maxsize:
            number_to_evict = self.cache_size // denominator
            for _ in range(number_to_evict):
                self.cache.popitem(last=False)
            _logger.info(f"{self.log_prefix} evicted {number_to_evict} items")
        else:
            _logger.warning(f"{self.log_prefix} eviction skipped")

    def get(self, key: Any) -> Any | None:
        result = self.cache.get(key, None)
        (
            _logger.debug(f"{self.log_prefix} cache hit: {key}")
            if result
            else _logger.debug(f"{self.log_prefix} cache miss: {key}")
        )
        return result

    def set(self, key: Any, value: Any) -> None:
        if key not in self.cache:
            self.cache[key] = value
            _logger.debug(f"{self.log_prefix} cache set: {key}")
            if self.cache_size > self.maxsize:
                _logger.info(f"{self.log_prefix} cache size exceeded")
                self._evict()
        else:
            self.cache[key] = value
            _logger.debug(f"{self.log_prefix} cache replace: {key}")


FIND_WORDS: str = "find_words"
SHOW_SUMMARIES: str = "show_summaries"

_caches: dict[str, FIFOCache | None] = {
    FIND_WORDS: None,
    SHOW_SUMMARIES: None,
}


def init_caches(cache_size: int) -> None:
    global _caches
    for key in _caches:
        _caches[key] = FIFOCache(tag=key, maxsize=cache_size)


def get_cache(key: str) -> FIFOCache:
    if _caches[key] is None or key not in _caches:
        raise RuntimeError(f"cache {key} does not exist or is not initialized")
    return cast(FIFOCache, _caches[key])
