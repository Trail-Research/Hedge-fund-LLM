from trading_system.agents.market_analyst.get_market_data import GetMarketData
from trading_system.agents.risk_team.riskAgent import RiskAgent


class AgentRiskMarketConditions(RiskAgent):
    """
    Vérifie que les conditions de marché sont acceptables avant d'ouvrir une position :
    - Volatilité intraday sous un seuil max
    - Spread (ask-bid) sous un seuil max
    """
    def __init__(self, max_volatility=0.02, max_spread=0.0005):
        self.max_volatility = max_volatility
        self.max_spread = max_spread

    def check(self, order, portfolio, market_data):

        market_data = GetMarketData(market_data)
        
        try:
            asset = order["asset"]

            # ➔ Utilise la méthode de MockMarketData pour récupérer l'historique
            prices = market_data.get_historical_data(asset, period="1w")
            if len(prices) < 2:
                return (False, order, "Pas assez d'historique pour calculer la volatilité")
            
            mean_price = sum(prices) / len(prices)
            variance = sum((p - mean_price) ** 2 for p in prices) / (len(prices) - 1)
            volatility = (variance ** 0.5) / mean_price

            # ➔ Utilise MockMarketData pour ask/bid
            ask = market_data.get_ask(asset)
            bid = market_data.get_bid(asset)
            spread = ask - bid
            mid_price = (ask + bid) / 2
            spread_pct = spread / mid_price

            # Checks
            if volatility > self.max_volatility:
                return (False, order, f"Volatilité trop élevée ({volatility:.2%} > {self.max_volatility:.2%})")
            
            if spread_pct > self.max_spread:
                return (False, order, f"Spread trop large ({spread_pct:.2%} > {self.max_spread:.2%})")

            return (True, order, "Market conditions OK")

        except Exception as e:
            return (False, order, f"Erreur dans MarketConditions check: {str(e)}")