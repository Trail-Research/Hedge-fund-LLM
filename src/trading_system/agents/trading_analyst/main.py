from trading_system.utils.llm.base_agent import BaseAgent
from .prompts import TRADING_RECOMMENDATION_PROMPT

class TradingAnalyst(BaseAgent):
    def build_prompt(self, analyses: dict) -> str:
        return TRADING_RECOMMENDATION_PROMPT.format(
            fundamentals_analysis=analyses.get('fundamentals', 'N/A'),
            social_analysis=analyses.get('social', 'N/A'),
            news_analysis=analyses.get('news', 'N/A'),
            market_analysis=analyses.get('market', 'N/A')
        ) 