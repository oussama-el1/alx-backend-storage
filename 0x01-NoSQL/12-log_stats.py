#!/usr/bin/env python3
""" Logs Nginx from MongoDB and prints stats
"""
import pymongo


def stats():
	""" stats function """
	collection = pymongo.MongoClient().logs.nginx
	print(f"{collection.count_documents({})} logs")
	print("Methods:")
	methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
	for method in methods:
		count = collection.count_documents({"method": method})
		print(f"\tmethod {method}: {count}")
	status_get = collection.count_documents({'method': 'GET', 'path': '/status'})
	print(f"{status_get} status check")


if __name__ == "__main__":
	stats()
