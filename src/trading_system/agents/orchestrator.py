from src.trading_system.agents.data_agents.social_media_agent import SocialMediaAgent
from src.trading_system.agents.data_agents.fundamentals_agent import FundamentalsAgent
from src.trading_system.agents.data_agents.news_agent import NewsAgent
from src.trading_system.agents.data_agents.market_agent import MarketAgent
from src.trading_system.agents.trader_agent import TraderAgent
from src.trading_system.agents.risk_management_agent import RiskManagementAgent, RiskProfile
from src.trading_system.agents.manager_agent import ManagerAgent
from src.trading_system.utils.llm.llm_manager import LLMManager
import json
import sys

class Orchestrator:
    def __init__(self, risk_profile: RiskProfile = RiskProfile.NEUTRAL):
        # Initialize all data agents
        self.social_agent = SocialMediaAgent()
        self.fundamentals_agent = FundamentalsAgent()
        self.news_agent = NewsAgent()
        self.market_agent = MarketAgent()
        
        # Initialize decision making agents
        self.trader_agent = TraderAgent()
        self.risk_agent = RiskManagementAgent(risk_profile=risk_profile)
        self.manager_agent = ManagerAgent()
        
        self.llm_manager = LLMManager()
        self.portfolio_state = {"available_capital": 1000000}  # Initialize with basic portfolio state

    def process(self, stock_symbol: str) -> dict:
        """
        Process the input data through all agents and coordinate their responses.
        
        Args:
            stock_symbol (str): The stock symbol to analyze
            
        Returns:
            dict: Dictionary containing all processed data and final recommendation
        """
        print(f"[Orchestrator] Starting analysis for {stock_symbol}...")
        
        try:
            # Step 1: Gather market data from all data agents
            data_results = self._gather_market_data(stock_symbol)
            if "error" in data_results:
                return data_results
            
            # Step 2: Generate trading proposal from trader
            trading_proposal = self.trader_agent.process(data_results)
            if "error" in trading_proposal:
                return trading_proposal
            
            # Step 3: Risk assessment
            risk_assessment = self.risk_agent.process(
                trading_proposal,
                data_results.get("market", {})
            )
            if "error" in risk_assessment:
                return risk_assessment
            
            # Step 4: Final decision from manager
            final_decision = self.manager_agent.process(
                trading_proposal,
                risk_assessment,
                self.portfolio_state
            )
            
            # Combine all results
            results = {
                "data_analysis": data_results,
                "trading_proposal": trading_proposal,
                "risk_assessment": risk_assessment,
                "final_decision": final_decision
            }
            
            print(f"[Orchestrator] Successfully processed all data for {stock_symbol}")
            return results
            
        except Exception as e:
            error_msg = f"Error in orchestration process: {str(e)}"
            print(f"[Orchestrator] {error_msg}")
            return {"error": error_msg}
    
    def _gather_market_data(self, stock_symbol: str) -> dict:
        """Gather and combine data from all data agents."""
        try:
            social_result = json.loads(self.social_agent.process(stock_symbol))
            fundamentals_result = json.loads(self.fundamentals_agent.process(stock_symbol))
            news_result = json.loads(self.news_agent.process(stock_symbol))
            market_result = json.loads(self.market_agent.process(stock_symbol))
            
            # Check for errors in agent results
            errors = []
            if "error" in social_result:
                errors.append(f"Social Media: {social_result['error']}")
            if "error" in fundamentals_result:
                errors.append(f"Fundamentals: {fundamentals_result['error']}")
            if "error" in news_result:
                errors.append(f"News: {news_result['error']}")
            if "error" in market_result:
                errors.append(f"Market: {market_result['error']}")
            
            if errors:
                return {
                    "error": "One or more agents encountered errors:",
                    "details": errors
                }
            
            # Combine all data
            return {
                "social": social_result,
                "fundamentals": fundamentals_result,
                "news": news_result,
                "market": market_result
            }
            
        except Exception as e:
            return {"error": f"Error gathering market data: {str(e)}"}
    
    def update_portfolio_state(self, new_state: dict):
        """Update the portfolio state with new information."""
        self.portfolio_state.update(new_state)
        
    def set_risk_profile(self, risk_profile: RiskProfile):
        """Update the risk profile for the trading system."""
        self.risk_agent = RiskManagementAgent(risk_profile=risk_profile)
    
    def _analyze_social_sentiment(self, social_data: dict) -> str:
        """
        Analyze sentiment from social media data.
        In a real implementation, this would use NLP to analyze the sentiment.
        """
        # Exemple simplifié : si plus de 60% des posts ont un score positif
        positive_posts = sum(1 for post in social_data if post.get("score", 0) > 0)
        total_posts = len(social_data)
        if total_posts > 0 and (positive_posts / total_posts) > 0.6:
            return "positive"
        return "neutral"
    
    def _analyze_news_sentiment(self, news_data: dict) -> str:
        """
        Analyze sentiment from news data.
        In a real implementation, this would use NLP to analyze the sentiment.
        """
        # Exemple simplifié : si plus de 60% des articles ont un titre négatif
        negative_articles = sum(1 for article in news_data if any(word in article.get("headline", "").lower() 
                            for word in ["down", "fall", "drop", "decline", "loss"]))
        total_articles = len(news_data)
        if total_articles > 0 and (negative_articles / total_articles) > 0.6:
            return "negative"
        return "neutral"
