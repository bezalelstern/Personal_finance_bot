from pymongo import MongoClient



mongo_client = MongoClient("mongodb://admin:1234@localhost:27018")
db = mongo_client["telegram_data"]
collection = db["messages"]

print("Connected to MongoDB!")