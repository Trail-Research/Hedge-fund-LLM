import tweepy
import json
from dotenv import load_dotenv
import os

load_dotenv()

################################################################################
# X (Twitter) API
################################################################################
def get_x_posts(keyword: str, tweet_limit: int = 10) -> str:
    """
    Retrieves X (Twitter) posts related to a specific keyword.
    
    Args:
        keyword (str): The search term to look for in tweets (e.g., 'AAPL' for Apple)
        tweet_limit (int, optional): Maximum number of tweets to retrieve
        
    Returns:
        str: A JSON string containing tweets with the following structure:
    """
    # X API authentication
    client = tweepy.Client(
        bearer_token=os.getenv("X_BEARER_TOKEN"),
        consumer_key=os.getenv("X_API_KEY"),
        consumer_secret=os.getenv("X_API_SECRET"),
        access_token=os.getenv("X_ACCESS_TOKEN"),
        access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET")
    )

    # Search tweets
    tweets = client.search_recent_tweets(
        query=keyword,
        max_results=tweet_limit,
        tweet_fields=['created_at', 'public_metrics', 'author_id']
    )

    result = {"tweets": []}

    if tweets.data:
        for tweet in tweets.data:
            tweet_data = {
                "text": tweet.text,
                "created_at": str(tweet.created_at),
                "author": str(tweet.author_id),
                "likes": tweet.public_metrics['like_count'],
                "retweets": tweet.public_metrics['retweet_count'],
                "replies": tweet.public_metrics['reply_count']
            }
            result["tweets"].append(tweet_data)

    return json.dumps(result, indent=4)

# Example usage
if __name__ == "__main__":
    x_data = get_x_posts(keyword="AAPL", tweet_limit=10)
    print("\nX data:")
    print(x_data)
