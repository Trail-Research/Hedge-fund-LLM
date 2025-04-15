from typing import Dict, Any

class TraderAgent:
    def __init__(self):
        self.current_position = None
        self.trading_threshold = 0.7  # Confidence threshold for making trades
        # Weights for different data sources
        self.source_weights = {
            "fundamentals": 0.35,  # Fundamental analysis has highest weight
            "market": 0.30,       # Technical/market analysis second highest
            "news": 0.20,         # News sentiment
            "social": 0.15        # Social media sentiment lowest weight
        }

    def process(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process research data and make trading decisions.
        
        Args:
            research_data (Dict[str, Any]): Combined analysis from research team
            
        Returns:
            Dict[str, Any]: Trading proposal including action, size, and rationale
        """
        try:
            # Initialize signal counters
            bullish_signals = 0
            bearish_signals = 0
            total_weight = 0
            
            # Analyze fundamental signals
            if research_data.get("fundamentals", {}).get("recommendation") == "buy":
                bullish_signals += self.source_weights["fundamentals"]
                total_weight += self.source_weights["fundamentals"]
            elif research_data.get("fundamentals", {}).get("recommendation") == "sell":
                bearish_signals += self.source_weights["fundamentals"]
                total_weight += self.source_weights["fundamentals"]
                
            # Analyze market signals
            if research_data.get("market", {}).get("trend") == "upward":
                bullish_signals += self.source_weights["market"]
                total_weight += self.source_weights["market"]
            elif research_data.get("market", {}).get("trend") == "downward":
                bearish_signals += self.source_weights["market"]
                total_weight += self.source_weights["market"]
            
            # Analyze news sentiment
            news_sentiment = research_data.get("news", {}).get("sentiment", "neutral")
            if news_sentiment == "positive":
                bullish_signals += self.source_weights["news"]
                total_weight += self.source_weights["news"]
            elif news_sentiment == "negative":
                bearish_signals += self.source_weights["news"]
                total_weight += self.source_weights["news"]
            
            # Analyze social media sentiment
            social_sentiment = research_data.get("social", {}).get("sentiment", "neutral")
            if social_sentiment == "positive":
                bullish_signals += self.source_weights["social"]
                total_weight += self.source_weights["social"]
            elif social_sentiment == "negative":
                bearish_signals += self.source_weights["social"]
                total_weight += self.source_weights["social"]
                
            # Calculate weighted confidence score
            if total_weight == 0:
                confidence = 0
                action = "hold"
            else:
                # Normalize signals by total weight considered
                bullish_signals = bullish_signals / total_weight
                bearish_signals = bearish_signals / total_weight
                
                if bullish_signals > bearish_signals:
                    confidence = bullish_signals
                    action = "buy" if confidence >= self.trading_threshold else "hold"
                else:
                    confidence = bearish_signals
                    action = "sell" if confidence >= self.trading_threshold else "hold"
            
            return {
                "action": action,
                "confidence": confidence,
                "position_size": self._calculate_position_size(confidence),
                "rationale": self._generate_rationale(research_data, action, confidence),
                "signal_breakdown": {
                    "fundamentals": research_data.get("fundamentals", {}).get("recommendation", "neutral"),
                    "market": research_data.get("market", {}).get("trend", "neutral"),
                    "news": news_sentiment,
                    "social": social_sentiment
                }
            }
            
        except Exception as e:
            return {"error": f"Error in trader processing: {str(e)}"}
            
    def _calculate_position_size(self, confidence: float) -> float:
        """Calculate position size based on confidence level."""
        # Basic position sizing based on confidence
        base_size = 1.0  # Base position size (100%)
        return base_size * confidence
        
    def _generate_rationale(self, research_data: Dict[str, Any], action: str, confidence: float) -> str:
        """Generate a detailed rationale for the trading decision."""
        rationale = f"Trading decision: {action.upper()} with {confidence:.2%} confidence.\n"
        rationale += "Based on:\n"
        
        if research_data.get("fundamentals"):
            rationale += f"- Fundamental Analysis ({self.source_weights['fundamentals']*100:.0f}% weight): {research_data['fundamentals'].get('summary', 'N/A')}\n"
        if research_data.get("market"):
            rationale += f"- Market Analysis ({self.source_weights['market']*100:.0f}% weight): {research_data['market'].get('summary', 'N/A')}\n"
        if research_data.get("news"):
            rationale += f"- News Sentiment ({self.source_weights['news']*100:.0f}% weight): {research_data['news'].get('summary', 'N/A')}\n"
        if research_data.get("social"):
            rationale += f"- Social Sentiment ({self.source_weights['social']*100:.0f}% weight): {research_data['social'].get('summary', 'N/A')}\n"
            
        return rationale 