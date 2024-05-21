#!/usr/bin/env python3
"""
Redis task 1
"""
from uuid import uuid4
import redis
from typing import Union


class Cache:
    """ Cache class to create instance for Redis client """
    def __init__(self):
        """ create private variable for Redis client  """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ method to store a data in a uuid4 key """
        key = str(uuid4())
        self._redis.set(key, data)
        return key
