from src.trading_system.utils.data.news import get_financial_news
from src.trading_system.utils.llm.llm_manager import LLMManager
import json

class NewsAgent:
    def __init__(self):
        self.llm_manager = LLMManager()

    def process(self, stock_symbol: str) -> str:
        """
        Process news data for a given stock symbol.
        
        Args:
            stock_symbol (str): The stock symbol to analyze
            
        Returns:
            str: JSON string containing news articles and LLM analysis
        """
        print(f"[NewsAgent] Processing news data for {stock_symbol}...")
        
        try:
            # Get financial news for the given symbol
            news_data = get_financial_news(stock_symbol)
            
            # Analyze data with LLM
            analysis = self.llm_manager.analyze_news(json.loads(news_data))
            
            # Return both raw data and analysis
            result = {
                "raw_data": json.loads(news_data),
                "analysis": analysis
            }
            
            print(f"[NewsAgent] Successfully processed news data for {stock_symbol}")
            return json.dumps(result)
            
        except Exception as e:
            error_msg = f"Error processing news data: {str(e)}"
            print(f"[NewsAgent] {error_msg}")
            return json.dumps({"error": error_msg}) 