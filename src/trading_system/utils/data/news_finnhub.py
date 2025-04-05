import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

def get_financial_news(symbol: str, api_key: str, max_articles: int = 5):
    url = f"https://finnhub.io/api/v1/company-news?symbol={symbol}&from=2024-04-01&to=2025-04-05&token={api_key}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Erreur lors de la récupération des actualités")

    news_data = response.json()
    
    # On prend les n dernières news
    selected_news = news_data[:max_articles]
    
    # Formatage pour LLM
    formatted = [
        {
            "headline": article["headline"],
            "summary": article["summary"],
            "datetime": article["datetime"],
            "source": article["source"],
            "url": article["url"]
        }
        for article in selected_news
    ]

    return json.dumps(formatted, indent=4)

# Exemple d’utilisation
if __name__ == "__main__":
    API_KEY = os.getenv("FINNHUB_API_KEY")
    news_json = get_financial_news("AAPL", API_KEY)
    print(news_json)
