from trading_system.utils.llm.base_agent import BaseAgent
from .prompts import MARKET_ANALYSIS_PROMPT
from trading_system.data_processing.fundamentals.markets_values import get_market_data  # You'll need to implement this

class MarketAnalyst(BaseAgent):
    def build_prompt(self, market_data: dict) -> str:
        return MARKET_ANALYSIS_PROMPT.format(
            market_data=market_data
        )
    
    def invoke(self, stock_symbol: str) -> str:
        """
        Invoke method to handle market data fetching
        Args:
            stock_symbol: The stock symbol to analyze
        Returns:
            str: Market analysis result
        """
        # Fetch market data for the given stock symbol
        market_data = get_market_data(stock_symbol)
        
        # Build and execute the prompt
        prompt = self.build_prompt(market_data)
        return self.model(prompt)