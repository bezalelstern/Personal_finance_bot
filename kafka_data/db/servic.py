from kafka_data.db.config_mongo import collection
import base64


def insert_to_mongo(data, image_path=None):
    try:
        if image_path:
            with open(image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            data["image_data"] = encoded_image

        collection.insert_one(data)
        print("Data successfully inserted into MongoDB.")
    except Exception as e:
        print(f"Error inserting data into MongoDB: {e}")