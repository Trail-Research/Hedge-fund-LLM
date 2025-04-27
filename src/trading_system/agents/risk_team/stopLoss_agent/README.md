# 🛡️ Rôle de l'agent `AgentRiskStopLoss`

Il garantit que **chaque ordre est protégé par un stop-loss cohérent**.

Concrètement, il fait deux choses :

- **Si le trader n'a pas mis de stop-loss** :
  - ➔ Ton agent **en crée un automatiquement** basé sur un pourcentage par défaut (**exemple ici : 5% en dessous du prix actuel**).

- **Si un stop-loss est fourni** :
  - ➔ Ton agent **vérifie qu’il est correct**, c'est-à-dire **qu’il est en dessous du prix actuel** (logique : un stop-loss vend pour limiter une perte, donc il doit être sous le prix actuel).

# 📉 C’est quoi un stop-loss ?

Un **stop-loss** est une **protection automatique** que tu places sur un trade pour **limiter tes pertes**.

- ➔ **Si le prix tombe** jusqu'à un certain niveau que tu as défini (= ton stop-loss),
- ➔ **Ton trade est automatiquement vendu** (ou clôturé) pour t’éviter de perdre encore plus.

## 🧠 Exemple concret :

- Tu achètes une action à **100€**.
- Tu places un **stop-loss à 95€**.

👉 Si le prix descend à **95€ ou moins**, ton broker vend automatiquement ta position.  
Donc ta perte maximale est limitée à **5€ par action**.

## 🎯 Pourquoi c’est super important ?

- **Éviter des grosses pertes** quand le marché bouge très vite contre toi.
- **Trader de façon disciplinée** sans émotions ("peur", "espoir", etc.).
- **Protéger ton capital** pour pouvoir durer longtemps sur les marchés.

## 🛠️ Techniquement :

- **Ordre stop-loss** = **ordre de vente conditionnel**.
- Tu dis à ton système : **"Vends immédiatement si le prix touche X"**.