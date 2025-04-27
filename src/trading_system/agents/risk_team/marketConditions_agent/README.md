# 📊 Rôle de `AgentRiskMarketConditions`

## 🎯 Objectif
Il vérifie que le marché est "calme" avant d'autoriser un ordre d'achat ou de vente.

Concrètement, il fait **deux contrôles principaux** :

---

## 1. 📈 Vérification de la volatilité

- Il récupère les **prix historiques** de l'actif sur **1 semaine** (`1w`).
- Il **calcule la volatilité** (en gros : est-ce que les prix ont beaucoup bougé cette semaine ?).
- **Si la volatilité est trop élevée** (par exemple, supérieure à **2%** si `max_volatility=0.02`), **l'ordre est rejeté**.

> 👉 **Pourquoi ?**  
> Si un actif est trop volatile, le risque de pertes est élevé.  
> L'agent protège donc contre des marchés **trop dangereux**.

---

## 2. 🔄 Vérification du spread (bid/ask)

- Il récupère :
  - le **prix bid** (meilleur prix pour vendre),
  - le **prix ask** (meilleur prix pour acheter).
- Il **calcule le spread** (la différence entre `ask` et `bid`).
- Il **mesure le spread en pourcentage** du prix moyen.
- **Si le spread est trop large** (exemple : plus de **0.05%** avec `max_spread=0.0005`), **l'ordre est aussi rejeté**.

> 👉 **Pourquoi ?**  
> Un grand spread = marché peu liquide = risque d'acheter trop cher ou de vendre trop bas.