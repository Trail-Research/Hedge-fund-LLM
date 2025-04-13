from trading_system.utils.llm.base_agent import BaseAgent
from .prompts import MARKET_ANALYSIS_PROMPT
from trading_system.data_ingestion.markets_values import get_market_data

class MarketAnalyst(BaseAgent):
    def build_prompt(self, market_data: dict) -> str:
        return MARKET_ANALYSIS_PROMPT.format(
            market_data=market_data
        )
    
    def invoke(self, stock_symbol: str) -> dict:
        """
        Invoke method to handle market data fetching
        Args:
            stock_symbol: The stock symbol to analyze
        Returns:
            dict: Dictionary containing both raw market data and analysis
        """
        # Fetch market data for the given stock symbol
        market_data = get_market_data(stock_symbol)
        
        # Build and execute the prompt
        prompt = self.build_prompt(market_data)
        analysis = self.model(prompt)

        return {
            "market_data": market_data,
            "analysis": analysis
        }