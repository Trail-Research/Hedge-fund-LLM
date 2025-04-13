from ..fundamental_analyst.main import FundamentalAnalyst
from ..sentiment_analyst.main import SentimentAnalyst
from ..news_analyst.main import NewsAnalyst
from ..market_analyst.main import MarketAnalyst
from ..trading_analyst.main import TradingAnalyst
from ..sentiment_analyst.sentiment_analyzer import RedditSentimentAnalyzer
from ..news_analyst.sentiment_analyzer import NewsSentimentAnalyzer
import json

class TradingOrchestrator:
    def __init__(self):
        # Initialize all analysts
        self.fundamental_analyst = FundamentalAnalyst()
        self.sentiment_analyst = SentimentAnalyst()
        self.news_analyst = NewsAnalyst()
        self.market_analyst = MarketAnalyst()
        self.trading_analyst = TradingAnalyst()
        
        # Initialize sentiment analyzers
        self.reddit_analyzer = RedditSentimentAnalyzer()
        self.news_analyzer = NewsSentimentAnalyzer()

    def analyze_stock(self, stock_symbol: str) -> dict:
        """
        Coordinate the analysis of a stock using all available analysts
        
        Args:
            stock_symbol (str): The stock symbol to analyze
            
        Returns:
            dict: Complete analysis including raw data and recommendations
        """
        try:
            # Collect all analyses and raw data
            fundamentals_result = self.fundamental_analyst.invoke(stock_symbol)
            sentiment_result = self.sentiment_analyst.invoke(stock_symbol)
            news_result = self.news_analyst.invoke(stock_symbol)
            market_result = self.market_analyst.invoke(stock_symbol)

            # Additional sentiment analysis
            social_sentiment = self.reddit_analyzer.analyze_sentiment(sentiment_result['social_data'])
            news_sentiment = self.news_analyzer.analyze_sentiment(news_result['news_data'])

            analyses = {
                'fundamentals': fundamentals_result['analysis'],
                'social': {
                    'analysis': sentiment_result['analysis'],
                    'sentiment_score': social_sentiment
                },
                'news': {
                    'analysis': news_result['analysis'],
                    'sentiment_score': news_sentiment
                },
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

        except Exception as e:
            error_msg = f"Error processing data for {stock_symbol}: {str(e)}"
            print(f"[TradingOrchestrator] {error_msg}")
            return {"error": error_msg} 