#!/usr/bin/env python3
"""
all students sorted by average score
"""


def top_students(mongo_collection):
    """ Use MongoDB aggregation framework to calculate the average score and sort by it """
    pipeline = [
        {
            "$project": {
                "name": 1,
                "topics": 1,
                "averageScore": {
                    "$avg": "$topics.score"
                }
            }
        },
        {
            "$sort": {
                "averageScore": -1
            }
        }
    ]

    return list(mongo_collection.aggregate(pipeline))
