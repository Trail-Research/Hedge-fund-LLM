import yfinance as yf
import json

def get_market_data(ticker: str, period: str = "5d", interval: str = "1d") -> str:
    """
    Retrieves historical data for a ticker using yfinance and converts it to JSON.
    
    Args:
        ticker (str): The stock symbol (e.g., 'AAPL')
        period (str): The time period (e.g., '5d', '1mo', '1y'...)
        interval (str): The interval between data points. Options:
            - '1m' (1 minute) - max 7 days
            - '2m' (2 minutes) - max 60 days
            - '5m' (5 minutes) - max 60 days
            - '15m' (15 minutes) - max 60 days
            - '30m' (30 minutes) - max 60 days
            - '60m' (1 hour) - max 730 days
            - '1d' (1 day) - max all
            - '1wk' (1 week) - max all
            - '1mo' (1 month) - max all
        
    Returns:
        str: A formatted JSON string containing market data
    """
    stock = yf.Ticker(ticker)

    # Get company information
    info = stock.info
    history = stock.history(period=period, interval=interval)

    # Convert DataFrame to JSON dictionary list
    json_data = []
    for date, row in history.iterrows():
        json_data.append({
            "date": date.strftime('%Y-%m-%d %H:%M:%S'),
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
    # Example with 5-minute intervals for the last day
    json_result = get_market_data("AAPL", "1d", "5m")
    print(json_result)
