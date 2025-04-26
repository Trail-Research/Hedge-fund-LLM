from trading_system.utils.llm.base_agent import BaseAgent
from .prompts import NEWS_ANALYSIS_PROMPT
from trading_system.data_processing.news.finnhub import get_financial_news
import time

class NewsAnalyst(BaseAgent):
    def build_prompt(self, news_data: dict) -> str:
        return NEWS_ANALYSIS_PROMPT.format(
            news_data=news_data
        )
    
    def invoke(self, stock_symbol: str) -> dict:
        """
        Invoke method to handle news data fetching
        Args:
            stock_symbol: The stock symbol to analyze
        Returns:
            dict: Dictionary containing both raw news data and analysis
        """
        print(f"[NewsAnalyst] Starting news data fetch for {stock_symbol}")
        try:
            news_data = get_financial_news(stock_symbol)
            print(f"[NewsAnalyst] Successfully fetched news data for {stock_symbol}")
            
            print("[NewsAnalyst] Building analysis prompt...")
            prompt = self.build_prompt(news_data)
            
            print("[NewsAnalyst] Generating analysis...")
            analysis = self.model(prompt)
            print("[NewsAnalyst] Analysis generated successfully")

            return {
                "news_data": news_data,
                "analysis": analysis
            }
        except Exception as e:
            print(f"[NewsAnalyst] Error processing {stock_symbol}: {str(e)}")
            print(f"[NewsAnalyst] Error type: {type(e).__name__}")
            print(f"[NewsAnalyst] Error details: {str(e)}")
            raise  # Re-raise the exception to be handled by the orchestrator 