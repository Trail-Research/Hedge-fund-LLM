from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

class LLMManager:
    def __init__(self):
        # Configuration des modèles Groq
        # Utilisation de llama3-8b-8192 pour tous les modèles car c'est le plus stable
        self.model = ChatGroq(
            model_name="llama3-8b-8192",
            temperature=0.7,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

    def analyze_fundamentals(self, fundamentals_data: dict, company_info: dict) -> str:
        """
        Analyse les données fondamentales de l'entreprise.
        """
        prompt = f"""
        En tant qu'analyste financier expert, analysez les données fondamentales suivantes et fournissez une évaluation détaillée :
        
        Données fondamentales :
        {fundamentals_data}
        
        Informations sur l'entreprise :
        {company_info}
        
        Veuillez fournir une analyse structurée avec :
        1. Analyse des ratios financiers clés et leur signification
        2. Évaluation de la santé financière (solvabilité, liquidité, rentabilité)
        3. Points forts et faibles de l'entreprise
        4. Recommandations d'amélioration et risques potentiels
        """
        
        response = self.model.invoke(prompt)
        return response.content

    def analyze_social_sentiment(self, social_data: dict) -> str:
        """
        Analyse le sentiment des discussions sur les réseaux sociaux.
        """
        prompt = f"""
        En tant qu'analyste de sentiment expert, analysez les discussions suivantes sur les réseaux sociaux :
        
        {social_data}
        
        Veuillez fournir une analyse structurée avec :
        1. Analyse du sentiment général (positif/négatif/neutre) avec pourcentage
        2. Thèmes principaux discutés et leur importance
        3. Préoccupations majeures des investisseurs
        4. Niveau d'engagement et influence potentielle sur le marché
        """
        
        response = self.model.invoke(prompt)
        return response.content

    def analyze_news(self, news_data: dict) -> str:
        """
        Analyse les actualités récentes.
        """
        prompt = f"""
        En tant qu'analyste de marché expert, analysez les actualités suivantes :
        
        {news_data}
        
        Veuillez fournir une analyse structurée avec :
        1. Événements majeurs et leur importance
        2. Impact potentiel sur l'entreprise (court/moyen/long terme)
        3. Tendances émergentes dans le secteur
        4. Risques identifiés et opportunités potentielles
        """
        
        response = self.model.invoke(prompt)
        return response.content

    def analyze_market_trends(self, market_data: dict) -> str:
        """
        Analyse les tendances du marché.
        """
        prompt = f"""
        En tant qu'analyste technique expert, analysez les tendances du marché suivantes :
        
        {market_data}
        
        Veuillez fournir une analyse structurée avec :
        1. Tendances principales (court/moyen/long terme)
        2. Indicateurs techniques clés et leur interprétation
        3. Niveaux de support/résistance importants
        4. Scénarios possibles et probabilités associées
        """
        
        response = self.model.invoke(prompt)
        return response.content

    def generate_trading_recommendation(self, all_analysis: dict) -> str:
        """
        Génère une recommandation de trading basée sur toutes les analyses.
        """
        prompt = f"""
        En tant qu'analyste de trading expert, sur la base des analyses suivantes, fournissez une recommandation détaillée :
        
        Analyse des fondamentaux :
        {all_analysis.get('fundamentals', 'N/A')}
        
        Analyse du sentiment social :
        {all_analysis.get('social', 'N/A')}
        
        Analyse des actualités :
        {all_analysis.get('news', 'N/A')}
        
        Analyse des tendances du marché :
        {all_analysis.get('market', 'N/A')}
        
        Veuillez fournir une recommandation structurée avec :
        1. Synthèse des points clés de chaque analyse
        2. Recommandation d'action (Acheter/Vendre/Conserver) avec justification
        3. Niveau de confiance (1-10) et facteurs de risque
        4. Points d'entrée/sortie recommandés
        5. Horizon temporel recommandé et objectifs de prix
        """
        
        response = self.model.invoke(prompt)
        return response.content 