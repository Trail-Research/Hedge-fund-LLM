from trading_system.agents.risk_team.riskAgent import RiskAgent


class AgentRiskStopLoss(RiskAgent):
    def __init__(self, default_stop_loss_percent=0.05):
        self.default_stop_loss_percent = default_stop_loss_percent

    def check(self, order, portfolio, market_data):
        if "stop_loss" not in order or order["stop_loss"] is None:
            # On va chercher le "current_price" dans market_data
            try:
                price = market_data["price_data"]["current_price"]
            except (KeyError, TypeError):
                return (False, order, "Market data missing 'current_price'")
            
            stop_loss_price = price * (1 - self.default_stop_loss_percent)
            order["stop_loss"] = round(stop_loss_price, 2)  # Arrondi joli

            return (True, order, "Stop-loss automatically added")
        
        # Si le stop loss existe déjà, on vérifie qu’il est cohérent
        current_price = market_data["price_data"]["current_price"]
        if order["stop_loss"] > current_price:
            return (False, order, "Invalid stop-loss: above current price")

        return (True, order, "OK")