from datetime import datetime, timedelta
from news_data.db.config_mongo import collection


def get_news_from_last_week(keyword):

    one_week_ago = datetime.now() - timedelta(weeks=1)
    query = {
        "date": {"$gte": one_week_ago.isoformat()},
        "message": {"$regex": f".*{keyword}.*"}
    }
    results = collection.find(query, {"_id": 0, "channel": 1, "message": 1, "date": 1, "image_url": 1})
    news_list = list(results)

    return news_list


if __name__ == "__main__":
    news = get_news_from_last_week("חדשות")
    print("News from the last week:")
    for item in news:
        print(item)
