#!/usr/bin/env python3
"""
Redis task 1
"""
from uuid import uuid4
import redis
from typing import Union, Callable, Optional, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ Tracks the number of calls made to a method in a Cache class. """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """Invokes the given method after incrementing its call counter."""
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ store the inputs and outputs """
    @wraps(method)
    def wrapper(self, *args) -> Any:
        """ invoke the given methods after add """
        if isinstance(self._redis, redis.Redis):
            methodname = method.__qualname__
            keyin = methodname + ':inputs'
            keyout = methodname + ':outputs'

            inputs = str(args)
            self._redis.rpush(keyin, inputs)

            out = method(self, *args)
            self._redis.rpush(keyout, out)

        return out
    return wrapper


def replay(method: Callable) -> None:
    """ replay the history """
    redis_client = redis.Redis()
    methodname = method.__qualname__
    listin = redis_client.lrange(f"{methodname}:inputs", 0, -1)  # nopep8
    listout = redis_client.lrange(f"{methodname}:outputs", 0, -1)  # nopep8

    in_and_out = zip(listin, listout)
    in_and_out_list = list(in_and_out)  # Store the result of zip in a list
    print(f"Cache.store was called {len(in_and_out_list)} times:")
    for invalue, outvalue in in_and_out_list:
        # Convert binary strings to regular strings
        if isinstance(invalue, bytes):
            invalue_str = f"{invalue.decode('utf-8')}"
        elif isinstance(invalue, int):
            invalue_str = f"{invalue}"
        else:
            invalue_str = f"{invalue}"

        outvalue_str = outvalue.decode('utf-8')
        print(f"{methodname}(*{invalue_str}) -> {outvalue_str}")


class Cache:
    """ Cache class to create instance for Redis client """
    def __init__(self):
        """Initialize the Cache instance and create a private Redis client."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
