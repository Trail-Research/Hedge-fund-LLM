class NewsSentimentAnalyzer:
    NEGATIVE_KEYWORDS = ["down", "fall", "drop", "decline", "loss"]
    
    @staticmethod
    def analyze_sentiment(news_data: dict) -> str:
        """
        Analyze sentiment from news data.
        Args:
            news_data: Dictionary containing news articles data
        Returns:
            str: Sentiment analysis result ('positive', 'neutral', 'negative')
        """
        negative_articles = sum(
            1 for article in news_data 
            if any(word in article.get("headline", "").lower() 
                  for word in NewsSentimentAnalyzer.NEGATIVE_KEYWORDS)
        )
        total_articles = len(news_data)
        
        if total_articles > 0 and (negative_articles / total_articles) > 0.6:
            return "negative"
        return "neutral" 