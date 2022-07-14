from contextlib import suppress
import json
import redis

from django.conf import settings


def _is_redis_available(redis_instance: redis.Redis) -> bool:
    """Check if the redis is connected."""
    with suppress(redis.ConnectionError):
        return redis_instance.ping()
    return False


def get_value_from_redis(key: str):
    r = redis.Redis.from_url(
        url=settings.REDIS_URL,
        decode_responses=True,
    )
    if _is_redis_available(r):
        value = r.get(key)
        if value:
            return json.loads(value)
        return


def set_value_to_redis(key: str, value: str):
    r = redis.Redis.from_url(
        url=settings.REDIS_URL,
        decode_responses=True,
    )
    if _is_redis_available(r):
        return r.set(key, value)
