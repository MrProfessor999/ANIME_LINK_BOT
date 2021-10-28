from animeSupport.database.gogoanime import *
from animeSupport import DATABASE, MONGODB_URL
from pymongo import MongoClient
client = MongoClient(MONGODB_URL)
db = client[DATABASE]


NAME = "database"
__all__ = "database"
