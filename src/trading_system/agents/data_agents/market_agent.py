from src.trading_system.utils.data.markets_values import get_market_data
from src.trading_system.utils.llm.llm_manager import LLMManager
import json

class MarketAgent:
    def __init__(self):
        self.llm_manager = LLMManager()

    def process(self, stock_symbol: str) -> str:
        """
        Process market data for a given stock symbol.
        
        Args:
            stock_symbol (str): The stock symbol to analyze
            
        Returns:
            str: JSON string containing market data and LLM analysis
        """
        print(f"[MarketAgent] Processing market data for {stock_symbol}...")
        
        try:
            # Get market data for the given symbol
            market_data = get_market_data(stock_symbol)
            
            # Analyze data with LLM
            analysis = self.llm_manager.analyze_market_trends(json.loads(market_data))
            
            # Return both raw data and analysis
            result = {
                "raw_data": json.loads(market_data),
                "analysis": analysis
            }
            
            print(f"[MarketAgent] Successfully processed market data for {stock_symbol}")
            return json.dumps(result)
            
        except Exception as e:
            error_msg = f"Error processing market data: {str(e)}"
            print(f"[MarketAgent] {error_msg}")
            return json.dumps({"error": error_msg}) 