class RiskAgent:
    def check(self, order, portfolio, market_data):
        """
        Retourne (is_valid, adjusted_order, reason)
        """
        raise NotImplementedError