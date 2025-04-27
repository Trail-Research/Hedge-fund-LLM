from trading_system.agents.market_analyst.get_market_data import GetMarketData
from trading_system.agents.risk_team.riskAgent import RiskAgent


class AgentRiskExposure(RiskAgent):
    def __init__(self, max_exposure_per_asset=0.1):
        self.max_exposure_per_asset = max_exposure_per_asset  # 10% du capital max par actif

    def check(self, order, portfolio, market_data):

        market_data = GetMarketData(market_data)
        
        try:
            # Récupère la valeur actuelle de l'actif via MockMarketData
            current_price = market_data.get_price(order["asset"])
            asset_value = order.get("notional_amount", current_price * order.get("quantity", 0))
            
            total_capital = portfolio["total_value"]
            current_exposure = portfolio["invested_assets"].get(order["asset"], 0)

            new_exposure_pct = (current_exposure + asset_value) / total_capital

            if new_exposure_pct > self.max_exposure_per_asset:
                return (
                    False,
                    order,
                    f"Exceeds exposure limit for {order['asset']} ({new_exposure_pct:.2%} > {self.max_exposure_per_asset:.2%})"
                )
            
            return (True, order, "Exposure OK")
        
        except Exception as e:
            return (False, order, f"Erreur dans Exposure check: {str(e)}")