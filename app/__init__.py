from flask import Flask
from pymongo import MongoClient
from config.settings import Config

app = Flask(__name__)
app.config.from_object(Config)

# MongoDB Client
mongo_client = MongoClient(app.config['MONGO_URI'])
db = mongo_client.get_default_database()

# Import routes
from . import routes
from .routes import app