# 📈 Comprendre SARIMA
## Modèle de prévision — Projet P9 Lapage

---

## 🎯 Pourquoi SARIMA ?

### Contexte Lapage

Nos données de CA présentent :
- Une **tendance** (évolution globale)
- Une **saisonnalité hebdomadaire** (patterns qui se répètent chaque semaine)
- Du **bruit** (variations aléatoires)

**SARIMA** est conçu exactement pour ce type de données !

---

## 📚 De ARIMA à SARIMA

### ARIMA : la base

> **A**uto**R**egressive **I**ntegrated **M**oving **A**verage

| Composante | Signification | Rôle |
|------------|---------------|------|
| **AR** (AutoRegressive) | p | Utilise les valeurs passées |
| **I** (Integrated) | d | Différenciation pour stationnarité |
| **MA** (Moving Average) | q | Utilise les erreurs passées |

**Notation** : ARIMA(p, d, q)

### SARIMA : ARIMA + Saisonnalité

> **S**easonal **ARIMA**

Ajoute une composante saisonnière : **(P, D, Q, s)**

**Notation complète** : SARIMA(p, d, q)(P, D, Q, s)

---

## 🔢 Décomposition des paramètres

### Notre modèle : SARIMA(1, 0, 1)(1, 1, 1, 7)

```
         Non-saisonnier        Saisonnier
         ─────────────         ──────────
              │                     │
        SARIMA(1, 0, 1)      (1, 1, 1, 7)
               │ │ │          │ │ │  │
               p d q          P D Q  s
```

| Paramètre | Valeur | Signification |
|-----------|--------|---------------|
| **p = 1** | AR(1) | Dépend de la valeur d'hier |
| **d = 0** | Pas de différenciation | Données déjà stationnaires |
| **q = 1** | MA(1) | Dépend de l'erreur d'hier |
| **P = 1** | SAR(1) | Dépend de la valeur il y a 7 jours |
| **D = 1** | Différenciation saisonnière | Enlève le pattern hebdo |
| **Q = 1** | SMA(1) | Dépend de l'erreur il y a 7 jours |
| **s = 7** | Période = 7 | Saisonnalité hebdomadaire |

---

## 🧮 L'équation (simplifiée)

### Idée intuitive

```
CA_aujourd'hui = f(CA_hier, CA_semaine_dernière, erreurs_passées) + bruit
```

### Formulation mathématique

$$y_t = c + \phi_1 y_{t-1} + \Phi_1 y_{t-7} + \theta_1 \epsilon_{t-1} + \Theta_1 \epsilon_{t-7} + \epsilon_t$$

| Symbole | Signification |
|---------|---------------|
| $y_t$ | CA du jour t |
| $c$ | Constante |
| $\phi_1$ | Coefficient AR (influence d'hier) |
| $\Phi_1$ | Coefficient SAR (influence semaine dernière) |
| $\theta_1$ | Coefficient MA (erreur d'hier) |
| $\Theta_1$ | Coefficient SMA (erreur semaine dernière) |
| $\epsilon_t$ | Bruit aléatoire |

---

## 📊 Visualisation des composantes

```
        CA journalier = Tendance + Saisonnalité + Résidus
        
   CA │    
      │   ╱╲    ╱╲    ╱╲    ╱╲         Série observée
      │  ╱  ╲  ╱  ╲  ╱  ╲  ╱  ╲
      │ ╱    ╲╱    ╲╱    ╲╱    ╲
      └─────────────────────────── Temps
      
      =
      
   T  │                    ╱
      │              ╱╱╱╱╱           Tendance (croissance)
      │        ╱╱╱╱╱
      └─────────────────────────── 
      
      +
      
   S  │   ╱╲    ╱╲    ╱╲    ╱╲       Saisonnalité (hebdo)
      │  ╱  ╲  ╱  ╲  ╱  ╲  ╱  ╲
      │ ╱    ╲╱    ╲╱    ╲╱    ╲
      └───────────────────────────
           L  M  M  J  V  S  D
      
      +
      
   R  │  ╱╲╱╲                        Résidus (bruit)
      │     ╲╱╲╱╲╱╲
      └───────────────────────────
```

---

## 🔧 Implémentation Python

### Entraînement

```python
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Définir le modèle
model = SARIMAX(
    ts_train,                          # Série temporelle
    order=(1, 0, 1),                   # (p, d, q)
    seasonal_order=(1, 1, 1, 7),       # (P, D, Q, s)
    enforce_stationarity=False,
    enforce_invertibility=False
)

# Entraîner
model_fit = model.fit(disp=False)

# Afficher le résumé
print(model_fit.summary())
```

### Prédiction

```python
# Prédire les 30 prochains jours
predictions = model_fit.forecast(steps=30)

# Avec intervalle de confiance
pred_conf = model_fit.get_forecast(steps=30)
pred_mean = pred_conf.predicted_mean
pred_ci = pred_conf.conf_int(alpha=0.05)  # IC 95%
```

---

## 📏 Performances sur Lapage

### Métriques obtenues

| Métrique | Valeur | Interprétation |
|----------|--------|----------------|
| **MAE** | 1 035.61 € | Erreur moyenne ~1000€/jour |
| **RMSE** | 1 252.04 € | Erreur quadratique |
| **MAPE** | 6.37 % | **~94% de précision** ✅ |

### Comparaison avec les autres modèles

| Modèle | MAE | Verdict |
|--------|-----|---------|
| Baseline (MM7) | ~1 500 € | ❌ Trop simple |
| Holt-Winters | ~1 200 € | ⚠️ Correct |
| **SARIMA** | **1 035 €** | ✅ **Meilleur** |
| Random Forest | ~1 100 € | ⚠️ Bon mais complexe |

---

## 🔍 Diagnostics du modèle

### Ce qu'il faut vérifier

```python
# Graphiques de diagnostic
model_fit.plot_diagnostics(figsize=(12, 8))
```

| Graphique | Ce qu'on veut voir |
|-----------|-------------------|
| **Résidus** | Centrés autour de 0, pas de pattern |
| **Histogramme** | Distribution normale |
| **QQ-Plot** | Points alignés sur la diagonale |
| **Correlogramme** | Pas d'autocorrélation résiduelle |

---

## 💾 Sauvegarde et chargement

### Sauvegarder

```python
import pickle

model_data = {
    'model': model_fit,
    'order': (1, 0, 1),
    'seasonal_order': (1, 1, 1, 7),
    'last_date': ts_train.index[-1],
    'metrics': {'mae': 1035.61, 'rmse': 1252.04, 'mape': 6.37}
}

with open('data/models/saved/best_model_sarima.pkl', 'wb') as f:
    pickle.dump(model_data, f)
```

### Charger et prédire

```python
with open('data/models/saved/best_model_sarima.pkl', 'rb') as f:
    model_data = pickle.load(f)

model = model_data['model']
predictions = model.forecast(steps=30)
```

---

## ⚠️ Limites de SARIMA

| Limite | Description | Mitigation |
|--------|-------------|------------|
| **Linéarité** | Suppose des relations linéaires | Utiliser ensemble si nécessaire |
| **Stationnarité** | Nécessite données stationnaires | Différenciation (d, D) |
| **Horizons longs** | Incertitude croissante | Limiter à 30-60 jours |
| **Changements structurels** | Ne gère pas les ruptures | Réentraîner régulièrement |
| **Événements spéciaux** | Pas de gestion des fériés | Ajouter des régresseurs |

---

## 🆚 SARIMA vs Prophet

| Critère | SARIMA | Prophet |
|---------|--------|---------|
| **Installation** | ✅ Simple (statsmodels) | ⚠️ Complexe (CmdStan) |
| **Interprétabilité** | ✅ Paramètres explicites | ⚠️ Boîte plus noire |
| **Jours fériés** | ❌ Manuel | ✅ Intégré |
| **Tendances non-linéaires** | ❌ Non | ✅ Oui |
| **Performance Windows** | ✅ OK | ❌ Problématique |

**Notre choix** : SARIMA pour sa robustesse et sa simplicité de déploiement.

---

## 📝 Résumé

### SARIMA(1, 0, 1)(1, 1, 1, 7) — Notre modèle

| Aspect | Détail |
|--------|--------|
| **Type** | Série temporelle avec saisonnalité |
| **Saisonnalité** | Hebdomadaire (s=7) |
| **Précision** | MAPE ~6% |
| **Usage** | Prévision CA 30 jours |
| **Déploiement** | API endpoint `/api/predict` |

### Points clés à retenir

1. SARIMA = ARIMA + composante saisonnière
2. Les paramètres (p,d,q)(P,D,Q,s) capturent différents aspects
3. Saisonnalité s=7 pour données journalières avec pattern hebdo
4. Toujours vérifier les diagnostics des résidus
5. Réentraîner régulièrement avec les nouvelles données