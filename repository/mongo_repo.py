from datetime import datetime, timedelta
from database.config_mongo import collection

def get_news_from_last_week(keyword):
    try:
        result = keyword.replace(",", " | ")
        one_week_ago = datetime.now() - timedelta(weeks=1)
        query = {
            "date": {"$gte": one_week_ago.isoformat()},
            "message": {"$regex": f".*{result}.*"}
        }
        results = collection.find(query)

        news_list = list(results)
        print("Raw data:", news_list)
        processed_list = [i for i in news_list]
        print("Processed data:", processed_list)

        return processed_list

    except Exception as e:
        print(f"Conversion error: {e}")
        return []

if __name__ == "__main__":
    news = get_news_from_last_week("כיי")
    print("News from the last week:")
    for item in news:
        print(item)
