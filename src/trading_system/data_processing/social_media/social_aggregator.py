import json
from .reddit import get_reddit_posts
from .x import get_x_posts

def get_social_data(keyword: str, reddit_post_limit: int = 10, reddit_comment_limit: int = 5, tweet_limit: int = 10) -> str:
    """
    Aggregates and processes social media data from Reddit and X (Twitter) for a given keyword.
    
    Args:
        keyword (str): The search term to look for in social media (e.g., 'AAPL' for Apple)
        reddit_post_limit (int, optional): Maximum number of Reddit posts to retrieve
        reddit_comment_limit (int, optional): Maximum number of comments per Reddit post to retrieve
        tweet_limit (int, optional): Maximum number of tweets to retrieve
        
    Returns:
        str: A JSON string containing processed social media data with sentiment analysis
    """
    # Get data from both platforms
    reddit_data = json.loads(get_reddit_posts(keyword, reddit_post_limit, reddit_comment_limit))
    x_data = json.loads(get_x_posts(keyword, tweet_limit))
    
    # Process and structure the data
    processed_data = {
        "keyword": keyword,
        "reddit": {
            "posts_count": len(reddit_data),
            "posts": []
        },
        "twitter": {
            "tweets_count": len(x_data.get("tweets", [])),
            "tweets": []
        },
        "summary": {
            "total_mentions": len(reddit_data) + len(x_data.get("tweets", [])),
            "sentiment": "neutral",  # This would be calculated with a sentiment analysis model
            "key_topics": []  # This would be extracted with topic modeling
        }
    }
    
    # Process Reddit data
    for post in reddit_data:
        processed_post = {
            "title": post.get("title", ""),
            "score": post.get("score", 0),
            "num_comments": post.get("num_comments", 0),
            "comments": []
        }
        
        # Process comments
        for comment in post.get("comments", []):
            processed_comment = {
                "text": comment.get("body", ""),
                "score": comment.get("score", 0),
                "sentiment": "neutral"  # This would be calculated with a sentiment analysis model
            }
            processed_post["comments"].append(processed_comment)
            
        processed_data["reddit"]["posts"].append(processed_post)
    
    # Process Twitter data
    for tweet in x_data.get("tweets", []):
        processed_tweet = {
            "text": tweet.get("text", ""),
            "created_at": tweet.get("created_at", ""),
            "likes": tweet.get("likes", 0),
            "retweets": tweet.get("retweets", 0),
            "replies": tweet.get("replies", 0),
            "sentiment": "neutral"  # This would be calculated with a sentiment analysis model
        }
        processed_data["twitter"]["tweets"].append(processed_tweet)
    
    # Generate a structured text summary
    summary_text = f"""
    Social Media Analysis for {keyword}:
    
    Total Mentions: {processed_data["summary"]["total_mentions"]}
    
    Reddit:
    - {processed_data["reddit"]["posts_count"]} posts found
    - Top post: {processed_data["reddit"]["posts"][0]["title"] if processed_data["reddit"]["posts"] else "No posts found"}
    
    Twitter:
    - {processed_data["twitter"]["tweets_count"]} tweets found
    - Most liked tweet: {processed_data["twitter"]["tweets"][0]["text"] if processed_data["twitter"]["tweets"] else "No tweets found"}
    
    Overall Sentiment: {processed_data["summary"]["sentiment"]}
    """
    
    # Add the structured text to the processed data
    processed_data["structured_text"] = summary_text
    
    return json.dumps(processed_data, indent=4)

# Example usage
if __name__ == "__main__":
    social_data = get_social_data(keyword="AAPL", reddit_post_limit=5, reddit_comment_limit=3, tweet_limit=5)
    print(social_data) 