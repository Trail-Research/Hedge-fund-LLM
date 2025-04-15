import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "TradingAgent/1.0")

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Trading Parameters
MAX_POSITION_SIZE = float(os.getenv("MAX_POSITION_SIZE", "1.0"))  # 100% of portfolio
RISK_FREE_RATE = float(os.getenv("RISK_FREE_RATE", "0.02"))  # 2% annual risk-free rate
MAX_DRAWDOWN = float(os.getenv("MAX_DRAWDOWN", "0.10"))  # 10% maximum drawdown

# Data Collection Parameters
SOCIAL_MEDIA_LOOKBACK_DAYS = int(os.getenv("SOCIAL_MEDIA_LOOKBACK_DAYS", "7"))
NEWS_LOOKBACK_DAYS = int(os.getenv("NEWS_LOOKBACK_DAYS", "30"))
MARKET_DATA_LOOKBACK_DAYS = int(os.getenv("MARKET_DATA_LOOKBACK_DAYS", "252"))  # One trading year

# Model Parameters
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.7"))
SENTIMENT_THRESHOLD = float(os.getenv("SENTIMENT_THRESHOLD", "0.6"))
