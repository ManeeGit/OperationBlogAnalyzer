from pymongo import MongoClient
from config import MONGO_URI

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["blog_analyzer"]
users = db["users"]

# Ask for username
username = input("Enter the username to promote to admin: ")

# Promote user
result = users.update_one(
    {"username": username},
    {"$set": {"is_admin": True}}
)

if result.modified_count > 0:
    print(f"✅ User '{username}' is now an admin.")
else:
    print(f"⚠️ User '{username}' not found or already an admin.")
