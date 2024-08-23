import pymongo
import bcrypt

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.xgfuv.mongodb.net/")
db = client["dairy_farm_db"]
users_collection = db["users"]
animals_collection = db["animals"]

def initialize_database():
    if "dairy_farm_db" not in client.list_database_names():
        db = client["dairy_farm_db"]
        db.create_collection("users")
        db.create_collection("animals")
        print("Database and collections created.")
    else:
        print("Database already exists.")

def login_user(username, password, login_type):
    user = users_collection.find_one({"username": username, "role": login_type})
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return user
    return None

def register_user(username, password, role):
    if users_collection.find_one({"username": username}):
        return False
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = {
        "username": username,
        "password": hashed_password,
        "role": role,
        "is_active": True
    }
    users_collection.insert_one(user)
    return True