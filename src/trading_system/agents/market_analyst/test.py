"""
Test module for the MarketAnalyst agent.
This module provides a function that returns predetermined data for testing purposes.
"""

import json

def get_mock_market_data():
    """
    Returns a predetermined dictionary containing mock market data.
    
    Returns:
        dict: A dictionary containing mock market data
    """
    mock_data = {
        "price_data": {
            "current_price": 175.84,
            "previous_close": 174.79,
            "open": 175.12,
            "day_high": 176.23,
            "day_low": 174.56,
            "volume": 52800000,
            "avg_volume": 52800000,
            "market_cap": 2760000000000,
            "pe_ratio": 28.5,
            "eps": 6.15,
            "dividend_yield": 0.52,
            "beta": 1.28,
            "bid": 175.75,       # Ajouté: Bid price
            "ask": 175.90        # Ajouté: Ask price (spread très serré)
        },
        "historical_data": {
            "1d": [174.79, 175.12, 175.45, 175.67, 175.84],
            "1w": [173.25, 174.12, 174.89, 175.23, 175.84],
            "1m": [169.34, 171.56, 173.78, 174.92, 175.84],
            "3m": [162.34, 165.67, 169.89, 173.45, 175.84],
            "6m": [145.67, 152.34, 159.78, 167.89, 175.84],
            "1y": [124.17, 135.67, 147.89, 159.34, 175.84]
        },
        "technical_indicators": {
            "sma_20": 173.45,
            "sma_50": 169.78,
            "sma_200": 155.67,
            "ema_12": 175.23,
            "ema_26": 173.89,
            "macd": 1.34,
            "macd_signal": 0.89,
            "macd_histogram": 0.45,
            "rsi_14": 58.7,
            "bollinger_upper": 178.34,
            "bollinger_middle": 173.45,
            "bollinger_lower": 168.56
        },
        "market_sentiment": {
            "overall": "bullish",
            "short_term": "neutral",
            "medium_term": "bullish",
            "long_term": "bullish",
            "analyst_ratings": {
                "buy": 25,
                "hold": 12,
                "sell": 3
            },
            "price_targets": {
                "low": 150.00,
                "average": 185.67,
                "high": 210.00
            },
            "sector": "equities"
        },
        "volatility_data": {
            "historical_volatility_1m": 0.015,  # 1.5% volatilité mensuelle
            "historical_volatility_3m": 0.018,  # 1.8% volatilité trimestrielle
            "historical_volatility_6m": 0.020   # 2.0% volatilité semestrielle
        }
    }
    
    return mock_data

def get_mock_analysis():
    """
    Returns a predetermined analysis of the market data.
    
    Returns:
        str: A string containing the analysis
    """
    return """
    Market Analysis for AAPL:
    
    Price Action:
    AAPL is currently trading at $175.84, up 0.60% from the previous close of $174.79. The stock has shown consistent upward momentum over the past month, gaining approximately 3.8% during this period. The current price is near the day's high of $176.23, indicating strong buying pressure.
    
    Technical Indicators:
    - The stock is trading above both the 20-day SMA ($173.45) and 50-day SMA ($169.78), indicating short-term bullish momentum.
    - The MACD is positive at 1.34 with a positive histogram of 0.45, confirming the bullish trend.
    - The RSI at 58.7 is in neutral territory, suggesting the stock is not overbought.
    - The price is within the Bollinger Bands, with the middle band at $173.45, indicating normal volatility.
    
    Market Sentiment:
    Overall market sentiment for AAPL is bullish, with 25 analysts recommending a "Buy" compared to only 3 recommending a "Sell." The average price target of $185.67 represents a potential upside of approximately 5.6% from current levels.
    
    Volume Analysis:
    Trading volume of 52.8 million shares is in line with the average daily volume, suggesting normal trading activity without unusual buying or selling pressure.
    
    Relative Performance:
    AAPL has outperformed the broader market indices over the past 3 months, gaining approximately 8.3% compared to the S&P 500's gain of 5.2% during the same period.
    
    Support and Resistance Levels:
    - Key support levels: $173.45 (20-day SMA), $169.78 (50-day SMA)
    - Key resistance levels: $176.23 (day's high), $178.34 (Bollinger upper band)
    
    Conclusion:
    The technical and sentiment indicators suggest a bullish outlook for AAPL in the medium to long term. The stock is in a clear uptrend, trading above key moving averages with positive momentum indicators. While the RSI indicates the stock is not overbought, investors should be mindful of potential resistance at the day's high and the upper Bollinger Band. The strong analyst sentiment and price targets provide additional confidence in the bullish outlook, though the potential upside of 5.6% to the average price target suggests the stock may be approaching fair value in the short term.
    """

def test_market_analyst(stock_symbol: str) -> dict:
    """
    Test function that simulates the MarketAnalyst's invoke method.
    
    Args:
        stock_symbol (str): The stock symbol to analyze (not used in mock data)
        
    Returns:
        dict: A dictionary containing mock market data and analysis
    """
    print(f"[MarketAnalyst] Starting mock market data fetch for {stock_symbol}")
    
    # Get mock data
    market_data = get_mock_market_data()
    print(f"[MarketAnalyst] Successfully fetched mock market data for {stock_symbol}")
    
    # Get mock analysis
    analysis = get_mock_analysis()
    print("[MarketAnalyst] Generated mock analysis")
    
    return {
        "market_data": market_data,
        "analysis": analysis
    }

# Example usage
if __name__ == "__main__":
    result = test_market_analyst("AAPL")
    print("\n=== Mock Market Data ===")
    print(result["market_data"])
    print("\n=== Mock Analysis ===")
    print(result["analysis"]) 