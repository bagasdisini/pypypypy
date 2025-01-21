from cachetools import TTLCache

# Create a cache manager with a max size and TTL (time-to-live) for items
cache = TTLCache(maxsize=1000000, ttl=60)  # maxsize: 1 million, ttl: 60 seconds


def get_cache(key):
    if key in cache:
        return cache[key]
    return None


def set_cache(key, value):
    cache[key] = value


def delete_cache(key):
    if key in cache:
        del cache[key]


def delete_all_cache():
    cache.clear()