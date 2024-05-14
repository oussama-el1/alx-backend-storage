#!/usr/bin/env python3
"""
9-insert_school.py
"""
import pymongo


def insert_school(mongo_collection, **kwargs):
  """ insert a new document in a collection """
  return mongo_collection.insert_one(kwargs)