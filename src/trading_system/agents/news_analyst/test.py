"""
Test module for the NewsAnalyst agent.
This module provides a function that returns predetermined data for testing purposes.
"""

import json

def get_mock_news_data():
    """
    Returns a predetermined JSON string containing mock news data.
    
    Returns:
        str: A JSON string containing mock news data
    """
    mock_data = {
        "articles": [
            {
                "title": "Apple Reports Record Q2 Earnings, Beats Expectations",
                "source": "Financial Times",
                "published_at": "2023-04-28T20:30:00Z",
                "url": "https://example.com/article1",
                "summary": "Apple Inc. reported record second-quarter earnings, surpassing analyst expectations. The company posted revenue of $94.8 billion, up 2% year-over-year, and earnings per share of $1.52, beating the consensus estimate of $1.43. iPhone sales remained strong, while services revenue continued to grow at a double-digit pace.",
                "sentiment": "positive"
            },
            {
                "title": "Apple's New iPhone 15 Expected to Feature USB-C Port",
                "source": "Bloomberg",
                "published_at": "2023-04-25T14:15:00Z",
                "url": "https://example.com/article2",
                "summary": "Apple's upcoming iPhone 15 is expected to feature a USB-C port, marking a significant change from the company's proprietary Lightning connector. This change is likely in response to European Union regulations requiring standardized charging ports. The move could impact Apple's accessory revenue but may improve user experience and reduce electronic waste.",
                "sentiment": "neutral"
            },
            {
                "title": "Apple Expands Services Business with New Subscription Offerings",
                "source": "Reuters",
                "published_at": "2023-04-20T09:45:00Z",
                "url": "https://example.com/article3",
                "summary": "Apple is expanding its services business with new subscription offerings, including an enhanced Apple TV+ service and additional features for Apple One subscribers. The company aims to increase recurring revenue streams as hardware sales growth moderates. Analysts view this strategy positively as it provides more stable revenue and higher margins.",
                "sentiment": "positive"
            },
            {
                "title": "Supply Chain Concerns Impact Apple's Production in China",
                "source": "Wall Street Journal",
                "published_at": "2023-04-18T16:20:00Z",
                "url": "https://example.com/article4",
                "summary": "Apple is facing supply chain challenges in China, with some production delays reported for certain iPhone models. The company is reportedly accelerating its efforts to diversify manufacturing outside of China, with increased production in India and Vietnam. These geopolitical tensions could impact Apple's ability to meet demand in key markets.",
                "sentiment": "negative"
            },
            {
                "title": "Apple's AI Strategy Takes Shape with New Initiatives",
                "source": "TechCrunch",
                "published_at": "2023-04-15T11:30:00Z",
                "url": "https://example.com/article5",
                "summary": "Apple is quietly building its artificial intelligence capabilities, with new initiatives expected to be announced at the upcoming Worldwide Developers Conference. The company is reportedly developing AI features for Siri, Photos, and other core applications. While Apple has been slower to market with AI compared to competitors, its privacy-focused approach may appeal to users concerned about data security.",
                "sentiment": "positive"
            }
        ],
        "summary": {
            "total_articles": 5,
            "sentiment": "positive",
            "key_topics": ["Earnings", "iPhone", "Services", "Supply Chain", "AI"]
        }
    }
    
    return json.dumps(mock_data, indent=4)

def get_mock_analysis():
    """
    Returns a predetermined analysis of the news data.
    
    Returns:
        str: A string containing the analysis
    """
    return """
    News Analysis for AAPL:
    
    Overall Sentiment: Positive
    
    Key News Themes:
    1. Strong Financial Performance
       - Record Q2 earnings reported, beating expectations
       - Revenue growth of 2% year-over-year
       - Services business showing robust growth
    
    2. Product Development
       - iPhone 15 expected to feature USB-C port
       - Changes likely driven by EU regulations
       - Potential impact on accessory revenue
    
    3. Strategic Initiatives
       - Expansion of services business with new subscription offerings
       - Focus on recurring revenue streams
       - Development of AI capabilities across core applications
    
    4. Supply Chain Challenges
       - Production delays reported in China
       - Accelerating diversification of manufacturing
       - Geopolitical tensions as a risk factor
    
    Market Impact Analysis:
    The positive news regarding earnings and strategic initiatives likely outweighs the supply chain concerns in the short term. The company's ability to beat expectations despite challenging macroeconomic conditions demonstrates resilience.
    
    The expansion of services and AI initiatives positions Apple for long-term growth beyond hardware sales, which is viewed positively by investors. However, the supply chain diversification efforts may increase costs in the near term.
    
    The transition to USB-C, while potentially impacting accessory revenue, is a necessary adaptation to regulatory changes and may improve user experience in the long run.
    
    Conclusion:
    The news sentiment for AAPL is predominantly positive, with strong financial performance and strategic initiatives being the dominant themes. While there are some concerns about supply chain issues, these appear to be manageable risks rather than significant threats to the company's overall trajectory. The focus on services growth and AI development suggests Apple is positioning itself for continued success in an evolving technology landscape.
    """

def test_news_analyst(stock_symbol: str) -> dict:
    """
    Test function that simulates the NewsAnalyst's invoke method.
    
    Args:
        stock_symbol (str): The stock symbol to analyze (not used in mock data)
        
    Returns:
        dict: A dictionary containing mock news data and analysis
    """
    print(f"[NewsAnalyst] Starting mock news data fetch for {stock_symbol}")
    
    # Get mock data
    news_data = get_mock_news_data()
    print(f"[NewsAnalyst] Successfully fetched mock news data for {stock_symbol}")
    
    # Get mock analysis
    analysis = get_mock_analysis()
    print("[NewsAnalyst] Generated mock analysis")
    
    return {
        "news_data": news_data,
        "analysis": analysis
    }

# Example usage
if __name__ == "__main__":
    result = test_news_analyst("AAPL")
    print("\n=== Mock News Data ===")
    print(result["news_data"])
    print("\n=== Mock Analysis ===")
    print(result["analysis"]) 