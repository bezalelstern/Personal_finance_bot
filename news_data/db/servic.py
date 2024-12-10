from news_data.db.config_mongo import collection


def insert_to_mongo(data):
    try:
        collection.insert_one(data)
        print("Data successfully inserted into MongoDB.")
    except Exception as e:
        print(f"Error inserting data into MongoDB: {e}")
