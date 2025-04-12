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

def extract_key_metrics(fundamentals_data: dict) -> dict:
    """
    Extrait les métriques clés des données fondamentales pour l'analyse de trading.
    
    Args:
        fundamentals_data (dict): Données complètes des fondamentaux
        
    Returns:
        dict: Dictionnaire contenant uniquement les métriques clés
    """
    profile = fundamentals_data["profile"][0]
    ratios = fundamentals_data["ratios"][0]
    balance_sheet = fundamentals_data["balance_sheet"][0]
    income_statement = fundamentals_data["income_statement"][0]
    
    return {
        # Informations générales
        "symbol": profile["symbol"],
        "company_name": profile["companyName"],
        "sector": profile["sector"],
        "industry": profile["industry"],
        "beta": profile["beta"],
        "employees": profile["fullTimeEmployees"],
        
        # Métriques de valorisation
        "price": profile["price"],
        "market_cap": profile["mktCap"],
        "pe_ratio": ratios["peRatioTTM"],
        "price_to_book": ratios["priceToBookRatioTTM"],
        "price_to_sales": ratios["priceToSalesRatioTTM"],
        "enterprise_value": profile["mktCap"] + balance_sheet["totalDebt"] - balance_sheet["cashAndCashEquivalents"],
        
        # Métriques de rentabilité
        "profit_margin": ratios["netProfitMarginTTM"],
        "return_on_equity": ratios["returnOnEquityTTM"],
        "return_on_assets": ratios["returnOnAssetsTTM"],
        "operating_margin": ratios["operatingProfitMarginTTM"],
        "ebitda_margin": income_statement["ebitdaratio"],
        
        # Métriques de liquidité
        "current_ratio": ratios["currentRatioTTM"],
        "quick_ratio": ratios["quickRatioTTM"],
        "cash_ratio": ratios["cashRatioTTM"],
        "working_capital": balance_sheet["totalCurrentAssets"] - balance_sheet["totalCurrentLiabilities"],
        "cash_and_equivalents": balance_sheet["cashAndCashEquivalents"],
        
        # Métriques de levier
        "debt_to_equity": ratios["debtEquityRatioTTM"],
        "total_debt": balance_sheet["totalDebt"],
        "interest_coverage": ratios["interestCoverageTTM"],
        "debt_ratio": ratios["debtRatioTTM"],
        
        # Métriques de croissance
        "revenue": income_statement["revenue"],
        "gross_profit": income_statement["grossProfit"],
        "operating_income": income_statement["operatingIncome"],
        "net_income": income_statement["netIncome"],
        "eps": income_statement["eps"],
        "eps_diluted": income_statement["epsdiluted"],
        
        # Métriques de dividendes
        "dividend_yield": ratios["dividendYielTTM"],
        "payout_ratio": ratios["payoutRatioTTM"],
        "dividend_per_share": ratios["dividendPerShareTTM"],
        
        # Métriques d'efficacité
        "asset_turnover": ratios["assetTurnoverTTM"],
        "inventory_turnover": ratios["inventoryTurnoverTTM"],
        "receivables_turnover": ratios["receivablesTurnoverTTM"],
        "days_sales_outstanding": ratios["daysOfSalesOutstandingTTM"],
        "days_inventory": ratios["daysOfInventoryOutstandingTTM"],
        
        # Métriques de flux de trésorerie
        "operating_cash_flow_per_share": ratios["operatingCashFlowPerShareTTM"],
        "free_cash_flow_per_share": ratios["freeCashFlowPerShareTTM"],
        "cash_per_share": ratios["cashPerShareTTM"],
        
        # Métriques de valorisation relative
        "price_to_free_cash_flow": ratios["priceToFreeCashFlowsRatioTTM"],
        "price_to_operating_cash_flow": ratios["priceToOperatingCashFlowsRatioTTM"],
        "enterprise_value_multiple": ratios["enterpriseValueMultipleTTM"]
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
    tool = "financial_modeling_prep" # "financial_modeling_prep" or "yahoo_finance"
    API_KEY = os.getenv("FINN_API_KEY")
    symbol = "AAPL"

    if tool == "financial_modeling_prep":
        data = get_all_fundamentals(symbol)
        #print(json.dumps(data, indent=2))
        print(json.dumps(extract_key_metrics(data), indent=2))
    elif tool == "yahoo_finance":
        data = get_company_info(symbol)
        print("\nCompany Info:")
        print(data)

