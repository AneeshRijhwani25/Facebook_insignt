from datetime import datetime
from bson import ObjectId

# class Page:
#     def __init__(self, name, username, url, page_id, profile_pic, email, website, category, followers, likes, creation_date):
#         self.name = name
#         self.username = username
#         self.url = url
#         self.page_id = page_id
#         self.profile_pic = profile_pic
#         self.email = email
#         self.website = website
#         self.category = category
#         self.followers = followers
#         self.likes = likes
#         self.creation_date = creation_date

#     def to_dict(self):
#         return {
#             "name": self.name,
#             "username": self.username,
#             "url": self.url,
#             "page_id": self.page_id,
#             "profile_pic": self.profile_pic,
#             "email": self.email,
#             "website": self.website,
#             "category": self.category,
#             "followers": self.followers,
#             "likes": self.likes,
#             "creation_date": self.creation_date,
#         }


class Page:
    def __init__(self, name, username, url, page_id, profile_pic=None, email=None, website=None, 
                 category=None, followers=0, likes=0, creation_date=None):
        self.name = name
        self.username = username
        self.url = url
        self.page_id = page_id
        self.profile_pic = profile_pic
        self.email = email
        self.website = website
        self.category = category
        self.followers = followers
        self.likes = likes
        self.creation_date = creation_date

    def to_dict(self):
        return {
            "name": self.name,
            "username": self.username,
            "url": self.url,
            "page_id": self.page_id,
            "profile_pic": self.profile_pic,
            "email": self.email,
            "website": self.website,
            "category": self.category,
            "followers": self.followers,
            "likes": self.likes,
            "creation_date": self.creation_date,
        }

class Post:
    def __init__(self, post_id, content, comments, likes, created_at):
        self.post_id = post_id
        self.content = content
        self.comments = comments
        self.likes = likes
        self.created_at = created_at

    def to_dict(self):
        return {
            "post_id": self.post_id,
            "content": self.content,
            "comments": self.comments,
            "likes": self.likes,
            "created_at": self.created_at,
        }