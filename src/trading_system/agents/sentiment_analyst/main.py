from trading_system.utils.llm.base_agent import BaseAgent
from .prompts import SENTIMENT_ANALYSIS_PROMPT
from trading_system.data_ingestion.social_media import get_social_data

class SentimentAnalyst(BaseAgent):
    def build_prompt(self, social_data: dict) -> str:
        return SENTIMENT_ANALYSIS_PROMPT.format(
            social_data=social_data
        )
    
    def invoke(self, stock_symbol: str) -> dict:
        """
        Invoke method to handle social sentiment data fetching
        Args:
            stock_symbol: The stock symbol to analyze
        Returns:
            dict: Dictionary containing both raw social data and analysis
        """
        social_data = get_social_data(stock_symbol)
        
        prompt = self.build_prompt(social_data)
        analysis = self.model(prompt)

        return {
            "social_data": social_data,
            "analysis": analysis
        } 