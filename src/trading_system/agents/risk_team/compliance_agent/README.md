# 🛡️ Rôle de l'Agent `AgentRiskCompliance`

## 🎯 Objectifs :
Cet agent sert à **appliquer des règles de conformité** pour gérer les risques du portefeuille. Il vérifie plusieurs critères avant d'accepter un ordre.

1. **📊 Limitation du pourcentage maximum par actif** :
   - Il vérifie que la part d'un actif dans le portefeuille ne dépasse pas un certain pourcentage (ex. 10% par actif).
   - Cela évite de concentrer trop de risques sur un seul actif.

2. **🏢 Limitation de l'exposition par secteur** :
   - Il vérifie que l'exposition à un secteur (par exemple, secteur technologique, crypto, etc.) ne dépasse pas un certain pourcentage (ex. 20% pour un secteur donné).

3. **📉 Vérification du levier** :
   - Il vérifie que l'effet de levier (le rapport entre la valeur investie et la valeur totale du portefeuille) ne dépasse pas une certaine limite (ex. 2x).
   - Cela permet de prévenir l'utilisation excessive de levier, qui peut entraîner des pertes importantes en cas de mouvement défavorable.

## 💡 Exemple de situation :
- Si un trader essaie d'acheter une action qui dépasserait le pourcentage maximum autorisé pour un actif (par exemple, si l'exposition à cet actif dépasse 10% du portefeuille), l'agent rejettera l'ordre et renverra un message d'erreur comme :
  > "Nouvelle exposition 15.00% > 10.00% max actif"

- Si l'ordre entraîne un levier trop élevé, par exemple 3x alors que la limite est 2x, l'agent rejettera l'ordre avec un message comme :
  > "Levier actuel 3.00x > 2.00x max"