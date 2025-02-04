from flask_caching import Cache
from config.settings import Config
cache = Cache()

def init_app(app):
    cache.init_app(app, config={
        "CACHE_TYPE": "redis",
        "CACHE_REDIS_URL": app.config.get("REDIS_URL", Config.REDIS_URL),
    })