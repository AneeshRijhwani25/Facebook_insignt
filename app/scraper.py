import requests
from bs4 import BeautifulSoup
from config.settings import Config
from flask import jsonify, request
import json
from .utils import followerformatter

def scrape_facebook_page(username):
    url = f"https://www.facebook.com/{username}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page data: {response.status_code}")
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # name = soup.find("title").text.split(" - ")[0] if soup.find("title") else None

    # profile_pic_tag = soup.select_one('meta[property="og:image"]')
    # profile_pic = profile_pic_tag['content'] if profile_pic_tag else None

    # page_id_tag = soup.find("meta", property="al:android:url")
    # page_id = page_id_tag["content"].split("/")[-1] if page_id_tag else None

    # email_tag = soup.find("a", href=lambda href: href and "mailto:" in href)
    # email = email_tag['href'].replace("mailto:", "").strip() if email_tag else None

    # website_tag = soup.find("a", href=lambda href: href and "http" in href and "facebook" not in href)
    # website = website_tag['href'] if website_tag else None

    # category_tag = soup.find("div", string=lambda s: s and "Page:" in s)
    # category = category_tag.find_next("span").text.strip() if category_tag else None


    # followers_tag = soup.find("a", string=lambda s: s and "followers" in s.lower())
    # if followers_tag:
    #     followers_text = followers_tag.text
    #     followers = ''.join(filter(str.isdigit, followers_text))
    # else:
    #     followers = "0"

    # likes_tag = soup.find("div", string=lambda s: s and "likes" in s.lower())
    # likes = ''.join(filter(str.isdigit, likes_tag.text)) if likes_tag else "0"
    
    # creation_date_tag = soup.find("div", string=lambda s: s and "Created" in s)
    # creation_date = creation_date_tag.text.strip() if creation_date_tag else None

    raw_html = str(soup)  
    # print(raw_html)

    # Step 2: Validate Gemini API Key
    gemini_key = Config.GOOGLE_API_KEY
    if not gemini_key:
        return jsonify({"error": "Gemini API key not found in environment variables."}), 500

    # Step 3: Prepare Gemini API request
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
    prompt = """
    Extract the following details from the provided HTML content of a Facebook page:
    {
        "name": "The name of the page",
        "username": "The username of the page",
        "url": "The page's URL",
        "page_id": "The page ID",
        "profile_pic": "URL to the profile picture",
        "email": "The email address",
        "website": "Linked website",
        "category": "Category of the page",
        "followers": "Number of followers",
        "likes": "Number of likes",
        "creation_date": "Page creation date"
    }
    Return the extracted data in valid JSON format.
    """
    payload = {
        "contents": [{"parts": [{"text": f"{prompt}\n\nHTML Content:\n{raw_html}"}]}]
    }
    try:
    # Make the Gemini API request
        api_response = requests.post(gemini_url, json=payload, headers={"Content-Type": "application/json"})
        
        if api_response.status_code != 200:
            return jsonify({"error": f"Gemini API call failed: {api_response.status_code}"}), 500

        # Parse the response data
        response_data = api_response.json()
        candidates = response_data.get("candidates", [])
        # print(candidates)
        if candidates:
            # Extract JSON text from the first candidate
            extracted_text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "{}")
            
            try:
                # Parse the extracted JSON string into a dictionary
                structured_data = json.loads(extracted_text.strip("```json\n").strip("```"))
                # print(structured_data)
                # Map the fields correctly
                result = {
                    "name": structured_data.get("name"),
                    "username": structured_data.get("username"),
                    "url": structured_data.get("url"),
                    "page_id": structured_data.get("page_id"),
                    "profile_pic": structured_data.get("profile_pic"),
                    "email": structured_data.get("email"),
                    "website": structured_data.get("website", None) if structured_data.get("website") else url,
                    "category": structured_data.get("category",None) if structured_data.get("category") else "Technology",
                    "followers": int(structured_data.get("followers", 0)) if structured_data.get("followers") else followerformatter(),
                    "likes": int(structured_data.get("likes", "0").replace(",", "")) if structured_data.get("likes") else 0,
                    "creation_date": structured_data.get("creation_date"),
                }
                # print(result)
            except json.JSONDecodeError as e:
                result = {"error": f"Failed to parse extracted data: {str(e)}"}
        else:
            result = {"error": "No candidates returned from Gemini API."}

    except Exception as e:
        result = {"error": f"Error while processing Gemini API request: {str(e)}"}

    # Step 5: Return the extracted data
    return {"raw_html": raw_html, "structured_data": result}
    # return soup , {
    #     "name": name,
    #     "username": username,
    #     "url": url,
    #     "page_id": page_id,
    #     "profile_pic": profile_pic,
    #     "email": email,
    #     "website": website,
    #     "category": category,
    #     "followers": int(followers) if followers else 0,
    #     "likes": int(likes) if likes else 0,
    #     "creation_date": creation_date
    # }
    # return raw_html, structured_data
