import requests
from bs4 import BeautifulSoup

def scrape_facebook_page(username):
    url = f"https://www.facebook.com/{username}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page data: {response.status_code}")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    name = soup.find("title").text.split(" - ")[0] if soup.find("title") else None

    profile_pic_tag = soup.select_one('meta[property="og:image"]')
    profile_pic = profile_pic_tag['content'] if profile_pic_tag else None

    page_id_tag = soup.find("meta", property="al:android:url")
    page_id = page_id_tag["content"].split("/")[-1] if page_id_tag else None

    email_tag = soup.find("a", href=lambda href: href and "mailto:" in href)
    email = email_tag['href'].replace("mailto:", "").strip() if email_tag else None

    website_tag = soup.find("a", href=lambda href: href and "http" in href and "facebook" not in href)
    website = website_tag['href'] if website_tag else None

    category_tag = soup.find("div", string=lambda s: s and "Page:" in s)
    category = category_tag.find_next("span").text.strip() if category_tag else None


    followers_tag = soup.find("a", string=lambda s: s and "followers" in s.lower())
    print(followers_tag)
    if followers_tag:
        followers_text = followers_tag.text
        followers = ''.join(filter(str.isdigit, followers_text))
    else:
        followers = "0"

    print(followers)

    likes_tag = soup.find("div", string=lambda s: s and "likes" in s.lower())
    likes = ''.join(filter(str.isdigit, likes_tag.text)) if likes_tag else "0"
    
    creation_date_tag = soup.find("div", string=lambda s: s and "Created" in s)
    creation_date = creation_date_tag.text.strip() if creation_date_tag else None

    return {
        "name": name,
        "username": username,
        "url": url,
        "page_id": page_id,
        "profile_pic": profile_pic,
        "email": email,
        "website": website,
        "category": category,
        "followers": int(followers) if followers else 0,
        "likes": int(likes) if likes else 0,
        "creation_date": creation_date
    }
