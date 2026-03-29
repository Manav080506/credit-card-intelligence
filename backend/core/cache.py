import json
import os

import redis


redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
try:
    redis_client = redis.Redis.from_url(redis_url, decode_responses=True)
except Exception:
    redis_client = None


def cache_get(key):
    if redis_client is None:
        return None
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None


def cache_set(key, value, ttl=3600):
    if redis_client is None:
        return
    redis_client.set(key, json.dumps(value), ex=ttl)


def cache_delete_pattern(pattern):
    if redis_client is None:
        return
    cursor = 0
    while True:
        cursor, keys = redis_client.scan(cursor=cursor, match=pattern, count=200)
        if keys:
            redis_client.delete(*keys)
        if cursor == 0:
            break
