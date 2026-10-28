from trading_system.agents.risk_team.marketConditions_agent.main import AgentRiskMarketConditions
from trading_system.agents.risk_team.exposure_agent.main import AgentRiskExposure
from trading_system.agents.risk_team.stopLoss_agent.main import AgentRiskStopLoss
from trading_system.agents.risk_team.compliance_agent.main import AgentRiskCompliance

def risk_management_pipeline(order, portfolio, mock_data_dict):
    agents = [
        AgentRiskExposure(max_exposure_per_asset=0.4),  # 40% max par actif
        AgentRiskMarketConditions(max_volatility=0.03, max_spread=0.001),
        AgentRiskStopLoss(default_stop_loss_percent=0.05),
        AgentRiskCompliance(
            max_asset_pct=0.40,                          # 40% max sur un seul actif
            max_sector_pct={"crypto": 0.20, "equities": 0.80},  # crypto max 20%, equities max 80%
            max_leverage=2.0
        ),
    ]

    for agent in agents:
        valid, order, reason = agent.check(order, portfolio, mock_data_dict)
        if not valid:
            print(f"[{agent.__class__.__name__}] Order rejected: {reason}")
            return None
        print(f"[{agent.__class__.__name__}] Order approved: {reason}")
    return order