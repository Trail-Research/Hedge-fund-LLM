from src.trading_system.utils.data.social_media import get_reddit_posts
from src.trading_system.utils.llm.llm_manager import LLMManager
import json

class SocialMediaAgent:
    def __init__(self):
        self.llm_manager = LLMManager()

    def process(self, stock_symbol: str) -> str:
        """
        Process social media data for a given stock symbol.
        
        Args:
            stock_symbol (str): The stock symbol to analyze
            
        Returns:
            str: JSON string containing Reddit posts and LLM analysis
        """
        print(f"[SocialMediaAgent] Processing social media data for {stock_symbol}...")
        
        try:
            # Get Reddit posts for the given symbol
            social_data = get_reddit_posts(keyword=stock_symbol, post_limit=10, comment_limit=5)
            
            # Analyze data with LLM
            analysis = self.llm_manager.analyze_social_sentiment(json.loads(social_data))
            
            # Return both raw data and analysis
            result = {
                "raw_data": json.loads(social_data),
                "analysis": analysis
            }
            
            print(f"[SocialMediaAgent] Successfully processed social media data for {stock_symbol}")
            return json.dumps(result)
            
        except Exception as e:
            error_msg = f"Error processing social media data: {str(e)}"
            print(f"[SocialMediaAgent] {error_msg}")
            return json.dumps({"error": error_msg}) 