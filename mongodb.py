from pymongo import MongoClient
from config import MONGO_URI
from datetime import datetime

client = MongoClient(MONGO_URI)
db = client["blog_analyzer"]
users = db["users"]
analysis = db["analyzed_blogs"]

def authenticate_user(username, password):
    user = users.find_one({"username": username, "password": password})
    if not user:
        return False
    if user.get("expires_at") and datetime.utcnow() > user["expires_at"]:
        return False
    return True

def is_admin(username):
    user = users.find_one({"username": username})
    return user and user.get("is_admin", False)

def add_user(username, password, expires_at=None, is_admin=False):
    if users.find_one({"username": username}):
        return False
    users.insert_one({
        "username": username,
        "password": password,
        "is_admin": is_admin,
        "expires_at": expires_at
    })
    return True


def store_analysis(keyword, username, blogs):
    analysis.update_one(
        {"keyword": keyword},
        {"$set": {
            "username": username,
            "blogs": blogs,
            "timestamp": datetime.utcnow()
        }},
        upsert=True
    )
