def get_paginated_results(collection, filters, page, limit):
    skip = (int(page) - 1) * int(limit)
    total = collection.count_documents(filters)
    results = list(collection.find(filters).skip(skip).limit(int(limit)))
    return {"total": total, "results": results}