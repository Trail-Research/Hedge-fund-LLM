"""
Exporte les données de la démo publique (mode données simulées) pour la page statique
de trail-landing (public/demo/data.js).
Usage: python scripts/export_demo_data.py > ../trail-landing/public/demo/data.js
"""

import contextlib
import io
import json

from trading_system.agents.trading_orchestrator import TradingOrchestrator


def parse_json(data):
    if isinstance(data, str):
        try:
            return json.loads(data)
        except ValueError:
            return data
    if isinstance(data, dict):
        return {key: parse_json(value) for key, value in data.items()}
    return data


def main():
    logs = io.StringIO()
    with contextlib.redirect_stdout(logs):
        orchestrator = TradingOrchestrator()  # toutes les sources en données simulées
        results = orchestrator.analyze_stock("AAPL")

    portfolio = {
        key: value for key, value in orchestrator.portfolio.items() if not callable(value)
    }
    data = {
        "symbol": "AAPL",
        "logs": [line.strip() for line in logs.getvalue().splitlines() if line.strip()],
        "results": parse_json(results),
        "portfolio": portfolio,
    }
    print("// Généré par Hedge-fund-LLM/scripts/export_demo_data.py — ne pas modifier à la main.")
    print(f"window.DEMO_DATA = {json.dumps(data, ensure_ascii=False, indent=1)};")


if __name__ == "__main__":
    main()
