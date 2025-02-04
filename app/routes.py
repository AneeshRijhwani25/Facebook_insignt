from flask import jsonify, request
from . import app, db
from .models import Page, Post
from .scraper import scrape_facebook_page
from .utils import get_paginated_results
from .cache import cache
from bson import ObjectId

@app.route("/api/page/<string:username>", methods=["GET"])
@cache.cached(timeout=300, query_string=True)
def get_page_details(username):
    page_data = db.pages.find_one({"username": username})
    if not page_data:
        scraped_data = scrape_facebook_page(username)
        if not scraped_data:
            return jsonify({"error": "Failed to fetch data for the specified username."}), 404
        page = Page(**scraped_data)
        db.pages.insert_one(page.to_dict())
        page_data = page.to_dict()
    if "_id" in page_data:
        page_data["_id"] = str(page_data["_id"])
    return jsonify(page_data)


@app.route("/api/pages", methods=["GET"])
@cache.cached(timeout=300, query_string=True)
def list_pages():
    filters = {}
    if "follower_range" in request.args:
        min_followers, max_followers = map(int, request.args["follower_range"].split("-"))
        filters["followers"] = {"$gte": min_followers, "$lte": max_followers}
    if "category" in request.args:
        filters["category"] = request.args["category"]

    pages = get_paginated_results(db.pages, filters, request.args.get("page", 1), request.args.get("limit", 10))
    return jsonify(pages)


@app.route("/api/posts/<string:username>", methods=["GET"])
@cache.cached(timeout=300, query_string=True)
def get_recent_posts(username):
    posts = db.posts.find({"username": username}).sort("created_at", -1).limit(10)
    return jsonify([Post(**post).to_dict() for post in posts])