import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

################################################################################
# Finnhub API
################################################################################
def get_financial_news(symbol: str, api_key: str, max_articles: int = 5) -> str:
    """
    Retrieves financial news for a given stock symbol using the Finnhub API.
    
    Args:
        symbol (str): The stock symbol to fetch news for (e.g., 'AAPL' for Apple)
        api_key (str): Finnhub API key
        max_articles (int, optional): Maximum number of articles to return. Defaults to 5.
        
    Returns:
        str: A JSON string containing the formatted news articles
    """
    url = f"https://finnhub.io/api/v1/company-news?symbol={symbol}&from=2024-04-01&to=2025-04-05&token={api_key}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Error while fetching news")

    news_data = response.json()
    
    # Take the n most recent news articles
    selected_news = news_data[:max_articles]
    
    # Format for LLM
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

# Example usage
if __name__ == "__main__":
    API_KEY = os.getenv("FINNHUB_API_KEY")
    news_json = get_financial_news("AAPL", API_KEY)
    print(news_json)
