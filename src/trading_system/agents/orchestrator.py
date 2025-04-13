from src.trading_system.agents.data_agents.social_media_agent import SocialMediaAgent
from src.trading_system.agents.data_agents.fundamentals_agent import FundamentalsAgent
from trading_system.agents.news_analyst.news_agent import NewsAgent
from trading_system.agents.market_agent.market_agent import MarketAgent
from src.trading_system.utils.llm.llm_manager import LLMManager
from trading_system.data_ingestion.reddit.sentiment_analyzer import RedditSentimentAnalyzer
from trading_system.data_ingestion.news.sentiment_analyzer import NewsSentimentAnalyzer
import json
import sys

class Orchestrator:
    def __init__(self):
        # Initialize all data agents
        self.social_agent = SocialMediaAgent()
        self.fundamentals_agent = FundamentalsAgent()
        self.news_agent = NewsAgent()
        self.market_agent = MarketAgent()
        self.llm_manager = LLMManager()
        self.reddit_analyzer = RedditSentimentAnalyzer()
        self.news_analyzer = NewsSentimentAnalyzer()

    def process(self, stock_symbol: str) -> dict:
        """
        Process the input data through all agents and coordinate their responses.
        
        Args:
            stock_symbol (str): The stock symbol to analyze
            
        Returns:
            dict: Dictionary containing all processed data and final recommendation
        """
        print(f"[Orchestrator] Starting analysis for {stock_symbol}...")
        
        # Process through each agent
        social_result = json.loads(self.social_agent.process(stock_symbol))
        fundamentals_result = json.loads(self.fundamentals_agent.process(stock_symbol))
        news_result = json.loads(self.news_agent.process(stock_symbol))
        market_result = json.loads(self.market_agent.process(stock_symbol))
        
        # Check for errors in agent results
        errors = []
        if "error" in social_result:
            errors.append(f"Social Media: {social_result['error']}")
        if "error" in fundamentals_result:
            errors.append(f"Fundamentals: {fundamentals_result['error']}")
        if "error" in news_result:
            errors.append(f"News: {news_result['error']}")
        if "error" in market_result:
            errors.append(f"Market: {market_result['error']}")
        
        if errors:
            return {
                "error": "One or more agents encountered errors:",
                "details": errors
            }
        
        try:
            # Parse all results
            results = {
                "social": social_result,
                "fundamentals": fundamentals_result,
                "news": news_result,
                "market": market_result
            }
            
            # Analyze sentiments using the specialized analyzers
            social_sentiment = self.reddit_analyzer.analyze_sentiment(social_result["data"])
            news_sentiment = self.news_analyzer.analyze_sentiment(news_result["data"])
            
            # Generate final recommendation based on all analyses
            recommendation = self.llm_manager.generate_trading_recommendation({
                "fundamentals": results["fundamentals"]["analysis"],
                "social": social_sentiment,
                "news": news_sentiment,
                "market": results["market"]["analysis"]
            })
            
            # Add recommendation to results
            results["recommendation"] = recommendation
            
            print(f"[Orchestrator] Successfully processed all data for {stock_symbol}")
            return results
            
        except Exception as e:
            error_msg = f"Error processing data: {str(e)}"
            print(f"[Orchestrator] {error_msg}")
            return {"error": error_msg}
    
    def _analyze_social_sentiment(self, social_data: dict) -> str:
        """
        Analyze sentiment from social media data.
        In a real implementation, this would use NLP to analyze the sentiment.
        """
        # Exemple simplifié : si plus de 60% des posts ont un score positif
        positive_posts = sum(1 for post in social_data if post.get("score", 0) > 0)
        total_posts = len(social_data)
        if total_posts > 0 and (positive_posts / total_posts) > 0.6:
            return "positive"
        return "neutral"
    
    def _analyze_news_sentiment(self, news_data: dict) -> str:
        """
        Analyze sentiment from news data.
        In a real implementation, this would use NLP to analyze the sentiment.
        """
        # Exemple simplifié : si plus de 60% des articles ont un titre négatif
        negative_articles = sum(1 for article in news_data if any(word in article.get("headline", "").lower() 
                            for word in ["down", "fall", "drop", "decline", "loss"]))
        total_articles = len(news_data)
        if total_articles > 0 and (negative_articles / total_articles) > 0.6:
            return "negative"
        return "neutral"
