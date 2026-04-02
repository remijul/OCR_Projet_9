# 🤖 Phase 5 — Introduction au Machine Learning
## Projet P9 — Librairie Lapage

---

## 📍 Positionnement de la Phase 5

```
Phase 1          Phase 2          Phase 3          Phase 4          Phase 5
Analyses    →    Dashboard   →    CI/CD       →    API REST    →    ML & Prédiction
Notebooks        Streamlit        Tests            FastAPI          SARIMA
                                  GitHub Actions   SQLite           Forecast
```

**Objectif** : Ajouter de l'**intelligence prédictive** à notre système d'analyse.

---

## 🎯 Machine Learning : À quoi ça sert ?

### Définition

> Le Machine Learning permet à un système d'**apprendre des patterns** à partir de données historiques pour **faire des prédictions** sur de nouvelles données.

### Applications métier

| Domaine | Application | Exemple Lapage |
|---------|-------------|----------------|
| **Prévision** | Anticiper des valeurs futures | Prévoir le CA des 30 prochains jours |
| **Classification** | Catégoriser des éléments | Segmenter les clients (VIP, occasionnel) |
| **Recommandation** | Suggérer des items pertinents | "Vous aimerez aussi..." |
| **Détection d'anomalies** | Identifier les comportements inhabituels | Fraude, pic de ventes anormal |

---

## 🔄 Comment ça marche ?

### Le principe fondamental

```
                    ENTRAÎNEMENT
    ┌─────────────────────────────────────┐
    │                                     │
    │   Données      →    Algorithme      │
    │   historiques       (apprend)       │
    │                                     │
    └─────────────────────────────────────┘
                         │
                         ▼
                      MODÈLE
                    (patterns appris)
                         │
                         ▼
    ┌─────────────────────────────────────┐
    │                                     │
    │   Nouvelles    →    Prédictions     │
    │   données                           │
    │                                     │
    └─────────────────────────────────────┘
                    INFÉRENCE
```

---

## 📊 Les deux grandes familles

### Apprentissage supervisé

> On fournit les **réponses** (labels) à l'algorithme pendant l'entraînement.

| Type | Description | Exemples |
|------|-------------|----------|
| **Régression** | Prédire une valeur numérique | CA, prix, température |
| **Classification** | Prédire une catégorie | Spam/non-spam, client fidèle/churner |

**Algorithmes courants** :
- Régression linéaire, Ridge, Lasso
- Random Forest, Gradient Boosting
- SVM, Réseaux de neurones

### Apprentissage non supervisé

> Pas de labels. L'algorithme découvre des **structures cachées**.

| Type | Description | Exemples |
|------|-------------|----------|
| **Clustering** | Regrouper des éléments similaires | Segmentation clients |
| **Réduction de dimension** | Simplifier les données | ACP, t-SNE |
| **Détection d'anomalies** | Identifier les outliers | Fraude |

**Algorithmes courants** :
- K-Means, DBSCAN, Hierarchical Clustering
- PCA, t-SNE, UMAP

---

## 🔮 Cas particulier : Les séries temporelles

### Définition

> Une **série temporelle** est une séquence de données indexées par le temps.

### Caractéristiques

| Composante | Description | Exemple Lapage |
|------------|-------------|----------------|
| **Tendance** | Évolution long terme | CA en hausse sur 2 ans |
| **Saisonnalité** | Patterns récurrents | Pics le week-end, creux en été |
| **Bruit** | Variations aléatoires | Fluctuations quotidiennes |

### Modèles spécialisés

| Modèle | Description |
|--------|-------------|
| **ARIMA/SARIMA** | Modèle statistique classique avec saisonnalité |
| **Prophet** | Développé par Meta, gère bien les jours fériés |
| **Holt-Winters** | Lissage exponentiel avec tendance et saisonnalité |
| **LSTM** | Réseau de neurones récurrent (Deep Learning) |

---

## 🔧 Le processus ML complet

```
┌─────────┐    ┌──────────┐    ┌─────────────┐    ┌────────────┐
│  DATA   │ → │ FEATURES │ → │ PREPROCESS  │ → │ TRAIN/TEST │
│         │    │          │    │             │    │   SPLIT    │
└─────────┘    └──────────┘    └─────────────┘    └────────────┘
     │              │                │                  │
  Collecte    Ingénierie      Normalisation        80% / 20%
  Nettoyage   Sélection       Encoding             Validation
                              Imputation           croisée
                                                        │
                                                        ▼
┌─────────────┐    ┌────────────┐    ┌─────────────────────────┐
│ DÉPLOIEMENT │ ← │ ÉVALUATION │ ← │     ENTRAÎNEMENT        │
│             │    │            │    │                         │
└─────────────┘    └────────────┘    └─────────────────────────┘
      │                 │                      │
   API REST        MAE, RMSE             Ajustement
   Monitoring      MAPE, R²              des poids
   MLOps           Confusion Matrix      Optimisation
```

---

## 📋 Étape par étape

### 1. Collecte & Nettoyage des données

```python
# Charger les transactions
df = pd.read_csv('transactions_enrichies.csv')

# Agréger par jour
df_daily = df.groupby('date').agg(ca=('price', 'sum'))
```

### 2. Feature Engineering

```python
# Créer des features temporelles
df['dayofweek'] = df['date'].dt.dayofweek
df['month'] = df['date'].dt.month
df['is_weekend'] = df['dayofweek'] >= 5
df['lag_7'] = df['ca'].shift(7)  # CA il y a 7 jours
```

### 3. Préparation des données

```python
# Gérer les valeurs manquantes
df = df.fillna(method='ffill')

# Normaliser si nécessaire
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

### 4. Split Train/Test

```python
# 80% train, 20% test (respecter l'ordre temporel !)
train = df.iloc[:-30]
test = df.iloc[-30:]
```

### 5. Entraînement

```python
# Entraîner le modèle
model = SARIMAX(train, order=(1,0,1), seasonal_order=(1,1,1,7))
model_fit = model.fit()
```

### 6. Évaluation

```python
# Calculer les métriques
predictions = model_fit.forecast(30)
mae = mean_absolute_error(test, predictions)
rmse = np.sqrt(mean_squared_error(test, predictions))
```

### 7. Déploiement

```python
# Sauvegarder
pickle.dump(model_fit, open('model.pkl', 'wb'))

# Charger et prédire via API
@app.post("/api/predict")
def predict(horizon: int = 30):
    model = pickle.load(open('model.pkl', 'rb'))
    return model.forecast(horizon)
```

---

## 📏 Métriques d'évaluation

### Pour la régression / prévision

| Métrique | Formule | Interprétation |
|----------|---------|----------------|
| **MAE** | Moyenne des erreurs absolues | Erreur moyenne en € |
| **RMSE** | Racine de la moyenne des erreurs² | Pénalise les grosses erreurs |
| **MAPE** | Erreur en % de la valeur réelle | Interprétable (ex: 6% d'erreur) |

### Exemple Lapage (SARIMA)

| Métrique | Valeur | Interprétation |
|----------|--------|----------------|
| **MAE** | 1 035 € | Erreur moyenne de ~1000€/jour |
| **RMSE** | 1 252 € | Certains jours avec plus d'erreur |
| **MAPE** | 6.37% | Prévision à ~94% de précision |

---

## 🎓 Compétences développées

| Code | Compétence | Application Phase 5 |
|------|------------|---------------------|
| **C8** | Paramétrer un service d'IA | Configurer et optimiser SARIMA |
| **C9** | Développer une API exposant un modèle d'IA | Endpoint `/api/predict` |

---

## 📝 Résumé

| Concept | Description |
|---------|-------------|
| **ML** | Apprendre des patterns pour prédire |
| **Supervisé** | Avec labels (régression, classification) |
| **Non supervisé** | Sans labels (clustering) |
| **Séries temporelles** | Données indexées par le temps |
| **Process** | Data → Features → Train → Eval → Deploy |
| **Métriques** | MAE, RMSE, MAPE |

**Notre choix pour Lapage** : SARIMA — modèle statistique robuste pour les séries temporelles avec saisonnalité hebdomadaire.