import random

def get_paginated_results(collection, filters, page, limit):
    skip = (int(page) - 1) * int(limit)
    total = collection.count_documents(filters)
    results = list(collection.find(filters).skip(skip).limit(int(limit)))

    for result in results:
        if "_id" in result:
            result["_id"] = str(result["_id"])

    return {"total": total, "results": results}



def followerformatter():
    return random.randint(14000000, 20000000)