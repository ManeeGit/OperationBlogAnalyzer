import pymongo
from config import MONGO_URI

client = pymongo.MongoClient(MONGO_URI)
db = client["blog_analyzer"]
users_collection = db["users"]

def authenticate_user(username, password):
    user = users_collection.find_one({"username": username, "password": password})
    return user is not None
