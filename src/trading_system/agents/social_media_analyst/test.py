"""
Test module for the SocialMediaAnalyst agent.
This module provides a function that returns predetermined data for testing purposes.
"""

import json
import os

def get_mock_social_data():
    """
    Returns a predetermined JSON string containing mock social media data.
    
    Returns:
        str: A JSON string containing mock social media data
    """
    mock_data = {
        "keyword": "AAPL",
        "reddit": {
            "posts_count": 3,
            "posts": [
                {
                    "title": "AAPL stock analysis - why I'm bullish",
                    "score": 125,
                    "num_comments": 3,
                    "comments": [
                        {
                            "text": "I agree with your analysis. Apple's ecosystem is incredibly strong.",
                            "score": 32,
                            "sentiment": "positive"
                        },
                        {
                            "text": "Don't forget about their services revenue growth.",
                            "score": 18,
                            "sentiment": "positive"
                        },
                        {
                            "text": "I'm concerned about their dependency on China for manufacturing.",
                            "score": -5,
                            "sentiment": "negative"
                        }
                    ]
                },
                {
                    "title": "AAPL earnings discussion thread",
                    "score": 89,
                    "num_comments": 2,
                    "comments": [
                        {
                            "text": "Revenue beat expectations but margins were slightly lower than expected.",
                            "score": 24,
                            "sentiment": "neutral"
                        },
                        {
                            "text": "The buyback program is massive, that's what matters most to me.",
                            "score": 15,
                            "sentiment": "positive"
                        }
                    ]
                },
                {
                    "title": "AAPL to $200 by EOY? 🚀",
                    "score": 45,
                    "num_comments": 2,
                    "comments": [
                        {
                            "text": "I'm all in on calls. This is going to the moon!",
                            "score": 12,
                            "sentiment": "positive"
                        },
                        {
                            "text": "Be careful with the hype. AAPL is a solid company but $200 is ambitious.",
                            "score": 8,
                            "sentiment": "neutral"
                        }
                    ]
                }
            ]
        },
        "twitter": {
            "tweets_count": 5,
            "tweets": [
                {
                    "text": "Just bought more $AAPL shares. The new iPhone sales are going to be massive! #investing",
                    "created_at": "2023-04-15T12:30:45Z",
                    "likes": 156,
                    "retweets": 23,
                    "replies": 12,
                    "sentiment": "positive"
                },
                {
                    "text": "Apple's services revenue growth is impressive. $AAPL continues to diversify beyond hardware. #stocks",
                    "created_at": "2023-04-14T18:22:10Z",
                    "likes": 89,
                    "retweets": 15,
                    "replies": 8,
                    "sentiment": "positive"
                },
                {
                    "text": "Concerned about $AAPL's exposure to China. Manufacturing risks could impact supply chain. #investing",
                    "created_at": "2023-04-13T09:45:30Z",
                    "likes": 45,
                    "retweets": 12,
                    "replies": 18,
                    "sentiment": "negative"
                },
                {
                    "text": "AAPL earnings beat expectations. Strong iPhone sales and services growth. $AAPL #stocks",
                    "created_at": "2023-04-12T20:15:22Z",
                    "likes": 234,
                    "retweets": 56,
                    "replies": 34,
                    "sentiment": "positive"
                },
                {
                    "text": "Apple's buyback program is massive. $AAPL returning value to shareholders. #investing",
                    "created_at": "2023-04-11T14:33:18Z",
                    "likes": 167,
                    "retweets": 42,
                    "replies": 21,
                    "sentiment": "positive"
                }
            ]
        },
        "summary": {
            "total_mentions": 8,
            "sentiment": "positive",
            "key_topics": ["iPhone", "Services", "China", "Earnings", "Buyback"]
        },
        "structured_text": """
    Social Media Analysis for AAPL:
    
    Total Mentions: 8
    
    Reddit:
    - 3 posts found
    - Top post: AAPL stock analysis - why I'm bullish
    
    Twitter:
    - 5 tweets found
    - Most liked tweet: AAPL earnings beat expectations. Strong iPhone sales and services growth. $AAPL #stocks
    
    Overall Sentiment: positive
    """
    }
    
    return json.dumps(mock_data, indent=4)

def get_mock_analysis():
    """
    Returns a predetermined analysis of the social media data.
    
    Returns:
        str: A string containing the analysis
    """
    return """
    Social Media Analysis for AAPL:
    
    Overall Sentiment: Positive
    
    Key Insights:
    1. Strong positive sentiment across both Reddit and Twitter platforms
    2. Recent earnings results were well-received by the community
    3. Services revenue growth and ecosystem strength are frequently mentioned positives
    4. Some concerns about China manufacturing dependencies, but these are minority views
    
    Reddit Analysis:
    - Most discussed topics: iPhone sales, services revenue, China manufacturing
    - Top post has 125 upvotes and discusses bullish outlook
    - Comments show mixed sentiment but predominantly positive
    
    Twitter Analysis:
    - High engagement on earnings-related tweets
    - Strong positive sentiment on buyback program
    - Some concerns about supply chain risks
    
    Conclusion:
    Social media sentiment for AAPL is predominantly positive, with strong community confidence in the company's ecosystem, services growth, and recent financial performance. While there are some concerns about manufacturing dependencies, these are not the dominant narrative in the social media discussion.
    """

def test_social_media_analyst(stock_symbol: str) -> dict:
    """
    Test function that simulates the SocialMediaAnalyst's invoke method.
    
    Args:
        stock_symbol (str): The stock symbol to analyze (not used in mock data)
        
    Returns:
        dict: A dictionary containing mock social data and analysis
    """
    print(f"[SocialMediaAnalyst] Starting mock social media data fetch for {stock_symbol}")
    
    # Get mock data
    social_data = get_mock_social_data()
    print(f"[SocialMediaAnalyst] Successfully fetched mock social media data for {stock_symbol}")
    
    # Get mock analysis
    analysis = get_mock_analysis()
    print("[SocialMediaAnalyst] Generated mock analysis")
    
    return {
        "social_data": social_data,
        "analysis": analysis
    }

# Example usage
if __name__ == "__main__":
    result = test_social_media_analyst("AAPL")
    print("\n=== Mock Social Media Data ===")
    print(result["social_data"])
    print("\n=== Mock Analysis ===")
    print(result["analysis"]) 