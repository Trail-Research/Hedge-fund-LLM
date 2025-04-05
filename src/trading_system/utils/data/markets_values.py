import yfinance as yf
import json

def get_market_data(ticker: str, period: str = "5d") -> str:
    """
    Retrieves historical data for a ticker using yfinance and converts it to JSON.
    
    Args:
        ticker (str): The stock symbol (e.g., 'AAPL')
        period (str): The time period (e.g., '5d', '1mo', '1y'...)
        
    Returns:
        str: A formatted JSON string containing market data
    """
    stock = yf.Ticker(ticker)

    # Get company information
    info = stock.info
    history = stock.history(period=period)

    # Convert DataFrame to JSON dictionary list
    json_data = []
    for date, row in history.iterrows():
        json_data.append({
            "date": date.strftime('%Y-%m-%d'),
            "open": round(row["Open"], 2),
            "high": round(row["High"], 2),
            "low": round(row["Low"], 2),
            "close": round(row["Close"], 2),
            "volume": int(row["Volume"])
        })

    # Create final dictionary containing historical data and company info
    final_result = {
        "history": json_data,
        "info": info
    }

    # Convert to formatted JSON string
    return json.dumps(final_result, indent=4)

# Example usage
if __name__ == "__main__":
    json_result = get_market_data("AAPL", "5d")
    print(json_result)
