from .fundamentals_analyst.main import FundamentalsAnalyst
from .market_analyst.main import MarketAnalyst
from .trading_analyst.main import TradingAnalyst
from .social_media_analyst.main import SocialMediaAnalyst
from .news_analyst.main import NewsAnalyst

from .fundamentals_analyst.test import test_fundamentals_analyst
from .news_analyst.test import test_news_analyst
from .market_analyst.test import test_market_analyst
from .trading_analyst.test import test_trading_analyst
from .social_media_analyst.test import test_social_media_analyst

from .risk_team.pipeline import risk_management_pipeline

import json
import time

class TradingOrchestrator:
    def __init__(self, use_test_data=None, portfolio=None):
        """
        Initialize the TradingOrchestrator
        
        Args:
            use_test_data (dict, optional): Dictionary specifying which components to use test data for.
                Keys can be: 'fundamentals', 'social', 'news', 'market', 'trading'
                Values should be boolean (True to use test data, False to use real API)
                Example: {'fundamentals': True, 'social': False, 'news': True, 'market': False, 'trading': False}
        """
        # Default to using real API for all components if not specified
        self.use_test_data = use_test_data or {
            'fundamentals': True,
            'social': True,
            'news': True,
            'market': True,
            'trading': True
        }
        
        # Initialize all analysts (only used when not using test data)
        self.fundamental_analyst = FundamentalsAnalyst()
        self.market_analyst = MarketAnalyst()
        self.trading_analyst = TradingAnalyst()
        self.news_analyst = NewsAnalyst()
        self.social_media_analyzer = SocialMediaAnalyst()

        # Portfolio = état courant du compte (valeur totale, exposures, levier…)
        self.portfolio = portfolio or self._load_initial_portfolio()

    def _load_initial_portfolio(self):
        # TODO: charger le portefeuille depuis une base ou API
        return {
            "total_value": 100_000.0,      # Valeur totale du portefeuille
            "cash": 50_000.0,              # Liquidités disponibles
            "invested_value": 50_000.0,    # Déjà investi sur AAPL et MSFT
            "invested_assets": {
                "AAPL": 30_000.0,          # 30k$ sur Apple
                "MSFT": 20_000.0,          # 20k$ sur Microsoft
            },
            "invested_sectors": {
                "equities": 50_000.0,      # Tout est en actions
            },
            "get_exposure": lambda asset: (
                30_000.0 if asset == "AAPL" else
                20_000.0 if asset == "MSFT" else
                0.0
            ) / 100_000.0,   # Exposition d'un actif par rapport au total

            "get_sector_exposure": lambda sector: (
                50_000.0 if sector == "equities" else
                0.0
            ) / 100_000.0,   # Exposition du secteur actions

            "get_total_notional": lambda: 50_000.0,  # Montant investi total
        }

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
            if self.use_test_data.get('fundamentals', False):
                print("[TradingOrchestrator] Using test data for fundamentals analysis")
                fundamentals_result = test_fundamentals_analyst(stock_symbol)
            else:
                fundamentals_result = self.fundamental_analyst.invoke(stock_symbol)
            print("[TradingOrchestrator] Fundamentals data fetched successfully")
            
            print("[TradingOrchestrator] Fetching social media data...")
            if self.use_test_data.get('social', False):
                print("[TradingOrchestrator] Using test data for social media analysis")
                social_results = test_social_media_analyst(stock_symbol)
            else:
                social_results = self.social_media_analyzer.invoke(stock_symbol)
            print("[TradingOrchestrator] Social media data fetched successfully")
            
            print("[TradingOrchestrator] Fetching news data...")
            if self.use_test_data.get('news', False):
                print("[TradingOrchestrator] Using test data for news analysis")
                news_result = test_news_analyst(stock_symbol)
            else:
                news_result = self.news_analyst.invoke(stock_symbol)
            print("[TradingOrchestrator] News data fetched successfully")
            
            print("[TradingOrchestrator] Fetching market data...")
            if self.use_test_data.get('market', False):
                print("[TradingOrchestrator] Using test data for market analysis")
                market_result = test_market_analyst(stock_symbol)
            else:
                market_result = self.market_analyst.invoke(stock_symbol)
            print("[TradingOrchestrator] Market data fetched successfully")
            
            analyses = {
                'fundamentals': fundamentals_result['analysis'],
                'social': {
                    'analysis': social_results['analysis'],
                },
                'news': {
                    'analysis': news_result['analysis'],
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
            if self.use_test_data.get('trading', False):
                print("[TradingOrchestrator] Using test data for trading recommendation")
                recommendation = test_trading_analyst(analyses)
            else:
                recommendation = self.trading_analyst.invoke(analyses)
            analyses['recommendation'] = recommendation
            print("[TradingOrchestrator] Analysis completed successfully")

            # --- Intégration Risk Management ---
            order = recommendation.get("order")
            if order:
                print("[TradingOrchestrator] Running risk management checks...")
                validated_order = risk_management_pipeline(
                    order,
                    self.portfolio,
                    market_result["market_data"]
                )
                if validated_order is None:
                    analyses['recommendation']['status'] = 'rejected_by_risk'
                else:
                    analyses['recommendation']['order'] = validated_order
                    analyses['recommendation']['status'] = 'approved_by_risk'
            else:
                print("[TradingOrchestrator] No order to validate.")

            return analyses

        except Exception as e:
            error_msg = f"Error processing data for {stock_symbol}: {str(e)}"
            print(f"[TradingOrchestrator] {error_msg}")
            print(f"[TradingOrchestrator] Error type: {type(e).__name__}")
            print(f"[TradingOrchestrator] Error details: {str(e)}")
            return {"error": error_msg} 