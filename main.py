from src.trading_system.agents.orchestrator import Orchestrator
import sys
import json

def main():
    """
    Main function to test the orchestrator with a stock symbol.
    Usage: python orchestrator.py <stock_symbol>
    Example: python orchestrator.py AAPL
    """
    if len(sys.argv) != 2:
        print("Usage: python orchestrator.py <stock_symbol>")
        print("Example: python orchestrator.py AAPL")
        sys.exit(1)
    
    stock_symbol = sys.argv[1].upper()
    print(f"\n=== Starting analysis for {stock_symbol} ===\n")
    
    orchestrator = Orchestrator()
    results = orchestrator.process(stock_symbol)
    
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
        else:
            print(f"\n=== {section.capitalize()} Analysis ===\n")
            if isinstance(data, dict) and "analysis" in data:
                print(data["analysis"])
            else:
                print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main() 