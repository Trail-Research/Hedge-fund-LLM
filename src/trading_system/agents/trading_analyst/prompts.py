TRADING_RECOMMENDATION_PROMPT = """
En tant qu'analyste de trading expert, sur la base des analyses suivantes, fournissez une recommandation détaillée :

Analyse des fondamentaux :
{fundamentals_analysis}

Analyse du sentiment social :
{social_analysis}

Analyse des actualités :
{news_analysis}

Analyse des tendances du marché :
{market_analysis}

Veuillez fournir une recommandation structurée avec :
1. Synthèse des points clés de chaque analyse
2. Recommandation d'action (Acheter/Vendre/Conserver) avec justification
3. Niveau de confiance (1-10) et facteurs de risque
4. Points d'entrée/sortie recommandés
5. Horizon temporel recommandé et objectifs de prix
""" 