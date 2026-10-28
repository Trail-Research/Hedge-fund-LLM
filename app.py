"""
Interface de démonstration du système de trading multi-agents.
Usage: streamlit run app.py
"""

import contextlib
import io
import json

import pandas as pd
import streamlit as st

from trading_system.agents.trading_orchestrator import TradingOrchestrator

COMPONENTS = {
    "fundamentals": "Fondamentaux",
    "social": "Réseaux sociaux",
    "news": "Actualités",
    "market": "Marché",
    "trading": "Recommandation",
}

ACTION_COLORS = {"BUY": "green", "SELL": "red", "HOLD": "orange"}


def run_analysis(stock_symbol: str, use_test_data: dict) -> tuple:
    """
    Lance l'orchestrateur en capturant ses logs (stdout) pour les afficher dans l'interface.

    Returns:
        tuple: (résultats de l'analyse, portefeuille, logs d'exécution)
    """
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        try:
            orchestrator = TradingOrchestrator(use_test_data=use_test_data)
            results = orchestrator.analyze_stock(stock_symbol)
            portfolio = orchestrator.portfolio
        except Exception as e:
            results = {"error": f"{type(e).__name__}: {e}"}
            portfolio = None
    return results, portfolio, buffer.getvalue()


def show_data(data):
    """Affiche une donnée brute qu'elle soit dict, chaîne JSON ou texte."""
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except ValueError:
            st.text(data)
            return
    if isinstance(data, (dict, list)):
        st.json(data, expanded=False)
    else:
        st.write(data)


def show_analysis(data):
    """Les analyses sont soit une chaîne, soit un dict contenant la clé 'analysis'."""
    if isinstance(data, dict):
        st.markdown(data.get("analysis", ""))
        if "sentiment_score" in data:
            st.metric("Score de sentiment", data["sentiment_score"])
    else:
        st.markdown(str(data))


def show_portfolio(portfolio: dict):
    st.subheader("Portefeuille")
    col1, col2, col3 = st.columns(3)
    col1.metric("Valeur totale", f"${portfolio.get('total_value', 0):,.0f}")
    col2.metric("Liquidités", f"${portfolio.get('cash', 0):,.0f}")
    col3.metric("Investi", f"${portfolio.get('invested_value', 0):,.0f}")
    assets = portfolio.get("invested_assets", {})
    if assets:
        st.dataframe(
            pd.DataFrame(
                [{"Actif": asset, "Montant ($)": amount} for asset, amount in assets.items()]
            ),
            hide_index=True,
            use_container_width=True,
        )


def show_recommendation(recommendation):
    if not isinstance(recommendation, dict):
        st.markdown(str(recommendation))
        return

    order = recommendation.get("order")
    status = recommendation.get("status")

    if order:
        action = str(order.get("action", "")).upper()
        color = ACTION_COLORS.get(action, "gray")
        st.markdown(f"## :{color}[{action}] {order.get('asset', '')}")

        if status == "approved_by_risk":
            st.success("Ordre validé par l'équipe de gestion des risques")
        elif status == "rejected_by_risk":
            st.error("Ordre rejeté par l'équipe de gestion des risques (voir le journal d'exécution)")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Montant", f"${order.get('notional_amount', 0):,.0f}")
        col2.metric("Prix d'entrée", f"${order.get('entry_price', 0):,.2f}")
        col3.metric("Stop-loss", f"${order.get('stop_loss', 0):,.2f}")
        col4.metric("Objectif", f"${order.get('target_price', 0):,.2f}")

        with st.expander("Détail de l'ordre"):
            st.json(order)
    else:
        st.info("Aucun ordre généré.")

    text = recommendation.get("recommendation")
    if text:
        st.markdown("### Justification")
        st.markdown(text)


def show_market(market_analysis, market_data):
    if isinstance(market_data, dict):
        price_data = market_data.get("price_data", {})
        if price_data:
            current = price_data.get("current_price")
            previous = price_data.get("previous_close")
            delta = f"{current - previous:+.2f}" if current and previous else None
            col1, col2, col3 = st.columns(3)
            col1.metric("Prix actuel", current, delta)
            col2.metric("Volume", f"{price_data.get('volume', 0):,}")
            col3.metric("P/E", price_data.get("pe_ratio"))

        historical = market_data.get("historical_data", {})
        if historical:
            period = st.selectbox("Période", list(historical.keys()), index=len(historical) - 1)
            st.line_chart(pd.DataFrame({"Prix": historical[period]}))

    show_analysis(market_analysis)


def main():
    st.set_page_config(page_title="Hedge Fund LLM", page_icon="📈", layout="wide")
    st.title("Hedge Fund LLM — Système de trading multi-agents")

    with st.sidebar:
        st.header("Paramètres")
        stock_symbol = st.text_input("Symbole boursier", value="AAPL").strip().upper()

        st.subheader("Données simulées")
        st.caption("Décochez pour utiliser les APIs réelles (clés requises dans .env).")
        use_test_data = {
            key: st.checkbox(label, value=True, key=f"test_{key}")
            for key, label in COMPONENTS.items()
        }

        launch = st.button("Lancer l'analyse", type="primary", use_container_width=True)

    if launch:
        if not stock_symbol:
            st.warning("Veuillez saisir un symbole boursier.")
        else:
            with st.spinner(f"Analyse de {stock_symbol} en cours..."):
                st.session_state["result"] = (stock_symbol, *run_analysis(stock_symbol, use_test_data))

    if "result" not in st.session_state:
        st.info("Choisissez un symbole et lancez l'analyse depuis la barre latérale.")
        return

    stock_symbol, results, portfolio, logs = st.session_state["result"]
    st.header(f"Analyse de {stock_symbol}")

    if "error" in results:
        st.error(results["error"])
    else:
        raw_data = results.get("raw_data", {})
        tabs = st.tabs(
            ["🎯 Recommandation", "📊 Fondamentaux", "📈 Marché", "📰 Actualités", "📱 Réseaux sociaux", "🗂️ Données brutes"]
        )
        with tabs[0]:
            show_recommendation(results.get("recommendation"))
            if portfolio:
                show_portfolio(portfolio)
        with tabs[1]:
            show_analysis(results.get("fundamentals"))
        with tabs[2]:
            show_market(results.get("market"), raw_data.get("market"))
        with tabs[3]:
            show_analysis(results.get("news"))
        with tabs[4]:
            show_analysis(results.get("social"))
        with tabs[5]:
            for key, label in COMPONENTS.items():
                if key in raw_data:
                    st.markdown(f"**{label}**")
                    show_data(raw_data[key])

    with st.expander("Journal d'exécution"):
        st.code(logs or "(vide)", language="text")


if __name__ == "__main__":
    main()
