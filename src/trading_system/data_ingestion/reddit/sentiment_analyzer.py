class RedditSentimentAnalyzer:
    @staticmethod
    def analyze_sentiment(social_data: dict) -> str:
        """
        Analyze sentiment from social media data.
        Args:
            social_data: Dictionary containing Reddit posts data
        Returns:
            str: Sentiment analysis result ('positive', 'neutral', 'negative')
        """
        positive_posts = sum(1 for post in social_data if post.get("score", 0) > 0)
        total_posts = len(social_data)
        
        if total_posts > 0 and (positive_posts / total_posts) > 0.6:
            return "positive"
        return "neutral" 