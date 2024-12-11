from datetime import datetime, timedelta

from database.config_mongo import collection


def get_news_from_last_week(keyword):
    result = keyword.replace(",", " | ")

    one_week_ago = datetime.now() - timedelta(weeks=1)
    query = {
        "date": {"$gte": one_week_ago.isoformat()},
        "message": {"$regex": f".*{result}.*"}
    }
    try:
        results = collection.find(query, {"_id": 0, "channel": 1, "message": 1, "date": 1, "image_url": 1})
        news_list = list(results)

        return news_list

    except Exception as e:
        return "Error"


if __name__ == "__main__":
    news = get_news_from_last_week("כיי")
    print("News from the last week:")
    for item in news:
        print(item)
