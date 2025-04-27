from trading_system.agents.market_analyst.get_market_data import GetMarketData
from trading_system.agents.risk_team.riskAgent import RiskAgent


class AgentRiskCompliance(RiskAgent):
    """
    Applique des règles globales de portefeuille :
    - % max par actif
    - % max dans une même classe d'actifs ou un même secteur
    - Levier / marge max
    """
    def __init__(self, max_asset_pct=0.10, max_sector_pct=None, max_leverage=2.0):
        self.max_asset_pct = max_asset_pct
        self.max_sector_pct = max_sector_pct or {}
        self.max_leverage = max_leverage

    def check(self, order, portfolio, market_data):

        market_data = GetMarketData(market_data)
        
        try:
            total_value = portfolio["total_value"]
            cash = portfolio.get("cash", 0)

            # 1) Nouvelle exposition sur l'actif
            asset = order["asset"]
            current_price = market_data.get_price(asset)
            order_value = order.get("notional_amount", current_price * order.get("quantity", 0))

            current_asset_value = portfolio["invested_assets"].get(asset, 0)
            new_asset_pct = (current_asset_value + order_value) / total_value
            if new_asset_pct > self.max_asset_pct:
                return (False, order,
                        f"Nouvelle exposition {new_asset_pct:.2%} > {self.max_asset_pct:.2%} max actif")

            # 2) Exposition par secteur
            sector = market_data.get_sector(asset)
            if sector in self.max_sector_pct:
                current_sector_value = portfolio["invested_sectors"].get(sector, 0)
                new_sector_pct = (current_sector_value + order_value) / total_value
                limit = self.max_sector_pct[sector]
                if new_sector_pct > limit:
                    return (False, order,
                            f"Exposition secteur {sector} de {new_sector_pct:.2%} > {limit:.2%} max")

            # 3) Vérifier le levier
            total_invested = portfolio.get("invested_value", 0)
            current_leverage = (total_invested + order_value) / total_value
            if current_leverage > self.max_leverage:
                return (False, order,
                        f"Levier actuel {current_leverage:.2f}x > {self.max_leverage:.2f}x max")

            return (True, order, "Compliance rules OK")

        except Exception as e:
            return (False, order, f"Erreur dans Compliance check: {str(e)}")

