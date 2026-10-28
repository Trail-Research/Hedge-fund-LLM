"""
Interface de démonstration du système de trading multi-agents (charte Trail Research).
Usage: streamlit run app.py
"""

import contextlib
import json
import os
import queue
import re
import textwrap
import threading
import time

import plotly.graph_objects as go
import streamlit as st

from trading_system.agents.trading_orchestrator import TradingOrchestrator

# --- Charte Trail Research (https://trailresear.ch) ---
PAPER = "#f9f9f5"
INK = "#1a3029"
MUTED = "#5e6962"
FOREST = "#193f34"
LINE = "#dedfd7"
SAGE = "#d3e6bf"
CARD = "#f0f1ea"
MOSS = "#66805a"
NEGATIVE = "#b5654a"
PALETTE = ["#193f34", "#66805a", "#a5b89a", "#d3e6bf", "#d9e0cd"]

# Démo publique : données simulées imposées, sans accès aux APIs réelles ni à leurs clés
PUBLIC_DEMO = os.getenv("PUBLIC_DEMO", "").lower() in ("1", "true", "yes")
DEMO_SYMBOL = "AAPL"  # Les données simulées des agents ne couvrent qu'Apple
STEP_DELAY = 0.75  # Pause entre deux étapes du pipeline, pour que la démo reste lisible

COMPONENTS = {
    "fundamentals": "Fondamentaux",
    "social": "Réseaux sociaux",
    "news": "Actualités",
    "market": "Marché",
    "trading": "Trader",
}
RISK_AGENTS = {
    "AgentRiskExposure": "Exposition",
    "AgentRiskMarketConditions": "Conditions de marché",
    "AgentRiskStopLoss": "Stop-loss",
    "AgentRiskCompliance": "Conformité",
}
ACTION_LABELS = {"BUY": "Acheter", "SELL": "Vendre", "HOLD": "Conserver"}

# Repères dans les logs de l'orchestrateur -> (étape, nouvel état)
LOG_MARKERS = [
    ("Fetching fundamentals data", "fundamentals", "running"),
    ("Fundamentals data fetched", "fundamentals", "done"),
    ("Fetching social media data", "social", "running"),
    ("Social media data fetched", "social", "done"),
    ("Fetching news data", "news", "running"),
    ("News data fetched", "news", "done"),
    ("Fetching market data", "market", "running"),
    ("Market data fetched", "market", "done"),
    ("Generating final recommendation", "trading", "running"),
    ("Analysis completed successfully", "trading", "done"),
    ("Running risk management checks", "risk", "running"),
    ("No order to validate", "risk", "skipped"),
]
RISK_LOG = re.compile(r"\[(AgentRisk\w+)\] Order (approved|rejected): (.*)")

LOGO_PATH = "M5 29 17 7h5L10 29Zm11 0L26 11h5L21 29Zm11 0 5-9v9Z"

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap');
html, body, [data-testid="stAppViewContainer"] {{ background: {PAPER}; color: {INK}; font-family: 'IBM Plex Sans', Arial, sans-serif; }}
[data-testid="stHeader"] {{ background: transparent; }}
[data-testid="stToolbar"], [data-testid="stDecoration"], footer {{ display: none; }}
.block-container {{ max-width: 1248px; padding-top: 0; }}
h1, h2, h3 {{ font-weight: 500 !important; letter-spacing: -0.02em; color: {INK}; }}
em {{ font-family: Georgia, 'Times New Roman', serif; font-weight: 400; color: {MOSS}; }}

.tr-header {{ display: flex; align-items: center; justify-content: space-between; height: 84px; border-bottom: 1px solid {LINE}; margin-bottom: 40px; }}
.tr-brand {{ display: inline-flex; gap: 11px; align-items: center; font-size: 22px; letter-spacing: -1px; font-weight: 600; color: {INK}; }}
.tr-brand svg {{ width: 30px; height: 30px; }}
.tr-brand .light {{ font-weight: 400; }}
.tr-brand .period {{ color: #5d8055; }}
.tr-header-tag {{ font: 400 10px/1.5 'IBM Plex Mono', monospace; letter-spacing: 1.6px; color: {MUTED}; }}

.tr-eyebrow {{ display: flex; align-items: center; gap: 10px; font: 400 10px/1.5 'IBM Plex Mono', monospace; letter-spacing: 1.6px; text-transform: uppercase; color: {MUTED}; }}
.tr-eyebrow::before {{ content: ""; width: 23px; height: 1px; background: #66845a; }}
.tr-hero-title {{ font-size: clamp(40px, 4.6vw, 66px); line-height: 1.06; letter-spacing: -3px; font-weight: 500; margin: 22px 0 0; color: {INK}; }}
.tr-hero-text {{ max-width: 440px; color: {MUTED}; line-height: 1.8; margin-top: 22px; }}
.tr-symbol {{ display: flex; align-items: center; gap: 12px; height: 40px; padding: 0 14px; border: 1px solid {LINE}; background: {CARD}; font-size: 13px; color: {MUTED}; white-space: nowrap; overflow: hidden; }}
.tr-symbol span {{ font: 500 13px/1 'IBM Plex Mono', monospace; letter-spacing: 1.4px; color: {FOREST}; }}
.tr-footnote {{ font-size: 11px; color: {MUTED}; margin-top: 30px; }}
.tr-footnote b {{ font: 20px/1 'IBM Plex Mono', monospace; color: #658258; font-weight: 400; margin-right: 8px; }}

.stButton > button {{ background: {FOREST}; color: #fff; border: 0; border-radius: 0; min-height: 49px; font-size: 13px; transition: background .2s, transform .2s; }}
.stButton > button:hover {{ background: #2b5343; color: #fff; transform: translateY(-2px); }}
.stButton > button:focus:not(:active) {{ color: #fff; }}
[data-baseweb="input"], [data-baseweb="base-input"], [data-baseweb="select"] > div {{ border-radius: 0 !important; }}
[data-baseweb="tab-list"] {{ gap: 28px; border-bottom: 1px solid {LINE}; }}
[data-baseweb="tab"] {{ font: 400 11px/1.5 'IBM Plex Mono', monospace !important; letter-spacing: 1.4px; text-transform: uppercase; padding-inline: 0; }}
[data-baseweb="tab-highlight"] {{ background: {FOREST}; }}

/* Graphe des agents, inspiré du bloc « signal » du site */
.tr-panel {{ position: relative; background: #17382e; color: #c3d0c3; padding: 22px 26px 18px; margin-top: 56px; overflow: hidden; box-shadow: 0 12px 28px #1a302907; }}
.tr-panel-top {{ position: relative; display: flex; justify-content: space-between; font: 400 10px/1.5 'IBM Plex Mono', monospace; letter-spacing: 1.6px; color: #a0b0a2; }}
.tr-graph {{ position: relative; width: 100%; height: auto; margin-top: 10px; overflow: visible; }}
.tr-graph text {{ font-family: 'IBM Plex Sans', Arial, sans-serif; }}
.tr-graph .col-label, .tr-graph .edge-label, .tr-graph .state {{ font-family: 'IBM Plex Mono', monospace; letter-spacing: 1.4px; }}
.tr-graph .col-label {{ font-size: 10px; fill: #7f978a; }}
.tr-graph .edge-label {{ font-size: 9px; fill: #8fa596; }}
.tr-graph .group {{ fill: #ffffff05; stroke: #ffffff26; stroke-dasharray: 4 5; }}
.tr-graph .node rect {{ fill: #ffffff08; stroke: #ffffff1f; transition: all .3s; }}
.tr-graph .node .name {{ font-size: 15px; fill: #c3d0c3; }}
.tr-graph .node .state {{ font-size: 9px; fill: #7f978a; }}
.tr-graph .node .dot {{ fill: #4d6a5d; }}
.tr-graph .node .halo {{ fill: none; stroke: {SAGE}; opacity: 0; }}
.tr-graph .node.is-running rect {{ fill: #d3e6bf14; stroke: {SAGE}99; }}
.tr-graph .node.is-running .dot, .tr-graph .node.is-done .dot {{ fill: {SAGE}; }}
.tr-graph .node.is-running .halo {{ animation: tr-halo 1.1s ease-out infinite; }}
.tr-graph .node.is-running .state, .tr-graph .node.is-done .state {{ fill: {SAGE}; }}
.tr-graph .node.is-done .name {{ fill: #fff; }}
.tr-graph .node.is-done rect {{ stroke: #d3e6bf55; }}
.tr-graph .node.is-rejected rect, .tr-graph .node.is-error rect {{ stroke: #e0957a99; fill: #e0957a12; }}
.tr-graph .node.is-rejected .dot, .tr-graph .node.is-error .dot {{ fill: #e0957a; }}
.tr-graph .node.is-rejected .state, .tr-graph .node.is-error .state {{ fill: #e0957a; }}
.tr-graph .node.output.is-done rect {{ fill: {SAGE}; stroke: {SAGE}; }}
.tr-graph .node.output.is-done .name, .tr-graph .node.output.is-done .state {{ fill: {FOREST}; }}
.tr-graph .node.output.is-done .dot {{ fill: {FOREST}; }}
@keyframes tr-halo {{ from {{ r: 5px; opacity: .9; }} to {{ r: 16px; opacity: 0; }} }}
.tr-graph .edge {{ fill: none; stroke-width: 1.6; transition: stroke .3s; }}
.tr-graph .edge.idle {{ stroke: #ffffff24; stroke-dasharray: 3 6; }}
.tr-graph .edge.ready {{ stroke: #d3e6bf66; }}
.tr-graph .edge.done {{ stroke: #d3e6bfb3; }}
.tr-graph .edge.active {{ stroke: {SAGE}; stroke-width: 2.2; stroke-dasharray: 7 7; animation: tr-flow .6s linear infinite; }}
.tr-graph .edge.ko {{ stroke: #e0957a; stroke-width: 2; }}
@keyframes tr-flow {{ to {{ stroke-dashoffset: -14; }} }}
.tr-ticker {{ position: relative; margin-top: 14px; padding-top: 12px; border-top: 1px solid #ffffff1c; font: 400 11px/1.7 'IBM Plex Mono', monospace; color: #8fa596; min-height: 62px; }}
.tr-ticker div:last-child {{ color: {SAGE}; }}
.tr-ticker div {{ white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
@media (max-width: 760px) {{ .tr-panel {{ padding: 16px 12px; }} .tr-graph .node .state, .tr-graph .edge-label {{ display: none; }} }}

/* Résultats */
.tr-section {{ margin-top: 64px; }}
.tr-decision {{ font-size: clamp(38px, 4vw, 58px); line-height: 1.05; letter-spacing: -2.5px; font-weight: 500; margin: 18px 0 14px; }}
.tr-pill {{ display: inline-flex; align-items: center; gap: 8px; padding: 6px 12px; font: 400 10px/1.5 'IBM Plex Mono', monospace; letter-spacing: 1.4px; text-transform: uppercase; }}
.tr-pill.ok {{ background: {SAGE}; color: {FOREST}; }}
.tr-pill.ko {{ background: #f3ddd4; color: #8a4430; }}
.tr-pill.neutral {{ background: {CARD}; color: {MUTED}; }}
.tr-tiles {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 1px; background: {LINE}; border: 1px solid {LINE}; margin-top: 26px; }}
.tr-tile {{ background: {PAPER}; padding: 16px 18px; animation: tr-rise .5s ease-out both; }}
.tr-tile .label {{ font: 400 9px/1.5 'IBM Plex Mono', monospace; letter-spacing: 1.4px; text-transform: uppercase; color: {MUTED}; }}
.tr-tile .value {{ font-size: 26px; letter-spacing: -1px; margin-top: 6px; color: {INK}; }}
.tr-tile .sub {{ font-size: 11px; color: {MOSS}; }}
@keyframes tr-rise {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}
.tr-checks {{ border-top: 1px solid {LINE}; margin-top: 8px; }}
.tr-check {{ display: grid; grid-template-columns: 26px 1fr; gap: 10px; padding: 12px 0; border-bottom: 1px solid {LINE}; animation: tr-rise .4s ease-out both; }}
.tr-check .mark {{ font: 15px/1.4 'IBM Plex Mono', monospace; color: {MOSS}; }}
.tr-check.ko .mark {{ color: {NEGATIVE}; }}
.tr-check.idle .mark {{ color: #b6bdb3; }}
.tr-check .title {{ font-size: 14px; font-weight: 500; }}
.tr-check .reason {{ font-size: 12px; color: {MUTED}; }}
.tr-prose {{ color: {INK}; line-height: 1.75; max-width: 780px; }}
.tr-company {{ font-size: 13px; color: {MUTED}; margin-top: 6px; }}
</style>
"""


def logo_svg(color=FOREST):
    return f'<svg viewBox="0 0 36 36" aria-hidden="true"><path d="{LOGO_PATH}" fill="{color}"/></svg>'


def html(markup: str):
    """Rend du HTML sans que Markdown interprète l'indentation."""
    st.markdown("".join(line.strip() for line in markup.splitlines()), unsafe_allow_html=True)


def dedent(text) -> str:
    """Retire l'indentation des textes des agents et échappe les $ (sinon interprétés comme du LaTeX)."""
    return textwrap.dedent(str(text)).strip().replace("$", "\\$")


def parse_json(data):
    if isinstance(data, str):
        try:
            return json.loads(data)
        except ValueError:
            return data
    return data


def money(value, decimals=0):
    try:
        return f"${float(value):,.{decimals}f}"
    except (TypeError, ValueError):
        return "—"


def pct(value):
    try:
        return f"{float(value):.0%}" if abs(float(value)) < 1.5 else f"{float(value):.2f}"
    except (TypeError, ValueError):
        return "—"


# --- Exécution en direct ---------------------------------------------------

class QueueWriter:
    """Remplace stdout pendant l'analyse : chaque ligne de log part dans une file."""

    def __init__(self):
        self.lines = queue.Queue()
        self._buffer = ""

    def write(self, text):
        self._buffer += text
        while "\n" in self._buffer:
            line, self._buffer = self._buffer.split("\n", 1)
            if line.strip():
                self.lines.put(line.strip())
        return len(text)

    def flush(self):
        pass


def initial_state():
    return {
        "steps": {key: "waiting" for key in [*COMPONENTS, "risk"]},
        "risk": {agent: ("waiting", "") for agent in RISK_AGENTS},
        "logs": [],
    }


def apply_log_line(state, line) -> bool:
    """Met à jour l'état du pipeline selon une ligne de log. Renvoie True si l'état a changé."""
    state["logs"].append(line)
    steps = state["steps"]
    for marker, step, status in LOG_MARKERS:
        if marker in line:
            steps[step] = status
            return True
    match = RISK_LOG.search(line)
    if match:
        agent, verdict, reason = match.groups()
        state["risk"][agent] = ("done" if verdict == "approved" else "rejected", reason)
        if verdict == "rejected":
            steps["risk"] = "rejected"
        elif all(status == "done" for status, _ in state["risk"].values()):
            steps["risk"] = "done"
        return True
    if "Error processing" in line:
        for step, status in steps.items():
            if status == "running":
                steps[step] = "error"
        return True
    return False


def run_live(stock_symbol, use_test_data, panel):
    """Lance l'orchestrateur dans un thread et anime le pipeline au fil des logs."""
    writer = QueueWriter()
    output = {}

    def worker():
        with contextlib.redirect_stdout(writer):
            try:
                orchestrator = TradingOrchestrator(use_test_data=use_test_data)
                output["results"] = orchestrator.analyze_stock(stock_symbol)
                output["portfolio"] = orchestrator.portfolio
            except Exception as e:
                print(f"[TradingOrchestrator] Error processing data for {stock_symbol}: {e}")
                output["results"] = {"error": f"{type(e).__name__}: {e}"}

    state = initial_state()
    thread = threading.Thread(target=worker, daemon=True)
    thread.start()
    while thread.is_alive() or not writer.lines.empty():
        try:
            line = writer.lines.get(timeout=0.1)
        except queue.Empty:
            continue
        match = RISK_LOG.search(line)
        if match:
            # Les contrôles de risque ne loggent que leur verdict : on affiche d'abord l'état « en cours »
            state["risk"][match.group(1)] = ("running", "")
            panel.markdown(pipeline_html(stock_symbol, state), unsafe_allow_html=True)
            time.sleep(STEP_DELAY)
        if apply_log_line(state, line):
            panel.markdown(pipeline_html(stock_symbol, state), unsafe_allow_html=True)
            time.sleep(STEP_DELAY)

    results = output.get("results", {"error": "Analyse interrompue"})
    status = (results.get("recommendation") or {}).get("status") if isinstance(results.get("recommendation"), dict) else None
    if status == "approved_by_risk":
        state["steps"]["risk"] = "done"
    elif status == "rejected_by_risk":
        state["steps"]["risk"] = "rejected"
    panel.markdown(pipeline_html(stock_symbol, state), unsafe_allow_html=True)
    return results, output.get("portfolio"), state


# --- Pipeline -------------------------------------------------------------

STATE_LABELS = {
    "waiting": "EN ATTENTE",
    "running": "EN COURS",
    "done": "OK",
    "rejected": "REJETÉ",
    "error": "ERREUR",
    "skipped": "AUCUN ORDRE",
}

# Géométrie du graphe (unités du viewBox 1200 x 410)
NODE_H = 54
ROWS = [50, 140, 230, 320]                      # haut des nœuds des colonnes analystes / risque
ANALYSTS_X, ANALYSTS_W = 30, 220
TRADER_X, TRADER_W, TRADER_Y, TRADER_H = 370, 190, 167, 90
RISK_X, RISK_W = 690, 230
OUTPUT_X, OUTPUT_W = 1010, 160
MID_Y = TRADER_Y + TRADER_H / 2


def svg_node(x, y, w, h, name, status, extra_class="", state_label=None):
    label = state_label or STATE_LABELS.get(status, "")
    cy = y + h / 2
    return (
        f'<g class="node is-{status} {extra_class}">'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}"/>'
        f'<circle class="halo" cx="{x + 20}" cy="{cy}" r="5"/>'
        f'<circle class="dot" cx="{x + 20}" cy="{cy}" r="5"/>'
        f'<text class="name" x="{x + 36}" y="{cy - 2}">{name}</text>'
        f'<text class="state" x="{x + 36}" y="{cy + 15}">{label}</text>'
        f"</g>"
    )


def edge_status(source, target):
    if source not in ("done", "rejected"):
        return "idle"
    if target in ("rejected", "error"):
        return "ko"
    if target == "running":
        return "active"
    if target in ("done", "skipped"):
        return "done"
    return "ready"


def svg_edge(path, status):
    """Lien entre deux agents ; un point parcourt le lien pendant que la cible travaille."""
    edge = f'<path class="edge {status}" d="{path}" marker-end="url(#tr-arrow-{status})"/>'
    if status == "active":
        edge += f'<circle r="4" fill="{SAGE}"><animateMotion dur="1.1s" repeatCount="indefinite" path="{path}"/></circle>'
    return edge


def pipeline_html(stock_symbol, state):
    steps, risk = state["steps"], state["risk"]
    risk_agents = list(RISK_AGENTS)
    output_status = {"done": "done", "rejected": "rejected", "skipped": "skipped", "error": "error"}.get(steps["risk"], "waiting")
    output_label = {"done": "VALIDÉ", "rejected": "REJETÉ", "skipped": "AUCUN"}.get(output_status)

    markers = "".join(
        f'<marker id="tr-arrow-{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M0 1 9 5 0 9z" fill="{color}"/></marker>'
        for name, color in [("idle", "#ffffff40"), ("ready", "#d3e6bf80"), ("done", "#d3e6bfcc"), ("active", SAGE), ("ko", "#e0957a")]
    )

    edges = []
    # Analystes -> Trader
    for key, top in zip(["fundamentals", "social", "news", "market"], ROWS):
        cy = top + NODE_H / 2
        x0, x1 = ANALYSTS_X + ANALYSTS_W, TRADER_X - 4
        edges.append(svg_edge(f"M{x0} {cy} C{x0 + 70} {cy} {x1 - 70} {MID_Y} {x1} {MID_Y}", edge_status(steps[key], steps["trading"])))
    # Trader -> premier contrôle de risque
    first_cy = ROWS[0] + NODE_H / 2
    x0, x1 = TRADER_X + TRADER_W, RISK_X - 4
    edges.append(svg_edge(f"M{x0} {MID_Y} C{x0 + 70} {MID_Y} {x1 - 70} {first_cy} {x1} {first_cy}", edge_status(steps["trading"], risk[risk_agents[0]][0])))
    # Chaîne des contrôles de risque (exécutés l'un après l'autre)
    center_x = RISK_X + RISK_W / 2
    for i in range(len(risk_agents) - 1):
        y0, y1 = ROWS[i] + NODE_H, ROWS[i + 1] - 4
        edges.append(svg_edge(f"M{center_x} {y0} L{center_x} {y1}", edge_status(risk[risk_agents[i]][0], risk[risk_agents[i + 1]][0])))
    # Dernier contrôle -> Ordre
    last_cy = ROWS[-1] + NODE_H / 2
    x0, x1 = RISK_X + RISK_W, OUTPUT_X - 4
    edges.append(svg_edge(f"M{x0} {last_cy} C{x0 + 60} {last_cy} {x1 - 60} {MID_Y} {x1} {MID_Y}", edge_status(risk[risk_agents[-1]][0], output_status)))

    nodes = [
        svg_node(ANALYSTS_X, top, ANALYSTS_W, NODE_H, COMPONENTS[key], steps[key])
        for key, top in zip(["fundamentals", "social", "news", "market"], ROWS)
    ]
    nodes.append(svg_node(TRADER_X, TRADER_Y, TRADER_W, TRADER_H, "Trader", steps["trading"]))
    nodes += [
        svg_node(RISK_X, top, RISK_W, NODE_H, RISK_AGENTS[agent], risk[agent][0])
        for agent, top in zip(risk_agents, ROWS)
    ]
    nodes.append(svg_node(OUTPUT_X, TRADER_Y, OUTPUT_W, TRADER_H, "Ordre", output_status, "output", output_label))

    done = sum(status in ("done", "skipped") for status in steps.values())
    logs = "".join(f"<div>&gt; {line}</div>" for line in state["logs"][-3:]) or "<div>&gt; En attente d'une analyse…</div>"
    return f"""
<div class="tr-panel">
<div class="tr-panel-top"><span>TR / PIPELINE DES AGENTS · {stock_symbol or "—"}</span><span>{done:02d} — {len(steps):02d}</span></div>
<svg class="tr-graph" viewBox="0 0 1200 410" aria-label="Graphe des agents">
<defs>{markers}<pattern id="tr-grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#729284" stroke-opacity=".12" stroke-width=".6"/></pattern></defs>
<rect x="-30" y="-20" width="1260" height="450" fill="url(#tr-grid)"/>
<rect class="group" x="{RISK_X - 18}" y="14" width="{RISK_W + 36}" height="{ROWS[-1] + NODE_H + 18 - 14}"/>
<text class="col-label" x="{ANALYSTS_X}" y="34">01 · ANALYSTES</text>
<text class="col-label" x="{TRADER_X}" y="{TRADER_Y - 16}">02 · TRADER</text>
<text class="col-label" x="{RISK_X}" y="34">03 · ÉQUIPE RISQUE</text>
<text class="col-label" x="{OUTPUT_X}" y="{TRADER_Y - 16}">04 · SORTIE</text>
<text class="edge-label" x="{(ANALYSTS_X + ANALYSTS_W + TRADER_X) / 2}" y="{ROWS[-1] + NODE_H + 30}" text-anchor="middle">RAPPORTS D'ANALYSE</text>
<text class="edge-label" x="{(TRADER_X + TRADER_W + RISK_X) / 2}" y="{MID_Y + 40}" text-anchor="middle">ORDRE PROPOSÉ</text>
<text class="edge-label" x="{(RISK_X + RISK_W + OUTPUT_X) / 2}" y="{MID_Y + 72}" text-anchor="middle">VERDICT</text>
{"".join(edges)}
{"".join(nodes)}
</svg>
<div class="tr-ticker">{logs}</div>
</div>
""".replace("\n", "")


# --- Graphiques -----------------------------------------------------------

def style_fig(fig, height):
    fig.update_layout(
        height=height,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="IBM Plex Sans, Arial, sans-serif", color=INK, size=12),
        showlegend=False,
        hoverlabel=dict(bgcolor=FOREST, font_color="#fff", font_family="IBM Plex Mono"),
    )
    fig.update_xaxes(gridcolor=LINE, zeroline=False, linecolor=LINE)
    fig.update_yaxes(gridcolor=LINE, zeroline=False, linecolor=LINE)
    return fig


def plot(fig):
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


def trade_ladder(order, current_price):
    entry, stop, target = order.get("entry_price"), order.get("stop_loss"), order.get("target_price")
    if not all(isinstance(v, (int, float)) for v in (entry, stop, target)):
        return None
    fig = go.Figure()
    fig.add_shape(type="rect", x0=stop, x1=entry, y0=-0.18, y1=0.18, fillcolor="#f3ddd4", line_width=0)
    fig.add_shape(type="rect", x0=entry, x1=target, y0=-0.18, y1=0.18, fillcolor=SAGE, line_width=0)
    points = [("Stop-loss", stop, NEGATIVE), ("Entrée", entry, FOREST), ("Objectif", target, MOSS)]
    if isinstance(current_price, (int, float)) and current_price != entry:
        points.append(("Cours", current_price, INK))
    for label, value, color in points:
        fig.add_trace(go.Scatter(
            x=[value], y=[0], mode="markers+text",
            marker=dict(size=16, color=color, symbol="line-ns", line=dict(width=3, color=color)),
            text=[f"{label}<br><b>${value:,.2f}</b>"], textposition="top center",
            textfont=dict(size=11, color=color), hovertemplate=f"{label}: $%{{x:,.2f}}<extra></extra>",
        ))
    span = abs(target - stop) or 1
    fig.update_yaxes(visible=False, range=[-0.6, 1.1])
    fig.update_xaxes(range=[min(stop, target) - span * 0.12, max(stop, target) + span * 0.12], tickprefix="$", showgrid=False)
    return style_fig(fig, 170)


def price_chart(market_data, period):
    prices = market_data.get("historical_data", {}).get(period, [])
    if not prices:
        return None
    x = list(range(len(prices)))
    indicators = market_data.get("technical_indicators", {})
    fig = go.Figure()
    upper, lower = indicators.get("bollinger_upper"), indicators.get("bollinger_lower")
    if upper and lower:
        fig.add_hrect(y0=lower, y1=upper, fillcolor=CARD, line_width=0, layer="below")
    fig.add_trace(go.Scatter(
        x=x, y=prices, mode="lines+markers", line=dict(color=FOREST, width=2.5, shape="spline"),
        marker=dict(size=7, color=PAPER, line=dict(color=FOREST, width=2)),
        fill="tozeroy", fillcolor="rgba(211,230,191,0.35)", hovertemplate="$%{y:,.2f}<extra></extra>",
    ))
    for key, label, color in [("sma_20", "SMA 20", MOSS), ("sma_50", "SMA 50", "#a5b89a"), ("sma_200", "SMA 200", "#b6bdb3")]:
        value = indicators.get(key)
        if value and min(prices) * 0.97 <= value <= max(prices) * 1.03:
            fig.add_hline(y=value, line=dict(color=color, width=1, dash="dot"),
                          annotation_text=label, annotation_position="top left", annotation_font=dict(size=10, color=color))
    low, high = min(prices), max(prices)
    margin = (high - low) * 0.25 or high * 0.02
    fig.update_yaxes(range=[low - margin, high + margin], tickprefix="$")
    fig.update_xaxes(showticklabels=False, showgrid=False)
    return style_fig(fig, 300)


def rsi_gauge(rsi):
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=rsi, number=dict(font=dict(size=34, color=INK)),
        gauge=dict(
            axis=dict(range=[0, 100], tickcolor=LINE, tickfont=dict(size=10, color=MUTED)),
            bar=dict(color=FOREST, thickness=0.28), bgcolor=CARD, borderwidth=0,
            steps=[dict(range=[0, 30], color="#e9ede2"), dict(range=[70, 100], color="#f3ddd4")],
        ),
    ))
    return style_fig(fig, 190)


def ratings_bar(ratings):
    labels = [("buy", "Achat", FOREST), ("hold", "Neutre", "#a5b89a"), ("sell", "Vente", NEGATIVE)]
    fig = go.Figure()
    for key, label, color in labels:
        value = ratings.get(key, 0)
        fig.add_trace(go.Bar(
            y=[""], x=[value], orientation="h", marker_color=color, name=label,
            text=[f"{label} {value}"], textposition="inside", insidetextanchor="middle",
            textfont=dict(color="#fff" if color != "#a5b89a" else FOREST, size=12),
            hovertemplate=f"{label}: %{{x}}<extra></extra>",
        ))
    fig.update_layout(barmode="stack")
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return style_fig(fig, 70)


def portfolio_donut(assets: dict, cash: float, title: str):
    labels = [*assets.keys(), "Liquidités"]
    values = [*assets.values(), cash]
    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.68, sort=False,
        marker=dict(colors=[*PALETTE[: len(assets)], CARD], line=dict(color=PAPER, width=2)),
        textinfo="label+percent", textfont=dict(size=11), hovertemplate="%{label}: $%{value:,.0f}<extra></extra>",
    ))
    fig.add_annotation(text=f"<span style='font-size:10px;color:{MUTED}'>{title}</span><br>${sum(values):,.0f}",
                       showarrow=False, font=dict(size=16, color=INK))
    return style_fig(fig, 260)


def sentiment_counts(data):
    """Compte récursivement les valeurs des clés 'sentiment' dans les données brutes."""
    counts = {}

    def walk(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "sentiment" and isinstance(value, str):
                    counts[value.lower()] = counts.get(value.lower(), 0) + 1
                else:
                    walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(parse_json(data))
    return counts


def sentiment_bar(counts):
    colors = {"positive": FOREST, "neutral": "#a5b89a", "negative": NEGATIVE}
    labels = {"positive": "Positif", "neutral": "Neutre", "negative": "Négatif"}
    fig = go.Figure()
    for key in ["positive", "neutral", "negative", *[k for k in counts if k not in colors]]:
        if key in counts:
            fig.add_trace(go.Bar(
                y=[""], x=[counts[key]], orientation="h", marker_color=colors.get(key, MUTED),
                text=[f"{labels.get(key, key)} {counts[key]}"], textposition="inside", insidetextanchor="middle",
                textfont=dict(color="#fff" if key != "neutral" else FOREST),
                hovertemplate=f"{labels.get(key, key)}: %{{x}}<extra></extra>",
            ))
    fig.update_layout(barmode="stack")
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return style_fig(fig, 70)


# --- Sections de résultats ------------------------------------------------

def tiles(items):
    cells = "".join(
        f'<div class="tr-tile" style="animation-delay:{i * 70}ms"><div class="label">{label}</div>'
        f'<div class="value">{value}</div><div class="sub">{sub}</div></div>'
        for i, (label, value, sub) in enumerate(items)
    )
    html(f'<div class="tr-tiles">{cells}</div>')


def analysis_text(data):
    text = data.get("analysis", "") if isinstance(data, dict) else data
    if text:
        st.markdown(dedent(text))


def show_decision(stock_symbol, results, portfolio, state):
    recommendation = results.get("recommendation")
    if not isinstance(recommendation, dict):
        analysis_text(recommendation)
        return
    order = recommendation.get("order") or {}
    status = recommendation.get("status")
    market_data = parse_json((results.get("raw_data") or {}).get("market")) or {}
    current_price = (market_data.get("price_data") or {}).get("current_price") if isinstance(market_data, dict) else None

    left, right = st.columns([1, 1.1], gap="large")
    with left:
        html(f'<div class="tr-eyebrow">Décision · {stock_symbol}</div>')
        if order:
            action = str(order.get("action", "")).upper()
            html(f'<div class="tr-decision">{ACTION_LABELS.get(action, action)} <em>{order.get("asset", stock_symbol)}</em></div>')
        else:
            html('<div class="tr-decision">Aucun <em>ordre</em></div>')
        if status == "approved_by_risk":
            html('<span class="tr-pill ok">● Validé par l\'équipe risque</span>')
        elif status == "rejected_by_risk":
            html('<span class="tr-pill ko">● Rejeté par l\'équipe risque</span>')
        else:
            html('<span class="tr-pill neutral">● Non soumis au risque</span>')

        if order:
            entry, stop, target = order.get("entry_price"), order.get("stop_loss"), order.get("target_price")
            upside = rr = "—"
            try:
                upside = f"{(target - entry) / entry:+.1%}"
                rr = f"{abs(target - entry) / abs(entry - stop):.1f}×"
            except (TypeError, ZeroDivisionError):
                pass
            horizon = order.get("time_horizon_days")
            tiles([
                ("Montant", money(order.get("notional_amount")), f"{order.get('notional_amount', 0) / portfolio['total_value']:.0%} du portefeuille" if portfolio else ""),
                ("Objectif", money(target, 2), upside),
                ("Ratio gain / risque", rr, f"Horizon {horizon} j" if horizon else ""),
            ])
    with right:
        if order:
            fig = trade_ladder(order, current_price)
            if fig:
                plot(fig)
        checks = []
        for agent, label in RISK_AGENTS.items():
            agent_status, reason = state["risk"][agent]
            css, mark = {"done": ("", "✓"), "rejected": ("ko", "✕")}.get(agent_status, ("idle", "·"))
            checks.append(
                f'<div class="tr-check {css}"><span class="mark">{mark}</span><div>'
                f'<div class="title">{label}</div><div class="reason">{reason or "Non évalué"}</div></div></div>'
            )
        html(f'<div class="tr-eyebrow" style="margin-top:12px">Contrôles de risque</div><div class="tr-checks">{"".join(checks)}</div>')

    text = recommendation.get("recommendation")
    if text:
        with st.expander("Lire la justification du trader"):
            st.markdown(dedent(text))


def show_market(results):
    market_data = parse_json((results.get("raw_data") or {}).get("market"))
    if isinstance(market_data, dict):
        price = market_data.get("price_data", {})
        current, previous = price.get("current_price"), price.get("previous_close")
        change = f"{(current - previous) / previous:+.2%} sur la séance" if current and previous else ""
        tiles([
            ("Cours", money(current, 2), change),
            ("Volume", f"{price.get('volume', 0) / 1e6:,.1f} M", "titres échangés"),
            ("P/E", price.get("pe_ratio", "—"), f"BPA {price.get('eps', '—')}"),
            ("Bêta", price.get("beta", "—"), "sensibilité au marché"),
        ])
        st.write("")
        historical = market_data.get("historical_data", {})
        if historical:
            col_chart, col_side = st.columns([2.2, 1], gap="large")
            with col_chart:
                periods = list(historical.keys())
                period = st.segmented_control("Période", periods, default=periods[-1], key="period") or periods[-1]
                fig = price_chart(market_data, period)
                if fig:
                    plot(fig)
            with col_side:
                rsi = market_data.get("technical_indicators", {}).get("rsi_14")
                if rsi is not None:
                    html('<div class="tr-eyebrow">RSI 14</div>')
                    plot(rsi_gauge(rsi))
                ratings = market_data.get("market_sentiment", {}).get("analyst_ratings")
                if ratings:
                    html('<div class="tr-eyebrow">Avis des analystes</div>')
                    plot(ratings_bar(ratings))
    html('<div class="tr-eyebrow" style="margin:24px 0 8px">Analyse du marché</div>')
    analysis_text(results.get("market"))


def show_fundamentals(results):
    raw = parse_json(((results.get("raw_data") or {}).get("fundamentals") or {}).get("fundamentals_data"))
    if isinstance(raw, dict):
        company = raw.get("company_info", {})
        data = raw.get("fundamentals_data", raw)
        if company.get("name"):
            html(f'<div class="tr-company">{company.get("name")} · {company.get("sector", "")} · {company.get("industry", "")}</div>')
        if isinstance(data, dict):
            tiles([
                ("Capitalisation", f"${data.get('market_cap', 0) / 1e12:,.2f} T" if data.get("market_cap") else "—", ""),
                ("Marge nette", pct(data.get("profit_margin")), f"Opérationnelle {pct(data.get('operating_margin'))}"),
                ("ROE", pct(data.get("return_on_equity")), f"ROA {pct(data.get('return_on_assets'))}"),
                ("Dette / capitaux", data.get("debt_to_equity", "—"), f"Ratio courant {data.get('current_ratio', '—')}"),
                ("Croissance CA", pct(data.get("revenue_growth")), f"Bénéfices {pct(data.get('earnings_growth'))}"),
            ])
            st.write("")
    analysis_text(results.get("fundamentals"))


def show_sentiment(results, key):
    counts = sentiment_counts((results.get("raw_data") or {}).get(key))
    if counts:
        html('<div class="tr-eyebrow">Répartition du sentiment</div>')
        plot(sentiment_bar(counts))
    analysis_text(results.get(key))


def show_portfolio(results, portfolio):
    if not portfolio:
        st.info("Portefeuille indisponible.")
        return
    assets = dict(portfolio.get("invested_assets", {}))
    cash = portfolio.get("cash", 0)
    recommendation = results.get("recommendation") if isinstance(results.get("recommendation"), dict) else {}
    order = recommendation.get("order") or {}
    tiles([
        ("Valeur totale", money(portfolio.get("total_value")), ""),
        ("Liquidités", money(cash), ""),
        ("Investi", money(portfolio.get("invested_value")), f"{len(assets)} positions"),
    ])
    col_before, col_after = st.columns(2)
    with col_before:
        plot(portfolio_donut(assets, cash, "AVANT"))
    with col_after:
        if order and recommendation.get("status") == "approved_by_risk":
            amount = order.get("notional_amount", 0)
            sign = -1 if str(order.get("action")).upper() == "SELL" else 1
            after = dict(assets)
            after[order["asset"]] = after.get(order["asset"], 0) + sign * amount
            plot(portfolio_donut(after, cash - sign * amount, "APRÈS L'ORDRE"))
        else:
            html(f'<div class="tr-prose" style="padding-top:110px;text-align:center;color:{MUTED}">Aucun ordre validé : le portefeuille reste inchangé.</div>')


def show_raw(results):
    raw_data = results.get("raw_data", {})
    for key, label in COMPONENTS.items():
        if key in raw_data:
            with st.expander(label):
                data = raw_data[key]
                if isinstance(data, dict):
                    data = {k: parse_json(v) for k, v in data.items()}
                st.json(parse_json(data), expanded=False)


# --- Page -----------------------------------------------------------------

def main():
    st.set_page_config(page_title="Trail Research — Hedge Fund LLM", page_icon="📈", layout="wide")
    st.markdown(CSS, unsafe_allow_html=True)
    html(f"""
<div class="tr-header">
<span class="tr-brand">{logo_svg()}<span>trail <span class="light">research</span><span class="period">.</span></span></span>
<span class="tr-header-tag">HEDGE FUND LLM · DESK MULTI-AGENTS</span>
</div>
""")

    hero_left, hero_right = st.columns([1.25, 1], gap="large", vertical_alignment="bottom")
    with hero_left:
        html("""
<div class="tr-eyebrow">Intelligence de marché</div>
<div class="tr-hero-title">Neuf agents. <em>Une décision.</em></div>
<div class="tr-hero-text">Fondamentaux, marché, actualités et réseaux sociaux sont analysés par des agents LLM spécialisés, puis un trader propose un ordre que l'équipe risque valide ou rejette.</div>
""")
    with hero_right:
        stock_symbol = DEMO_SYMBOL
        symbol_badge = f'<div class="tr-symbol"><span>{DEMO_SYMBOL}</span>Apple Inc.</div>'
        if PUBLIC_DEMO:
            html(symbol_badge)
            use_test_data = {key: True for key in COMPONENTS}
            footnote = "Démo sur données simulées."
        else:
            col_symbol, col_sources = st.columns([1.3, 1])
            with col_symbol:
                html(symbol_badge)
            with col_sources:
                with st.popover("Sources", width="stretch"):
                    st.caption("Cochées : données simulées. Décochées : APIs réelles (clés requises dans .env).")
                    use_test_data = {key: st.checkbox(label, value=True, key=f"test_{key}") for key, label in COMPONENTS.items()}
            footnote = "Mode démo par défaut : aucune clé API nécessaire."
        launch = st.button("Lancer l'analyse  ↗", type="primary", width="stretch")
        html(f'<div class="tr-footnote" style="margin-top:14px"><b>+</b>{footnote}</div>')

    panel = st.empty()
    saved = st.session_state.get("result")
    if saved:
        panel.markdown(pipeline_html(saved["symbol"], saved["state"]), unsafe_allow_html=True)
    else:
        panel.markdown(pipeline_html(stock_symbol, initial_state()), unsafe_allow_html=True)

    if launch:
        st.session_state.pop("result", None)
        results, portfolio, state = run_live(stock_symbol, use_test_data, panel)
        st.session_state["result"] = {"symbol": stock_symbol, "results": results, "portfolio": portfolio, "state": state}

    saved = st.session_state.get("result")
    if not saved:
        return

    results, portfolio, state, symbol = saved["results"], saved["portfolio"], saved["state"], saved["symbol"]
    html('<div class="tr-section"></div>')
    if "error" in results:
        st.error(results["error"])
    else:
        show_decision(symbol, results, portfolio, state)
        st.write("")
        tabs = st.tabs(["Marché", "Fondamentaux", "Actualités", "Réseaux sociaux", "Portefeuille", "Données brutes"])
        with tabs[0]:
            show_market(results)
        with tabs[1]:
            show_fundamentals(results)
        with tabs[2]:
            show_sentiment(results, "news")
        with tabs[3]:
            show_sentiment(results, "social")
        with tabs[4]:
            show_portfolio(results, portfolio)
        with tabs[5]:
            show_raw(results)

    with st.expander("Journal d'exécution"):
        st.code("\n".join(state["logs"]) or "(vide)", language="text")


if __name__ == "__main__":
    main()
