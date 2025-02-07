from flask import jsonify, request
from . import app, db
import requests
from .models import Page, Post
from .scraper import scrape_facebook_page
from .utils import get_paginated_results
from .cache import cache
from bson import ObjectId
from config.settings import Config

@app.route("/api/page/<string:username>", methods=["GET"])
@cache.cached(timeout=300, query_string=True)
def get_page_details(username):
    page_data = db.pages.find_one({"username": username})
    if not page_data:
        # Step 2: Scrape Facebook page data if not found in the database
        response = scrape_facebook_page(username)

        # Extract structured data from the scraper response
        scraped_data = response.get("structured_data")
        if not scraped_data or "error" in scraped_data:
            return jsonify({"error": "Failed to fetch data for the specified username."}), 404

        # Step 3: Save the scraped data to the database
        try:
            page = Page(**scraped_data)
            db.pages.insert_one(page.to_dict())
            page_data = page.to_dict()
        except Exception as e:
            return jsonify({"error": f"Error saving data to the database: {str(e)}"}), 500

    # Convert MongoDB ObjectId to string for JSON serialization
    if "_id" in page_data:
        page_data["_id"] = str(page_data["_id"])

    # Step 4: Return the page data as a JSON response
    return jsonify(page_data)

@app.route("/api/pages", methods=["GET"])
@cache.cached(timeout=300, query_string=True)
def list_pages():
    filters = {}
    if "follower_range" in request.args:
        min_followers, max_followers = map(
            int, request.args["follower_range"].split("-"))
        filters["followers"] = {"$gte": min_followers, "$lte": max_followers}
    if "category" in request.args:
        filters["category"] = request.args["category"]

    page = request.args.get("page", 1)
    limit = request.args.get("limit", 10)
    pages = get_paginated_results(db.pages, filters, page, limit)

    return jsonify(pages)


@app.route("/api/posts/<string:username>", methods=["GET"])
@cache.cached(timeout=300, query_string=True)
def get_recent_posts(username):
    posts = db.posts.find({"username": username}).sort(
        "created_at", -1).limit(10)
    return jsonify([Post(**post).to_dict() for post in posts])


@app.route("/api/summary/<string:username>", methods=["GET"])
@cache.cached(timeout=300, query_string=True)
def generate_ai_summary(username):
    page_data = db.pages.find_one({"username": username})
    if not page_data:
        return jsonify({"error": "Page not found"}), 404



    # Call Gemini API
    gemini_key = Config.GOOGLE_API_KEY
    if not gemini_key:
        return jsonify({"error": "Gemini API key not found in environment variables."}), 500

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
    payload = {
        "contents": [{"parts": [{"text": f"Provide a concise summary of this Facebook page: {page_data}"}]}]
    }

    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            response_data = response.json()
            candidates = response_data.get("candidates", [])
            if candidates:
                content = candidates[0].get("content", {})
                if "parts" in content:
                    summary = content["parts"][0].get("text", "Could not generate a summary.")
                else:
                    summary = "No parts found in the response."
            else:
                summary = "No candidates found in the response."
        else:
            summary = f"Error occurred while calling the Gemini API: {response.status_code}"
    except Exception as e:
        summary = f"Error occurred while processing the request: {str(e)}"

    return jsonify({
        "username": username,
        "summary": summary
}), 200
