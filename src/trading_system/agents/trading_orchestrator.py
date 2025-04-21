from .fundamentals_analyst.main import FundamentalsAnalyst
from .news_analyst.main import NewsAnalyst
from .market_analyst.main import MarketAnalyst
from .trading_analyst.main import TradingAnalyst
from .social_media_analyst.main import SocialMediaAnalyst
from .news_analyst.main import NewsAnalyst
import json
import time

class TradingOrchestrator:
    def __init__(self):
        # Initialize all analysts
        self.fundamental_analyst = FundamentalsAnalyst()
        self.news_analyst = NewsAnalyst()
        self.market_analyst = MarketAnalyst()
        self.trading_analyst = TradingAnalyst()
        
        # Initialize sentiment analyzers
        self.social_media_analyzer = SocialMediaAnalyst()
        self.news_analyzer = NewsAnalyst()

    def analyze_stock(self, stock_symbol: str) -> dict:
        """
        Coordinate the analysis of a stock using all available analysts
        
        Args:
            stock_symbol (str): The stock symbol to analyze
            
        Returns:
            dict: Complete analysis including raw data and recommendations
        """
        try:
            print(f"\n[TradingOrchestrator] Starting analysis for {stock_symbol}")
            
            # Collect all analyses and raw data
            print("[TradingOrchestrator] Fetching fundamentals data...")
            fundamentals_result = self.fundamental_analyst.invoke(stock_symbol)
            print("[TradingOrchestrator] Fundamentals data fetched successfully")
            
            print("[TradingOrchestrator] Fetching social media data...")
            social_results = self.social_media_analyzer.invoke(stock_symbol)
            print("[TradingOrchestrator] Social media data fetched successfully")
            
            print("[TradingOrchestrator] Fetching news data...")
            news_result = self.news_analyst.invoke(stock_symbol)
            print("[TradingOrchestrator] News data fetched successfully")
            
            print("[TradingOrchestrator] Fetching market data...")
            market_result = self.market_analyst.invoke(stock_symbol)

            # Additional sentiment analysis
            # social_sentiment = self.social_media_analyzer.analyze_sentiment(social_reculs['social_data'])
            # news_sentiment = self.news_analyzer.analyze_sentiment(news_result['news_data'])
            print("[TradingOrchestrator] Market data fetched successfully")
            
            analyses = {
                'fundamentals': fundamentals_result['analysis'],
                'social': {
                    'analysis': social_results['analysis'],
                    # 'sentiment_score': social_sentiment
                },
                'news': {
                    'analysis': news_result['analysis'],
                    # 'sentiment_score': news_sentiment
                },
                'market': market_result['analysis'],
                
                # Store all raw data
                'raw_data': {
                    'fundamentals': {
                        'fundamentals_data': fundamentals_result['fundamentals_data'],
                        'company_info': fundamentals_result['company_info']
                    },
                    'social': social_results['social_data'],
                    'news': news_result['news_data'],
                    'market': market_result['market_data']
                }
            }

            print("[TradingOrchestrator] Generating final recommendation...")
            recommendation = self.trading_analyst.invoke(analyses)
            analyses['recommendation'] = recommendation
            print("[TradingOrchestrator] Analysis completed successfully")

            return analyses

        except Exception as e:
            error_msg = f"Error processing data for {stock_symbol}: {str(e)}"
            print(f"[TradingOrchestrator] {error_msg}")
            print(f"[TradingOrchestrator] Error type: {type(e).__name__}")
            print(f"[TradingOrchestrator] Error details: {str(e)}")
            return {"error": error_msg} 