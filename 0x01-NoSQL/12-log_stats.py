#!/usr/bin/env python3
""" Logs Nginx from MongoDB and prints stats """
import pymongo



def stats():
  """ logs for Nginx from MongoDB and prints stats """
  collection = pymongo.MongoClient().logs.nginx
  print(f"{collection.count_documents({})} logs")
  print("Methods:")
  methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
  for method in methods:
    count = collection.count_documents({"method": method})
    print(f"\tmethod {method}: {count}")
  print(f"{collection.count_documents({'method': 'GET', 'path': '/status'})}\
    status check")


stats()
