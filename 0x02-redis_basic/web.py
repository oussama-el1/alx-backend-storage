#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
"""
import requests
from typing import Callable
from functools import wraps
import redis


def Mydecorator(fun: Callable) -> Callable:
    """ Track a web page """
    @wraps(fun)
    def wrapper(url):
        """ wrapper for a get page function """
        client = redis.Redis()
        client.incr(f'count:{url}')
        client.expire(f'count:{url}', 10)

        return fun(url)
    return wrapper


@Mydecorator
def get_page(url: str) -> str:
    """ Implementing an expiring web cache and tracker """
    response = requests.get(url)
    if response.status_code == 200:
        content = response.text
        return content
