"""
Test module for the TradingAnalyst agent.
This module provides a function that returns predetermined data for testing purposes.
"""

def get_mock_recommendation():
    """
    Returns a predetermined trading recommendation.
    
    Returns:
        str: A string containing the trading recommendation
    """

    recommendation = """
    Trading Recommendation for AAPL:
    
    Overall Recommendation: BUY
    
    Summary:
    Based on comprehensive analysis of fundamentals, market data, news sentiment, and social media sentiment, AAPL presents a favorable investment opportunity with a BUY recommendation. The company demonstrates strong financial health, positive market sentiment, and favorable news coverage, outweighing minor concerns about supply chain risks.
    
    Key Strengths:
    1. Strong Financial Fundamentals
       - Robust profit margins (25%) and operating margins (30%)
       - Solid revenue and earnings growth
       - Strong cash position and shareholder returns through buybacks
    
    2. Positive Market Sentiment
       - Bullish technical indicators with stock trading above key moving averages
       - Strong analyst ratings with 25 "Buy" recommendations vs. only 3 "Sell"
       - Average price target of $185.67 represents 5.6% upside
    
    3. Favorable News and Social Media Sentiment
       - Positive earnings results and strategic initiatives
       - Strong community confidence in ecosystem and services growth
       - Dominant positive narrative in social media discussions
    
    Risk Factors:
    1. Supply Chain Concerns
       - Production delays reported in China
       - Geopolitical tensions affecting manufacturing
       - Diversification efforts may increase costs in near term
    
    2. Valuation Considerations
       - P/E ratio of 28.5 is above historical averages
       - Stock approaching potential resistance levels
       - Limited short-term upside to price targets
    
    Investment Strategy:
    - Entry Point: Current price of $175.84 is reasonable for a long-term position
    - Position Size: Consider a moderate position (3-5% of portfolio)
    - Time Horizon: Medium to long-term (6-12 months)
    - Stop Loss: Set at $169.78 (50-day SMA) to protect against technical breakdown
    
    Alternative Scenarios:
    - Bullish Case: Stock reaches $185-190 range based on continued momentum and positive earnings
    - Bearish Case: Stock pulls back to $165-170 range if market sentiment shifts or supply chain issues worsen
    
    Conclusion:
    AAPL represents a solid BUY opportunity for investors with a medium to long-term horizon. The company's strong fundamentals, positive sentiment across multiple data sources, and strategic initiatives position it well for continued success. While there are some risks to monitor, particularly around supply chain and valuation, the overall investment thesis remains compelling. Investors should consider dollar-cost averaging into the position to mitigate short-term volatility risks.
    """

    order = {
        "asset": "AAPL",
        "action": "BUY",
        "notional_amount": 3000,        # 3% d'un portefeuille de 100k$
        "entry_price": 175.84,
        "stop_loss": 169.78,
        "target_price": 185.67,
        "time_horizon_days": 180
    }

    return {
        "recommendation": recommendation,
        "order": order
    }

def test_trading_analyst(analyses: dict) -> str:
    """
    Test function that simulates the TradingAnalyst's invoke method.
    
    Args:
        analyses (dict): Dictionary containing analyses from other analysts (not used in mock data)
        
    Returns:
        str: A string containing the trading recommendation
    """
    print("[TradingAnalyst] Generating mock trading recommendation")
    
    # Get mock recommendation
    recommendation = get_mock_recommendation()
    print("[TradingAnalyst] Generated mock trading recommendation")
    
    return recommendation

# Example usage
if __name__ == "__main__":
    # Create a mock analyses dictionary
    mock_analyses = {
        "fundamentals": {"analysis": "Mock fundamentals analysis"},
        "social": {"analysis": "Mock social media analysis"},
        "news": {"analysis": "Mock news analysis"},
        "market": "Mock market analysis"
    }
    
    recommendation = test_trading_analyst(mock_analyses)
    print("\n=== Mock Trading Recommendation ===")
    print(recommendation) 