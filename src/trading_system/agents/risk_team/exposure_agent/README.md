# 🛡️ Rôle de `AgentRiskExposure`

## 🎯 Objectif :
Limiter la taille d'une position sur **un seul actif** pour éviter de **trop se concentrer** sur un actif et **répartir les risques**.

---

## 🔍 Comment il fonctionne :

1. Il récupère :
    - Le **prix actuel** de l'actif (`current_price`),
    - La **valeur de l'ordre** (`asset_value`), soit :
        - Directement (`notional_amount`) **ou**
        - Prix actuel × quantité.

2. Il récupère aussi :
    - La **valeur totale** du portefeuille (`total_value`),
    - L'**exposition actuelle** sur cet actif (`invested_assets`).

3. Il calcule :
   - Le **nouveau pourcentage d'exposition** après l'ordre.

4. Il compare ce pourcentage à une limite fixée (max_exposure_per_asset, par défaut 10%).

## 🚨 Si dépassement :

- L'agent rejette l'ordre et donne un message du type :

> "Exceeds exposure limit for AAPL (12.3% > 10.0%)"

## ✅ Sinon :

- L'ordre passe avec un message "Exposure OK".


> 👉 Pourquoi c'est important ?
> Pour éviter qu'un seul trade représente une trop grosse partie du portefeuille (et donc éviter de tout perdre si cet actif
s'effondre).