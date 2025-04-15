from typing import Dict, Any
from enum import Enum

class RiskProfile(Enum):
    CONSERVATIVE = "conservative"
    NEUTRAL = "neutral"
    AGGRESSIVE = "aggressive"

class RiskManagementAgent:
    def __init__(self, risk_profile: RiskProfile = RiskProfile.NEUTRAL):
        self.risk_profile = risk_profile
        self.max_position_size = self._get_max_position_size()
        self.stop_loss_levels = self._get_stop_loss_levels()
        
    def process(self, trading_proposal: Dict[str, Any], market_conditions: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate trading proposal against risk parameters and market conditions.
        
        Args:
            trading_proposal (Dict[str, Any]): Proposed trade from trader
            market_conditions (Dict[str, Any]): Current market conditions
            
        Returns:
            Dict[str, Any]: Risk assessment and adjusted trading parameters
        """
        try:
            # Evaluate market volatility
            volatility_risk = self._assess_volatility(market_conditions)
            
            # Evaluate position size risk
            position_size = trading_proposal.get("position_size", 0)
            size_risk = self._assess_position_size(position_size)
            
            # Calculate overall risk score
            risk_score = self._calculate_risk_score(volatility_risk, size_risk)
            
            # Adjust position size if necessary
            adjusted_position = self._adjust_position_size(position_size, risk_score)
            
            # Generate risk assessment
            assessment = {
                "risk_level": self._categorize_risk(risk_score),
                "original_position_size": position_size,
                "adjusted_position_size": adjusted_position,
                "stop_loss": self._calculate_stop_loss(trading_proposal, market_conditions),
                "risk_factors": {
                    "volatility": volatility_risk,
                    "position_size": size_risk,
                    "total_risk_score": risk_score
                },
                "approval": risk_score <= self._get_risk_threshold()
            }
            
            return assessment
            
        except Exception as e:
            return {"error": f"Error in risk assessment: {str(e)}"}
    
    def _get_max_position_size(self) -> float:
        """Get maximum position size based on risk profile."""
        return {
            RiskProfile.CONSERVATIVE: 0.1,  # 10% of portfolio
            RiskProfile.NEUTRAL: 0.2,      # 20% of portfolio
            RiskProfile.AGGRESSIVE: 0.3    # 30% of portfolio
        }[self.risk_profile]
    
    def _get_stop_loss_levels(self) -> float:
        """Get stop loss levels based on risk profile."""
        return {
            RiskProfile.CONSERVATIVE: 0.02,  # 2% loss
            RiskProfile.NEUTRAL: 0.05,      # 5% loss
            RiskProfile.AGGRESSIVE: 0.08    # 8% loss
        }[self.risk_profile]
    
    def _assess_volatility(self, market_conditions: Dict[str, Any]) -> float:
        """Assess market volatility risk."""
        volatility = market_conditions.get("volatility", 0)
        if volatility > 0.3:  # High volatility
            return 1.0
        elif volatility > 0.15:  # Medium volatility
            return 0.5
        return 0.2  # Low volatility
    
    def _assess_position_size(self, size: float) -> float:
        """Assess position size risk."""
        if size > self.max_position_size:
            return 1.0
        return size / self.max_position_size
    
    def _calculate_risk_score(self, volatility_risk: float, size_risk: float) -> float:
        """Calculate overall risk score."""
        weights = {
            "volatility": 0.6,
            "size": 0.4
        }
        return (volatility_risk * weights["volatility"] + 
                size_risk * weights["size"])
    
    def _adjust_position_size(self, original_size: float, risk_score: float) -> float:
        """Adjust position size based on risk score."""
        if risk_score > 0.8:
            return original_size * 0.5  # Reduce position by 50%
        elif risk_score > 0.6:
            return original_size * 0.7  # Reduce position by 30%
        return original_size
    
    def _calculate_stop_loss(self, proposal: Dict[str, Any], market_conditions: Dict[str, Any]) -> float:
        """Calculate stop loss level based on risk profile and market conditions."""
        base_stop = self.stop_loss_levels
        volatility_adjustment = market_conditions.get("volatility", 0) * 0.5
        return base_stop + volatility_adjustment
    
    def _categorize_risk(self, risk_score: float) -> str:
        """Categorize risk level based on risk score."""
        if risk_score > 0.7:
            return "HIGH"
        elif risk_score > 0.4:
            return "MEDIUM"
        return "LOW"
    
    def _get_risk_threshold(self) -> float:
        """Get maximum acceptable risk threshold based on risk profile."""
        return {
            RiskProfile.CONSERVATIVE: 0.4,
            RiskProfile.NEUTRAL: 0.6,
            RiskProfile.AGGRESSIVE: 0.8
        }[self.risk_profile] 