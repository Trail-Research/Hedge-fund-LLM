from trading_system.agents.risk_team.riskAgent import RiskAgent


class AgentRiskStopLoss(RiskAgent):
    def __init__(self, default_stop_loss_percent=0.05):
        self.default_stop_loss_percent = default_stop_loss_percent

    def check(self, order, portfolio, market_data):
        if "stop_loss" not in order:
            price = market_data.get_price(order["asset"])
            stop_loss_price = price * (1 - self.default_stop_loss_percent)
            order["stop_loss"] = stop_loss_price
            return (True, order, "Stop-loss added")
        return (True, order, "OK")