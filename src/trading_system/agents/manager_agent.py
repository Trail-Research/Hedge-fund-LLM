from typing import Dict, Any
from datetime import datetime

class ManagerAgent:
    def __init__(self):
        self.daily_trade_count = 0
        self.daily_risk_budget = 1.0  # 100% at start of day
        self.max_daily_trades = 10
        self.min_confidence_threshold = 0.6
        self.last_reset = datetime.now().date()
        
    def process(self, 
               trading_proposal: Dict[str, Any], 
               risk_assessment: Dict[str, Any],
               portfolio_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make final decision on trade execution based on trader proposal and risk assessment.
        
        Args:
            trading_proposal (Dict[str, Any]): Proposed trade from trader
            risk_assessment (Dict[str, Any]): Risk evaluation from risk management
            portfolio_state (Dict[str, Any]): Current portfolio state and constraints
            
        Returns:
            Dict[str, Any]: Final decision and execution parameters
        """
        try:
            # Reset daily counters if needed
            self._check_daily_reset()
            
            # Initial validation
            if not self._validate_trade_request(trading_proposal, risk_assessment):
                return {
                    "approved": False,
                    "reason": "Trade validation failed",
                    "details": self._get_validation_details(trading_proposal, risk_assessment)
                }
            
            # Check portfolio constraints
            if not self._check_portfolio_constraints(portfolio_state, trading_proposal):
                return {
                    "approved": False,
                    "reason": "Portfolio constraints not met",
                    "details": self._get_portfolio_constraint_details(portfolio_state)
                }
            
            # Make final decision
            decision = self._make_decision(trading_proposal, risk_assessment, portfolio_state)
            
            # Update daily counters if trade approved
            if decision["approved"]:
                self._update_daily_counters(decision["risk_usage"])
            
            return decision
            
        except Exception as e:
            return {
                "approved": False,
                "error": f"Error in manager processing: {str(e)}"
            }
    
    def _check_daily_reset(self):
        """Reset daily counters if it's a new day."""
        current_date = datetime.now().date()
        if current_date != self.last_reset:
            self.daily_trade_count = 0
            self.daily_risk_budget = 1.0
            self.last_reset = current_date
    
    def _validate_trade_request(self, 
                              proposal: Dict[str, Any], 
                              risk_assessment: Dict[str, Any]) -> bool:
        """Validate basic trade request parameters."""
        # Check if we've exceeded daily trade limit
        if self.daily_trade_count >= self.max_daily_trades:
            return False
            
        # Check confidence threshold
        if proposal.get("confidence", 0) < self.min_confidence_threshold:
            return False
            
        # Check risk approval
        if not risk_assessment.get("approval", False):
            return False
            
        return True
    
    def _check_portfolio_constraints(self, 
                                   portfolio: Dict[str, Any], 
                                   proposal: Dict[str, Any]) -> bool:
        """Check if trade meets portfolio constraints."""
        # Check if we have enough buying power
        if proposal.get("action") == "buy":
            required_capital = proposal.get("position_size", 0) * proposal.get("price", 0)
            if required_capital > portfolio.get("available_capital", 0):
                return False
        
        # Check sector exposure limits
        sector = proposal.get("sector")
        if sector:
            current_sector_exposure = portfolio.get("sector_exposure", {}).get(sector, 0)
            if current_sector_exposure + proposal.get("position_size", 0) > 0.3:  # 30% sector limit
                return False
        
        return True
    
    def _make_decision(self, 
                      proposal: Dict[str, Any], 
                      risk_assessment: Dict[str, Any],
                      portfolio: Dict[str, Any]) -> Dict[str, Any]:
        """Make final trading decision."""
        # Use risk-adjusted position size
        adjusted_size = risk_assessment["adjusted_position_size"]
        
        # Calculate risk usage for this trade
        risk_usage = self._calculate_risk_usage(proposal, risk_assessment)
        
        # Check if we have enough risk budget
        if risk_usage > self.daily_risk_budget:
            return {
                "approved": False,
                "reason": "Insufficient risk budget",
                "remaining_budget": self.daily_risk_budget
            }
        
        return {
            "approved": True,
            "action": proposal["action"],
            "symbol": proposal.get("symbol"),
            "position_size": adjusted_size,
            "stop_loss": risk_assessment["stop_loss"],
            "risk_usage": risk_usage,
            "execution_parameters": {
                "order_type": "market",  # Could be more sophisticated
                "time_in_force": "day",
                "timestamp": datetime.now().isoformat()
            }
        }
    
    def _calculate_risk_usage(self, 
                            proposal: Dict[str, Any], 
                            risk_assessment: Dict[str, Any]) -> float:
        """Calculate how much of the daily risk budget this trade will use."""
        base_risk = risk_assessment["risk_factors"]["total_risk_score"]
        position_size_factor = proposal.get("position_size", 0)
        return base_risk * position_size_factor
    
    def _update_daily_counters(self, risk_usage: float):
        """Update daily counters after approved trade."""
        self.daily_trade_count += 1
        self.daily_risk_budget -= risk_usage
    
    def _get_validation_details(self, 
                              proposal: Dict[str, Any], 
                              risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed validation failure reasons."""
        return {
            "daily_trades_remaining": self.max_daily_trades - self.daily_trade_count,
            "confidence_threshold_met": proposal.get("confidence", 0) >= self.min_confidence_threshold,
            "risk_approval": risk_assessment.get("approval", False)
        }
    
    def _get_portfolio_constraint_details(self, portfolio: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed portfolio constraint failure reasons."""
        return {
            "available_capital": portfolio.get("available_capital", 0),
            "sector_exposures": portfolio.get("sector_exposure", {}),
            "current_positions": portfolio.get("positions", {})
        } 