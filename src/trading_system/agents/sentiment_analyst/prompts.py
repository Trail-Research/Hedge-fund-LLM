SENTIMENT_ANALYSIS_PROMPT = """
En tant qu'analyste de sentiment expert, analysez les discussions suivantes sur les réseaux sociaux :

{social_data}

Veuillez fournir une analyse structurée avec :
1. Analyse du sentiment général (positif/négatif/neutre) avec pourcentage
2. Thèmes principaux discutés et leur importance
3. Préoccupations majeures des investisseurs
4. Niveau d'engagement et influence potentielle sur le marché
""" 