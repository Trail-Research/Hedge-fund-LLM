from trading_system.utils.llm.base_agent import BaseAgent
from .prompts import FUNDAMENTALS_ANALYSIS_PROMPT
from trading_system.data_ingestion.fundamentals import get_fundamentals_data, get_company_info

class FundamentalsAnalyst(BaseAgent):
    def build_prompt(self, fundamentals_data: dict, company_info: dict) -> str:
        return FUNDAMENTALS_ANALYSIS_PROMPT.format(
            fundamentals_data=fundamentals_data,
            company_info=company_info
        )
    
    def invoke(self, stock_symbol: str) -> dict:
        """
        Invoke method to handle fundamentals data fetching
        Args:
            stock_symbol: The stock symbol to analyze
        Returns:
            dict: Dictionary containing both raw fundamentals data and analysis
        """
        fundamentals_data = get_fundamentals_data(stock_symbol)
        company_info = get_company_info(stock_symbol)
        
        prompt = self.build_prompt(fundamentals_data, company_info)
        analysis = self.model(prompt)

        return {
            "fundamentals_data": fundamentals_data,
            "company_info": company_info,
            "analysis": analysis
        }