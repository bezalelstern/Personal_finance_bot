from faker import Faker
import random

from news_data.db.config_mongo import collection

# יצירת אובייקט Faker
fake = Faker()

# פונקציה ליצירת הודעות רנדומליות
def generate_random_message():
    return {
        "channel": fake.company(),
        "message": fake.text(max_nb_chars=200),
        "date": fake.date_time_this_year().isoformat(),
        "image_url": fake.image_url() if random.choice([True, False]) else None,
        "user": {
            "username": fake.user_name(),
            "full_name": fake.name(),
            "email": fake.email()
        }
    }

# הכנסת נתונים למסד הנתונים
def insert_random_data(num_records):
    data = [generate_random_message() for _ in range(num_records)]
    result = collection.insert_many(data)
    print(f"Inserted {len(result.inserted_ids)} records into the database.")

# הרצה
if __name__ == "__main__":
    num_records = 100  # מספר הרשומות להוסיף
    insert_random_data(num_records)
