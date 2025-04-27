from trading_system.agents.market_analyst.get_market_data import GetMarketData
from trading_system.agents.risk_team.riskAgent import RiskAgent


class AgentRiskStopLoss(RiskAgent):
    def __init__(self, default_stop_loss_percent=0.05):
        self.default_stop_loss_percent = default_stop_loss_percent

    def check(self, order, portfolio, market_data):

        market_data = GetMarketData(market_data)
        
        try:
            current_price = market_data.get_price(order["asset"])
            
            if "stop_loss" not in order or order["stop_loss"] is None:
                stop_loss_price = current_price * (1 - self.default_stop_loss_percent)
                order["stop_loss"] = round(stop_loss_price, 2)  # Arrondi joli
                return (True, order, "Stop-loss automatically added")
            
            # Si le stop loss existe déjà, on vérifie qu’il est cohérent
            if order["stop_loss"] > current_price:
                return (False, order, "Invalid stop-loss: above current price")

            return (True, order, "OK")

        except Exception as e:
            return (False, order, f"Erreur dans StopLoss check: {str(e)}")