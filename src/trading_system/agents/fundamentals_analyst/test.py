"""
Test module for the FundamentalsAnalyst agent.
This module provides a function that returns predetermined data for testing purposes.
"""

import json

def get_mock_fundamentals_data():
    """
    Returns a predetermined JSON string containing mock fundamentals data.
    
    Returns:
        str: A JSON string containing mock fundamentals data
    """
    mock_data = {
        "company_info": {
            "name": "Apple Inc.",
            "symbol": "AAPL",
            "sector": "Technology",
            "industry": "Consumer Electronics",
            "description": "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide. The company offers iPhone, iPad, Mac, Apple Watch, and AirPods. It also provides Apple TV+, Apple Music, Apple Arcade, Apple Fitness+, Apple News+, Apple Pay, Apple Card, and Apple Books.",
            "website": "https://www.apple.com",
            "ceo": "Tim Cook",
            "employees": 164000,
            "headquarters": "Cupertino, California"
        },
        "fundamentals_data": {
            "current_price": 175.84,
            "market_cap": 2760000000000,
            "pe_ratio": 28.5,
            "eps": 6.15,
            "dividend_yield": 0.52,
            "beta": 1.28,
            "52_week_high": 198.23,
            "52_week_low": 124.17,
            "avg_volume": 52800000,
            "revenue": 394328000000,
            "profit_margin": 0.25,
            "operating_margin": 0.30,
            "return_on_equity": 0.17,
            "return_on_assets": 0.15,
            "debt_to_equity": 1.56,
            "current_ratio": 0.88,
            "quick_ratio": 0.82,
            "book_value": 3.47,
            "cash_per_share": 4.23,
            "revenue_growth": 0.08,
            "earnings_growth": 0.05
        }
    }
    
    return json.dumps(mock_data, indent=4)

def get_mock_analysis():
    """
    Returns a predetermined analysis of the fundamentals data.
    
    Returns:
        str: A string containing the analysis
    """
    return """
    Fundamentals Analysis for AAPL:
    
    Company Overview:
    Apple Inc. (AAPL) is a technology company that designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide. The company is headquartered in Cupertino, California, and is led by CEO Tim Cook.
    
    Key Financial Metrics:
    - Current Price: $175.84
    - Market Cap: $2.76T
    - P/E Ratio: 28.5
    - EPS: $6.15
    - Dividend Yield: 0.52%
    
    Financial Health:
    - Revenue: $394.3B
    - Profit Margin: 25%
    - Operating Margin: 30%
    - Return on Equity: 17%
    - Return on Assets: 15%
    
    Growth Metrics:
    - Revenue Growth: 8%
    - Earnings Growth: 5%
    
    Valuation Metrics:
    - Book Value: $3.47
    - Cash per Share: $4.23
    - Debt to Equity: 1.56
    
    Analysis:
    Apple demonstrates strong financial health with robust profit margins and solid returns on equity and assets. The company's revenue and earnings growth, while positive, have moderated compared to previous years, which is expected for a company of its size and maturity.
    
    The P/E ratio of 28.5 suggests the stock is trading at a premium compared to the broader market, reflecting investors' confidence in Apple's brand strength, ecosystem, and cash generation capabilities. The company's substantial cash position provides flexibility for continued innovation, acquisitions, and shareholder returns through dividends and buybacks.
    
    Apple's transition toward services revenue is progressing well, providing a more stable and recurring revenue stream. This diversification helps reduce reliance on hardware sales cycles and should support more consistent growth in the future.
    
    Overall, Apple's fundamentals remain strong, with a solid balance sheet, healthy margins, and a clear strategy for growth through both hardware and services.
    """

def test_fundamentals_analyst(stock_symbol: str) -> dict:
    """
    Test function that simulates the FundamentalsAnalyst's invoke method.
    
    Args:
        stock_symbol (str): The stock symbol to analyze (not used in mock data)
        
    Returns:
        dict: A dictionary containing mock fundamentals data and analysis
    """
    print(f"[FundamentalsAnalyst] Starting mock fundamentals data fetch for {stock_symbol}")
    
    # Get mock data
    fundamentals_data = get_mock_fundamentals_data()
    print(f"[FundamentalsAnalyst] Successfully fetched mock fundamentals data for {stock_symbol}")
    
    # Get mock analysis
    analysis = get_mock_analysis()
    print("[FundamentalsAnalyst] Generated mock analysis")
    
    return {
        "fundamentals_data": fundamentals_data,
        "company_info": json.loads(fundamentals_data)["company_info"],
        "analysis": analysis
    }

# Example usage
if __name__ == "__main__":
    result = test_fundamentals_analyst("AAPL")
    print("\n=== Mock Fundamentals Data ===")
    print(result["fundamentals_data"])
    print("\n=== Mock Analysis ===")
    print(result["analysis"]) 