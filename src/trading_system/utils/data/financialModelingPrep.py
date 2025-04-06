import requests
import os
from dotenv import load_dotenv

load_dotenv()

base_url = "https://financialmodelingprep.com/api/v3"

def get_financial_ratios(symbol: str) -> dict:
    """
    Retrieves the latest financial ratios for a given company.
    
    Args:
        symbol (str): The stock symbol (e.g., 'AAPL' for Apple)
        
    Returns:
        dict: Financial ratios in TTM (Trailing Twelve Months) format
    """
    url = f"{base_url}/ratios-ttm/{symbol}?apikey={API_KEY}"
    response = requests.get(url)
    return response.json()

def get_balance_sheet(symbol: str) -> dict:
    """
    Retrieves the latest balance sheet statement for a given company.
    
    Args:
        symbol (str): The stock symbol (e.g., 'AAPL' for Apple)
        
    Returns:
        dict: Balance sheet data
    """
    url = f"{base_url}/balance-sheet-statement/{symbol}?limit=1&apikey={API_KEY}"
    response = requests.get(url)
    return response.json()

def get_income_statement(symbol: str) -> dict:
    """
    Retrieves the latest income statement for a given company.
    
    Args:
        symbol (str): The stock symbol (e.g., 'AAPL' for Apple)
        
    Returns:
        dict: Income statement data
    """
    url = f"{base_url}/income-statement/{symbol}?limit=1&apikey={API_KEY}"
    response = requests.get(url)
    return response.json()

def get_company_profile(symbol: str) -> dict:
    """
    Retrieves the company profile information.
    
    Args:
        symbol (str): The stock symbol (e.g., 'AAPL' for Apple)
        
    Returns:
        dict: Company profile data
    """
    url = f"{base_url}/profile/{symbol}?apikey={API_KEY}"
    response = requests.get(url)
    return response.json()

def get_all_fundamentals(symbol: str) -> dict:
    """
    Retrieves all fundamental data for a given company.
    
    Args:
        symbol (str): The stock symbol (e.g., 'AAPL' for Apple)
        
    Returns:
        dict: Dictionary containing all fundamental data
    """
    return {
        "profile": get_company_profile(symbol),
        "ratios": get_financial_ratios(symbol),
        "balance_sheet": get_balance_sheet(symbol),
        "income_statement": get_income_statement(symbol)
    }

# Example usage
if __name__ == "__main__":
    API_KEY = os.getenv("FINN_API_KEY")
    symbol = "AAPL"  # You can replace with MSFT, TSLA, etc.
    data = get_all_fundamentals("AAPL")
    import json
    print(json.dumps(data, indent=2))  # Pretty print the JSON
