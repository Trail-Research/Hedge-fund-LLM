# 🏦 Hedge Fund LLM - Système de Trading Multi-Agents

<div align="center">

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

*Un système de trading automatisé basé sur des agents LLM spécialisés pour l'analyse financière et la gestion de risques*

</div>

## 📋 Table des Matières

- [🎯 Vue d'ensemble](#-vue-densemble)
- [🏗️ Architecture](#️-architecture)
- [✨ Fonctionnalités](#-fonctionnalités)
- [🚀 Installation](#-installation)
- [💡 Utilisation](#-utilisation)
- [🤖 Agents Spécialisés](#-agents-spécialisés)
- [🛡️ Gestion des Risques](#️-gestion-des-risques)
- [📊 Sources de Données](#-sources-de-données)
- [🔧 Configuration](#-configuration)
- [📈 Exemple d'Analyse](#-exemple-danalyse)
- [🤝 Contribution](#-contribution)
- [📜 Licence](#-licence)

## 🎯 Vue d'ensemble

**Hedge Fund LLM** est un système de trading automatisé sophistiqué qui utilise une architecture multi-agents basée sur des Large Language Models (LLM) pour analyser les marchés financiers et générer des recommandations de trading. Ce projet s'inspire des recherches récentes en IA financière, notamment l'article ["Multi-Agent LLM Framework for Hedge Fund Trading"](https://arxiv.org/pdf/2412.20138).

Le système combine plusieurs types d'analyses financières :
- **Analyse fondamentale** : Ratios financiers, bilans, performances
- **Analyse technique** : Indicateurs de marché, tendances, niveaux de support/résistance
- **Analyse des actualités** : Impact des événements sur les prix
- **Analyse des médias sociaux** : Sentiment des investisseurs sur Reddit et Twitter/X
- **Gestion des risques** : Validation et contrôle des ordres de trading

## 🏗️ Architecture

Le système utilise une architecture modulaire avec un orchestrateur central qui coordonne plusieurs agents spécialisés :

```
TradingOrchestrator
├── FundamentalsAnalyst     # Analyse des données financières
├── MarketAnalyst          # Analyse technique et tendances
├── NewsAnalyst            # Analyse des actualités
├── SocialMediaAnalyst     # Sentiment des réseaux sociaux
├── TradingAnalyst         # Génération des recommandations
└── RiskManagementPipeline # Validation et contrôle des risques
    ├── ExposureAgent      # Contrôle de l'exposition par actif
    ├── MarketConditionsAgent # Validation des conditions de marché
    ├── StopLossAgent      # Gestion automatique des stop-loss
    └── ComplianceAgent    # Règles de conformité
```

## ✨ Fonctionnalités

### 🔍 Analyse Multi-Sources
- **Données fondamentales** via Financial Modeling Prep API
- **Données de marché** via Yahoo Finance
- **Actualités financières** via Finnhub API
- **Médias sociaux** via Reddit (PRAW) et Twitter/X APIs
- **Analyse de sentiment** intégrée

### 🧠 Intelligence Artificielle
- **Agents LLM spécialisés** utilisant Groq/Llama3
- **Prompts optimisés** pour chaque type d'analyse
- **Synthèse intelligente** des données multi-sources
- **Recommandations argumentées** avec niveaux de confiance

### 🛡️ Gestion des Risques
- **Contrôle d'exposition** par actif (limite par défaut : 40%)
- **Validation des conditions de marché** (volatilité, spread)
- **Stop-loss automatiques** (5% par défaut)
- **Règles de conformité** (secteurs, levier)

### 📊 Données Temps Réel
- **Prix en temps réel** et données historiques
- **Indicateurs techniques** (RSI, MACD, Bollinger Bands)
- **Sentiment de marché** agrégé
- **Actualités récentes** et leur impact

## 🚀 Installation

### Prérequis
- Python 3.8+
- Clés API pour les services externes (voir [Configuration](#-configuration))

### Installation des dépendances

```bash
# Cloner le repository
git clone https://github.com/Trail-Research/Hedge-fund-LLM.git
cd Hedge-fund-LLM

# Créer un environnement virtuel
python -m venv hedge-fund-env
source hedge-fund-env/bin/activate  # Linux/Mac
# ou
hedge-fund-env\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Installer le package en mode développement
pip install -e .
```

## 💡 Utilisation

### Utilisation Basique

```bash
# Analyser un symbole boursier
python main.py AAPL

# Exemples d'autres symboles
python main.py MSFT
python main.py GOOGL
python main.py TSLA
```

### Interface de Démo

```bash
streamlit run app.py
```

L'interface (charte graphique Trail Research) s'ouvre dans le navigateur : l'analyse porte sur AAPL (les données simulées ne couvrent qu'Apple) ; choisissez dans « Sources » entre données simulées (par défaut, aucune clé API requise) et APIs réelles, puis lancez l'analyse. Le pipeline des agents s'anime en direct, puis l'interface affiche la décision, le graphique entrée / stop-loss / objectif, le détail des contrôles de risque, des graphiques interactifs (cours, RSI, avis des analystes, sentiment), le portefeuille avant / après l'ordre, les données brutes et le journal d'exécution.

### Démo publique (https://trailresear.ch/demo/)

La démo publique est une page statique du site [trail-landing](https://github.com/Trail-Research/trail-landing) (`public/demo/`), qui rejoue une analyse en données simulées. Après une modification des agents ou des données simulées, régénérer ses données :

```bash
python scripts/export_demo_data.py > ../trail-landing/public/demo/data.js
```

### Utilisation Programmatique

```python
from trading_system.agents.trading_orchestrator import TradingOrchestrator

# Initialiser l'orchestrateur
orchestrator = TradingOrchestrator()

# Analyser un actif
results = orchestrator.analyze_stock("AAPL")

# Accéder aux résultats
print("Analyse fondamentale:", results['fundamentals'])
print("Recommandation:", results['recommendation'])
```

### Mode Test vs Production

```python
# Mode test (utilise des données simulées)
orchestrator = TradingOrchestrator(use_test_data={
    'fundamentals': True,
    'social': True,
    'news': True,
    'market': True,
    'trading': True
})

# Mode production (utilise les APIs réelles)
orchestrator = TradingOrchestrator(use_test_data={
    'fundamentals': False,
    'social': False,
    'news': False,
    'market': False,
    'trading': False
})
```

## 🤖 Agents Spécialisés

### 📊 FundamentalsAnalyst
- **Données analysées** : Ratios P/E, ROE, ROA, debt-to-equity, marges
- **Sources** : Financial Modeling Prep, Yahoo Finance
- **Sortie** : Évaluation de la santé financière et points forts/faibles

### 📈 MarketAnalyst
- **Données analysées** : Prix, volume, indicateurs techniques
- **Indicateurs** : RSI, MACD, Bollinger Bands, moyennes mobiles
- **Sortie** : Tendances et niveaux de support/résistance

### 📰 NewsAnalyst
- **Sources** : Finnhub API pour actualités financières
- **Analyse** : Impact des événements sur les prix
- **Sortie** : Sentiment des actualités et risques/opportunités

### 📱 SocialMediaAnalyst
- **Sources** : Reddit (r/stocks, r/investing, r/wallstreetbets), Twitter/X
- **Analyse** : Sentiment et engagement de la communauté
- **Sortie** : Score de sentiment et thèmes dominants

### 🎯 TradingAnalyst
- **Entrée** : Synthèse de toutes les analyses précédentes
- **Sortie** : Recommandation (BUY/SELL/HOLD) avec justification
- **Inclut** : Prix d'entrée, stop-loss, objectifs de prix

## 🛡️ Gestion des Risques

Le système intègre un pipeline de gestion des risques sophistiqué :

### 🎯 AgentRiskExposure
- **Objectif** : Limiter l'exposition par actif
- **Limite par défaut** : 40% du portefeuille par actif
- **Fonction** : Prévient la concentration excessive

### 🌡️ AgentRiskMarketConditions
- **Volatilité maximale** : 3% par défaut
- **Spread maximum** : 0.1% par défaut
- **Fonction** : Évite le trading en conditions de marché défavorables

### 🛑 AgentRiskStopLoss
- **Stop-loss automatique** : 5% par défaut
- **Validation** : Vérifie la cohérence des stop-loss manuels
- **Protection** : Limite les pertes sur chaque position

### ⚖️ AgentRiskCompliance
- **Limites par secteur** : Crypto 20%, Actions 80%
- **Levier maximum** : 2x par défaut
- **Conformité** : Applique les règles réglementaires

## 📊 Sources de Données

| Service | Type de données | API utilisée |
|---------|----------------|--------------|
| **Financial Modeling Prep** | Données fondamentales | REST API |
| **Yahoo Finance** | Prix et données historiques | yfinance |
| **Finnhub** | Actualités financières | REST API |
| **Reddit** | Discussions et sentiment | PRAW |
| **Twitter/X** | Tweets et engagement | Tweepy |
| **Groq** | Modèles LLM | Llama3-8B-8192 |

## 🔧 Configuration

### Variables d'environnement
Créez un fichier `.env` à la racine du projet :

```env
# APIs de données financières
FINN_API_KEY=your_financial_modeling_prep_key
FINNHUB_API_KEY=your_finnhub_key

# APIs réseaux sociaux
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_KEY=your_reddit_secret
X_BEARER_TOKEN=your_twitter_bearer_token
X_API_KEY=your_twitter_api_key
X_API_SECRET=your_twitter_api_secret
X_ACCESS_TOKEN=your_twitter_access_token
X_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret

# API LLM
GROQ_API_KEY=your_groq_api_key
```

### Obtention des clés API

1. **Financial Modeling Prep** : [financialmodelingprep.com](https://financialmodelingprep.com)
2. **Finnhub** : [finnhub.io](https://finnhub.io)
3. **Reddit** : [reddit.com/prefs/apps](https://reddit.com/prefs/apps)
4. **Twitter/X** : [developer.twitter.com](https://developer.twitter.com)
5. **Groq** : [console.groq.com](https://console.groq.com)

## 📈 Exemple d'Analyse

Voici un exemple de sortie pour l'analyse d'AAPL :

```
=== Starting analysis for AAPL ===

=== Fundamentals Analysis ===
Apple démontre une santé financière solide avec des marges robustes (25%) 
et des retours sur capitaux propres élevés (17%). Le ratio P/E de 28.5 
reflète une valorisation premium justifiée par la force de la marque...

=== Market Analysis ===
AAPL évolue au-dessus de ses moyennes mobiles clés (SMA 20 et 50), 
indiquant une tendance haussière à court terme. Le MACD positif 
confirme la dynamique...

=== Trading Recommendation ===
**Recommandation : ACHAT**
- Prix d'entrée : $175.84
- Stop-loss : $169.78 (50-day SMA)
- Objectif : $185.67 (+5.6%)
- Horizon : 6-12 mois
- Confiance : 8/10
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

1. **Fork** le repository
2. Créez une **branche feature** (`git checkout -b feature/nouvelle-fonctionnalite`)
3. **Committez** vos changements (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. **Push** vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créez une **Pull Request**

### Guidelines
- Utilisez des noms de variables/fonctions explicites
- Ajoutez des docstrings pour les nouvelles fonctions
- Testez vos modifications avant de soumettre
- Respectez le style de code existant

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

<div align="center">

**Développé par [Trail Research](https://github.com/Trail-Research)**

*Ce projet s'inspire des recherches en IA financière et vise à démocratiser l'accès aux outils de trading algorithmique.*

</div>