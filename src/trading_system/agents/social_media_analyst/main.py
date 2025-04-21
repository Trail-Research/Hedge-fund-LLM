from trading_system.utils.llm.base_agent import BaseAgent
from .prompts import SOCIAL_MEDIA_ANALYSIS_PROMPT
from trading_system.data_processing.social_media import get_social_data
import time

class SocialMediaAnalyst(BaseAgent):
    def build_prompt(self, social_data: dict) -> str:
        return SOCIAL_MEDIA_ANALYSIS_PROMPT.format(
            social_data=social_data
        )
    
    def invoke(self, stock_symbol: str) -> dict:
        """
        Invoke method to handle social media data fetching
        Args:
            stock_symbol: The stock symbol to analyze
        Returns:
            dict: Dictionary containing both raw social data and analysis
        """
        print(f"[SocialMediaAnalyst] Starting social media data fetch for {stock_symbol}")
        try:
            social_data = get_social_data(stock_symbol)
            print(f"[SocialMediaAnalyst] Successfully fetched social media data for {stock_symbol}")
            
            print("[SocialMediaAnalyst] Building analysis prompt...")
            prompt = self.build_prompt(social_data)
            
            print("[SocialMediaAnalyst] Generating analysis...")
            analysis = self.model(prompt)
            print("[SocialMediaAnalyst] Analysis generated successfully")

            return {
                "social_data": social_data,
                "analysis": analysis
            }
        except Exception as e:
            print(f"[SocialMediaAnalyst] Error processing {stock_symbol}: {str(e)}")
            print(f"[SocialMediaAnalyst] Error type: {type(e).__name__}")
            print(f"[SocialMediaAnalyst] Error details: {str(e)}")
            raise  # Re-raise the exception to be handled by the orchestrator 