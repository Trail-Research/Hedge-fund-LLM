import praw
import json
from dotenv import load_dotenv
import os

load_dotenv()

def get_reddit_posts(keyword: str, post_limit: int = 10, comment_limit: int = 10) -> str:
    """
    Retrieves Reddit posts and comments related to a specific keyword from financial subreddits.
    
    Args:
        keyword (str): The search term to look for in posts (e.g., 'AAPL' for Apple)
        post_limit (int, optional): Maximum number of posts to retrieve
        comment_limit (int, optional): Maximum number of comments per post to retrieve
        
    Returns:
        str: A JSON string containing posts and their comments with the following structure:
    """
    # Reddit API authentication
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_KEY"),
        user_agent="hedgefun-bot"
    )

    subreddit = reddit.subreddit("stocks+investing+wallstreetbets")
    posts = subreddit.search(keyword, sort="new", limit=post_limit)

    result = []

    for post in posts:
        post_data = {
            "title": post.title,
            "url": post.url,
            "score": post.score,
            "num_comments": post.num_comments,
            "comments": []
        }

        post.comments.replace_more(limit=0)
        count = 0
        for comment in post.comments.list():
            if count >= comment_limit:
                break
            post_data["comments"].append({
                "author": str(comment.author),
                "body": comment.body,
                "score": comment.score,
                "created_utc": comment.created_utc,
                "depth": comment.depth
            })
            count += 1

        result.append(post_data)

    return json.dumps(result, indent=4)

# Example usage
if __name__ == "__main__":
    data = get_reddit_posts(keyword="AAPL", post_limit=40, comment_limit=0)
    print(data)
