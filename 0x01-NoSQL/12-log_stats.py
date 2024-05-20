#!/usr/bin/env python3
""" Logs Nginx from MongoDB and prints stats
"""
from pymongo import MongoClient


def stats():
	""" stats function """
	client = MongoClient('mongodb://127.0.0.1:27017')
	collection = client.logs.nginx
	print(f"{collection.count_documents({})} logs")
	print("Methods:")
	methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
	for method in methods:
		req_count = len(list(collection.find({'method': method})))
		print('\tmethod {}: {}'.format(method, req_count))
	status_checks_count = len(list(
		collection.find({'method': 'GET', 'path': '/status'})
	))
	print('{} status check'.format(status_checks_count))

if __name__ == "__main__":
	stats()
