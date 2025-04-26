from trading_system.agents.risk_team.riskAgent import RiskAgent


class AgentRiskExposure(RiskAgent):
    def __init__(self, max_exposure_per_asset=0.1):
        self.max_exposure_per_asset = max_exposure_per_asset  # 10% du capital max par actif

    def check(self, order, portfolio, market_data):
        asset_value = market_data.get_price(order["asset"]) * order["quantity"]
        total_capital = portfolio["total_value"]
        current_exposure = portfolio.get_exposure(order["asset"])

        if (current_exposure + asset_value) / total_capital > self.max_exposure_per_asset:
            return (False, order, f"Exceeds exposure limit for {order['asset']}")
        
        return (True, order, "OK")