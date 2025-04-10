import requests
import os
import yfinance as yf
import json
from dotenv import load_dotenv

load_dotenv()

base_url = "https://financialmodelingprep.com/api/v3"


################################################################################
# Financial Modeling Prep API
################################################################################
FINN_API_KEY = os.getenv("FINN_API_KEY")

def get_financial_ratios(symbol: str) -> dict:
    """
    Retrieves the latest financial ratios for a given company.
    
    Args:
        symbol (str): The stock symbol (e.g., 'AAPL' for Apple)
        
    Returns:
        dict: Financial ratios in TTM (Trailing Twelve Months) format
    """
    url = f"{base_url}/ratios-ttm/{symbol}?apikey={FINN_API_KEY}"
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
    url = f"{base_url}/balance-sheet-statement/{symbol}?limit=1&apikey={FINN_API_KEY}"
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
    url = f"{base_url}/income-statement/{symbol}?limit=1&apikey={FINN_API_KEY}"
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
    url = f"{base_url}/profile/{symbol}?apikey={FINN_API_KEY}"
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

################################################################################
# Yahoo Finance API
################################################################################
def get_company_info(ticker: str) -> str:
    """
    Retrieves company information for a ticker using yfinance and converts it to JSON.
    
    Args:
        ticker (str): The stock symbol (e.g., 'AAPL')
        
    Returns:
        str: A formatted JSON string containing company information
    """
    stock = yf.Ticker(ticker)
    info = stock.info
    return json.dumps(info, indent=4)


# Example usage
if __name__ == "__main__":
    tool = "yahoo_finance" # "financial_modeling_prep" or "yahoo_finance"
    API_KEY = os.getenv("FINN_API_KEY")
    symbol = "AAPL"

    if tool == "financial_modeling_prep":
        data = get_all_fundamentals("AAPL")
        print(json.dumps(data, indent=2))
    elif tool == "yahoo_finance":
        data = get_company_info("AAPL")
        print("\nCompany Info:")
        print(data)

