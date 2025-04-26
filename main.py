from trading_system.agents.trading_orchestrator import TradingOrchestrator
import sys
import json

def main():
    """
    Main function to test the trading orchestrator with a stock symbol.
    Usage: python main.py <stock_symbol>
    Example: python main.py AAPL
    """
    if len(sys.argv) != 2:
        print("Usage: python main.py <stock_symbol>")
        print("Example: python main.py AAPL")
        sys.exit(1)
    
    stock_symbol = sys.argv[1].upper()
    print(f"\n=== Starting analysis for {stock_symbol} ===\n")
    
    orchestrator = TradingOrchestrator()
    results = orchestrator.analyze_stock(stock_symbol)  # Changed from process() to analyze_stock()
    
    print("\n=== Analysis Results ===\n")
    
    # Check for errors
    if "error" in results:
        print("Error:", results["error"])
        if "details" in results:
            print("\nDetails:")
            for error in results["details"]:
                print(f"- {error}")
        sys.exit(1)
    
    # Print each section of the analysis
    for section, data in results.items():
        if section == "recommendation":
            print("\n=== Trading Recommendation ===\n")
            print(data)
        elif section != "raw_data":  # Skip printing raw data unless specifically needed
            print(f"\n=== {section.capitalize()} Analysis ===\n")
            if isinstance(data, dict):
                if "analysis" in data:
                    print(data["analysis"])
                if "sentiment_score" in data:
                    print(f"Sentiment Score: {data['sentiment_score']}")
            else:
                print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main() 