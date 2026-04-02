# 📚 Projet P9 — Librairie Lapage

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.45-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![CI/CD](https://github.com/remijul/OCR_Projet_9/actions/workflows/ci.yml/badge.svg)](https://github.com/remijul/OCR_Projet_9/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Analyse des ventes et prévisions** pour la librairie en ligne Lapage  
> Projet de formation OpenClassrooms — Data Analyst & Développeur IA

---

## 🎯 Contexte

La librairie **Lapage** souhaite analyser ses données de ventes e-commerce (2 ans d'historique) pour :

- Comprendre les comportements d'achat clients
- Identifier les corrélations entre variables (catégories, segments, temporalité)
- Anticiper le chiffre d'affaires futur

Ce projet couvre l'ensemble du cycle de développement d'une application data/IA :

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   Phase 1         Phase 2         Phase 3         Phase 4         Phase 5  │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐   │
│  │ Jupyter │ ─► │Dashboard│ ─► │  CI/CD  │ ─► │   API   │ ─► │   ML    │   │
│  │ Analyse │    │Streamlit│    │  Tests  │    │ FastAPI │    │ SARIMA  │   │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘   │
│                                                                            │
│     📊              📱              🔄              🔌              🤖   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Structure du projet

```
OCR_Projet_9/
│
├── 📊 notebooks/                    # Phase 1 — Analyses Jupyter
│   ├── exploration.ipynb
│   ├── correlations.ipynb
│   ├── saisonnalite.ipynb
│   └── acp_lapage.ipynb
│
├── 📱 dashboard/                    # Phase 2 — Application Streamlit
│   ├── app.py                       # Point d'entrée
│   └── pages/
│       ├── 1_📊_KPIs.py
│       ├── 2_📈_Evolution_CA.py
│       ├── 3_🔍_Correlations.py
│       └── 4_🔮_Previsions_CA.py
│
├── 🔌 api/                          # Phase 4 — API REST
│   └── app/
│       ├── main.py
│       └── routers/
│           ├── kpis.py
│           ├── products.py
│           └── predictions.py       # Phase 5 — Endpoint ML
│
├── 🔧 src/                          # Code partagé
│   ├── data_loader.py
│   └── database.py
│
├── 📦 data/
│   ├── raw/                         # Données brutes
│   ├── processed/                   # Données nettoyées
│   │   └── transactions_enrichies.csv
│   ├── db/
│   │   └── lapage.db               # Base SQLite
│   └── models/saved/
│       └── best_model_sarima.pkl   # Modèle ML
│
├── 🧪 tests/                        # Phase 3 — Tests pytest
│   └── test_app.py
│
├── ⚙️ .github/workflows/            # Phase 3 — CI/CD
│   └── ci.yml
│
├── 📄 requirements.txt
└── 📄 README.md
```

---

## 🚀 Phases du projet

### Phase 1 — Analyses exploratoires 📊

> **Objectif** : Analyser les données de ventes pour identifier les insights business

| Analyse | Description | Notebook |
|---------|-------------|----------|
| Exploration | Statistiques descriptives, distributions | `exploration.ipynb` |
| Corrélations | Tests statistiques quali/quanti | `correlations.ipynb` |
| Saisonnalité | Décomposition temporelle | `saisonnalite.ipynb` |
| ACP | Analyse en composantes principales | `acp_lapage.ipynb` |

**Résultats clés** :
- Saisonnalité hebdomadaire marquée (pics le week-end)
- Corrélation significative entre catégorie et panier moyen
- 3 segments clients identifiés (VIP, Régulier, Occasionnel)

---

### Phase 2 — Dashboard Streamlit 📱

> **Objectif** : Créer une application web interactive pour le CODIR

```bash
# Lancement
cd dashboard
streamlit run app.py
```

**Fonctionnalités** :
- 📊 KPIs avec filtres dynamiques (période, catégorie, segment)
- 📈 Évolution temporelle du CA avec sélecteur de granularité
- 🔍 Analyses de corrélations interactives
- 🔮 Prévisions de CA (connecté à l'API)

**Accès** : http://localhost:8501

---

### Phase 3 — CI/CD & Tests 🔄

> **Objectif** : Industrialiser le projet avec tests et déploiement automatisé

```bash
# Exécuter les tests
pytest tests/ -v
```

**Pipeline CI/CD** (GitHub Actions) :
1. ✅ Installation des dépendances
2. ✅ Exécution des tests pytest
3. ✅ Vérification qualité code
4. ✅ Déploiement Streamlit Cloud (si tests OK)

**Couverture** : Tests unitaires sur `data_loader`, `database`, et endpoints API

---

### Phase 4 — API REST 🔌

> **Objectif** : Exposer les données via une API RESTful avec FastAPI

```bash
# Lancement
cd api
python -m uvicorn app.main:app --reload
```

**Endpoints disponibles** :

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Informations API |
| `/health` | GET | Health check (DB + modèle) |
| `/api/kpis` | GET | Indicateurs clés |
| `/api/products` | GET | Liste produits avec filtres |
| `/api/products/categories` | GET | Stats par catégorie |
| `/api/predict` | GET | Prévisions CA (Phase 5) |
| `/api/predict/info` | GET | Infos modèle ML |

**Documentation** : http://localhost:8000/docs (Swagger UI)

---

### Phase 5 — Modèle prédictif 🤖

> **Objectif** : Prédire le chiffre d'affaires avec un modèle SARIMA

**Modèle retenu** : `SARIMA(1, 0, 1)(1, 1, 1, 7)`

| Métrique | Valeur | Interprétation |
|----------|--------|----------------|
| **MAE** | 1 035 € | Erreur moyenne par jour |
| **RMSE** | 1 252 € | Erreur quadratique |
| **MAPE** | 6.37% | ~94% de précision |

**Comparaison des modèles testés** :

| Modèle | MAE | Verdict |
|--------|-----|---------|
| Baseline (MM7) | ~1 500€ | ❌ Trop simple |
| Holt-Winters | ~1 200€ | ⚠️ Correct |
| **SARIMA** | **1 035€** | ✅ **Meilleur** |
| Random Forest | ~1 100€ | ⚠️ Bon mais complexe |

**Usage API** :
```bash
curl "http://localhost:8000/api/predict?horizon_days=30"
```

---

## ⚙️ Installation

### Prérequis

- Python 3.12+
- Git

### Installation

```bash
# Cloner le repo
git clone https://github.com/remijul/OCR_Projet_9.git
cd OCR_Projet_9

# Créer et activer le venv
python -m venv venv
.\venv\Scripts\Activate      # Windows
source venv/bin/activate     # Linux/Mac

# Installer les dépendances
pip install -r requirements.txt
```

### Lancement rapide

```bash
# 1. Initialiser la base de données
python src/init_db.py

# 2. Entraîner le modèle (optionnel, .pkl fourni)
jupyter notebook notebooks/p9_phase5_demo_sarima.ipynb

# 3. Lancer l'API
cd api
python -m uvicorn app.main:app --reload

# 4. Lancer le dashboard (autre terminal)
cd dashboard
streamlit run app.py
```

---

## 🎓 Compétences REAC couvertes

Ce projet permet de valider les compétences suivantes du titre **Développeur en Intelligence Artificielle** :

### Bloc 1 — Données

| Code | Compétence | Phase |
|------|------------|-------|
| C4 | Créer une base de données dans le respect du RGPD | Phase 4 |
| C5 | Développer une API REST mettant à disposition les données | Phase 4 |

### Bloc 2 — Modèles IA

| Code | Compétence | Phase |
|------|------------|-------|
| C8 | Paramétrer un service d'intelligence artificielle | Phase 5 |
| C9 | Développer une API exposant un modèle d'IA | Phase 5 |

### Bloc 3 — Application IA

| Code | Compétence | Phase |
|------|------------|-------|
| C14 | Analyser le besoin d'application d'un commanditaire | Phase 2 |
| C15 | Concevoir le cadre technique d'une application | Phase 2 |
| C17 | Développer les composants et interfaces d'une application | Phase 2 |
| C18 | Automatiser les phases de tests via intégration continue | Phase 3 |
| C19 | Créer un processus de livraison continue | Phase 3 |

---

## 📊 Données

**Source** : `transactions_enrichies.csv`

| Colonne | Description |
|---------|-------------|
| `id_prod` | Identifiant produit |
| `date` | Date de transaction |
| `session_id` | Session de navigation |
| `client_id` | Identifiant client |
| `price` | Prix de la transaction |
| `categ` | Catégorie produit |
| `sex` | Genre du client |
| `birth` | Année de naissance |
| `segment_client` | Segment (VIP, Régulier, Occasionnel) |
| `age_client` | Âge calculé |

**Période** : Mars 2021 — Février 2023 (730 jours)

---

## 🛠️ Technologies

| Catégorie | Technologies |
|-----------|--------------|
| **Langages** | Python 3.12 |
| **Data** | Pandas, NumPy |
| **Visualisation** | Plotly, Seaborn, Matplotlib |
| **ML / Stats** | statsmodels (SARIMA), scikit-learn, SciPy |
| **Web Framework** | Streamlit, FastAPI |
| **Base de données** | SQLite |
| **Tests** | pytest |
| **CI/CD** | GitHub Actions, Streamlit Cloud |
| **Versioning** | Git, GitHub |

---

## 📝 Licence

Ce projet est sous licence MIT — voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 👤 Auteur

**Rémi Julien**  
Formation Développeur en Intelligence Artificielle — OpenClassrooms

🔗 Repository : [github.com/remijul/OCR_Projet_9](https://github.com/remijul/OCR_Projet_9)

---

<p align="center">
  <i>Projet réalisé dans le cadre de la formation OpenClassrooms</i><br>
  <b>🏪 Librairie Lapage — Analyse & Prévision des ventes</b>
</p>