from trading_system.utils.llm.base_agent import BaseAgent
from .prompts import NEWS_ANALYSIS_PROMPT
from trading_system.data_processing.news.finnhub import get_financial_news

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
        news_data = get_financial_news(stock_symbol)
        
        prompt = self.build_prompt(news_data)
        analysis = self.model(prompt)

        return {
            "news_data": news_data,
            "analysis": analysis
        } 