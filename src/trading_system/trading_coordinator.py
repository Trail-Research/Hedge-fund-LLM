from agents.fundamental_analyst.main import FundamentalAnalyst
from agents.sentiment_analyst.main import SentimentAnalyst
from agents.news_analyst.main import NewsAnalyst
from agents.market_analyst.main import MarketAnalyst
from agents.trading_analyst.main import TradingAnalyst

class TradingCoordinator:
    def __init__(self):
        self.fundamental_analyst = FundamentalAnalyst()
        self.sentiment_analyst = SentimentAnalyst()
        self.news_analyst = NewsAnalyst()
        self.market_analyst = MarketAnalyst()
        self.trading_analyst = TradingAnalyst()
    
    def analyze_all(self, stock_symbol: str) -> dict:
        # Collect all analyses and raw data
        fundamentals_result = self.fundamental_analyst.invoke(stock_symbol)
        sentiment_result = self.sentiment_analyst.invoke(stock_symbol)
        news_result = self.news_analyst.invoke(stock_symbol)
        market_result = self.market_analyst.invoke(stock_symbol)
        
        analyses = {
            'fundamentals': fundamentals_result['analysis'],
            'social': sentiment_result['analysis'],
            'news': news_result['analysis'],
            'market': market_result['analysis'],
            
            # Store all raw data
            'raw_data': {
                'fundamentals': {
                    'fundamentals_data': fundamentals_result['fundamentals_data'],
                    'company_info': fundamentals_result['company_info']
                },
                'social': sentiment_result['social_data'],
                'news': news_result['news_data'],
                'market': market_result['market_data']
            }
        }
        
        # Generate final recommendation
        recommendation = self.trading_analyst.invoke(analyses)
        analyses['recommendation'] = recommendation
        
        return analyses 