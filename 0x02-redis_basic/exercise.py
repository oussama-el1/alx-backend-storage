#!/usr/bin/env python3
"""
Redis task 1
"""
from uuid import uuid4
import redis
from typing import Union, Callable, Optional


class Cache:
    """ Cache class to create instance for Redis client """

    def __init__(self):
        """Initialize the Cache instance and create a private Redis client."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the given data in Redis using a randomly
        generated UUID as the key.

        Args:
            data (Union[str, bytes, int, float]): The data to store.

        Returns:
            str: The UUID key under which the data is stored.
        """
        key: str = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None)\
            -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis and optionally apply a conversion function.

        Args:
            key (str): The key of the data to retrieve.
            fn (Optional[Callable]): A function to apply to the retrieved data.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data,
            optionally converted, or None if key does not exist.
        """
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a string value from Redis.

        Args:
            key (str): The key of the string to retrieve.

        Returns:
            Optional[str]: The string value, or None if key does not exist.
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer value from Redis.

        Args:
            key (str): The key of the integer to retrieve.

        Returns:
            Optional[int]: The integer value, or None if key does not exist.
        """
        return self.get(key, lambda x: int(x))
