class GetMarketData:
    def __init__(self, data):
        self.data = data

    def get_price(self, asset):
        return self.data["price_data"]["current_price"]

    def get_bid(self, asset):
        return self.data["price_data"]["bid"]

    def get_ask(self, asset):
        return self.data["price_data"]["ask"]

    def get_sector(self, asset):
        return self.data["market_sentiment"]["sector"]

    def get_volatility(self, asset, period="1m"):
        vol_key = f"historical_volatility_{period}"
        return self.data["volatility_data"].get(vol_key, 0.02)  # 2% défaut si pas trouvé

    def get_historical_data(self, asset, period="1m"):
        return self.data["historical_data"].get(period, [])

    def get_technical_indicator(self, indicator_name):
        return self.data["technical_indicators"].get(indicator_name)

    def get_market_sentiment(self):
        return self.data["market_sentiment"]

    def get_price_target(self):
        return self.data["market_sentiment"]["price_targets"]