from src.trading_system.utils.data.fundamentals import get_all_fundamentals, get_company_info
from src.trading_system.utils.llm.llm_manager import LLMManager
import json

class FundamentalsAgent:
    def __init__(self):
        self.llm_manager = LLMManager()

    def process(self, stock_symbol: str) -> str:
        """
        Process fundamental data for a given stock symbol.
        
        Args:
            stock_symbol (str): The stock symbol to analyze
            
        Returns:
            str: JSON string containing fundamental data and LLM analysis
        """
        print(f"[FundamentalsAgent] Processing fundamental data for {stock_symbol}...")
        
        try:
            # Get all fundamental data
            fundamental_data = get_all_fundamentals(stock_symbol)
            
            # Get additional company info from Yahoo Finance
            company_info = get_company_info(stock_symbol)
            
            # Analyze data with LLM
            analysis = self.llm_manager.analyze_fundamentals(fundamental_data, json.loads(company_info))
            
            # Return both raw data and analysis
            result = {
                "raw_data": {
                    "fundamentals": fundamental_data,
                    "company_info": json.loads(company_info)
                },
                "analysis": analysis
            }
            
            print(f"[FundamentalsAgent] Successfully processed fundamental data for {stock_symbol}")
            return json.dumps(result)
            
        except Exception as e:
            error_msg = f"Error processing fundamental data: {str(e)}"
            print(f"[FundamentalsAgent] {error_msg}")
            return json.dumps({"error": error_msg}) 