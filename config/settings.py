import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    CACHE_TTL = os.getenv("CACHE_TTL", 300)
    REDIS_URL = os.getenv("REDIS_URL")
    CACHE_TYPE = "redis" 
