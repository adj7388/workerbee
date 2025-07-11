from collections import OrderedDict


class FIFOCache:
    def __init__(self, maxsize=128):
        self.cache = OrderedDict()
        self.maxsize = maxsize

    def get(self, key):
        result = self.cache.get(key)
        if result is not None:
            print(f"Get cached result: {key}")
        return result

    def set(self, key, result):
        print(f"Put result in cache: {key}")
        if key in self.cache:
            print(f"Deleting: {key}")
            del self.cache[key]
        elif len(self.cache) >= self.maxsize:
            print(f"Evicting: {key}")
            self.cache.popitem(last=False)
        self.cache[key] = result
