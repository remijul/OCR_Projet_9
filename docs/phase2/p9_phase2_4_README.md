# 🏪 Dashboard Lapage

Application Streamlit pour l'analyse des ventes de la librairie Lapage.

---

## 🚀 Installation

### Prérequis
- Python 3.9+
- pip

### Étapes

```bash
# 1. Cloner le projet (si pas déjà fait)
git clone <url_du_repo>
cd lapage_project

# 2. Créer un environnement virtuel
python -m venv venv

# 3. Activer l'environnement
# Windows :
venv\Scripts\activate
# Mac/Linux :
source venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt
```

---

## ▶️ Lancement

```bash
cd dashboard
streamlit run app.py
```

L'application s'ouvre sur `http://localhost:8501`

---

## 📁 Structure du projet

```
dashboard/
├── app.py                    # Point d'entrée
├── README.md                 # Ce fichier
├── pages/                    # Pages de l'application
│   ├── 1_📊_KPIs.py          # Indicateurs clés
│   ├── 2_📈_Evolution_CA.py  # Analyse temporelle
│   └── 3_🔍_Correlations.py  # Analyses bivariées
└── src/
    └── data_loader.py        # Chargement des données
```

---

## 📊 Pages disponibles

| Page | Description | Filtres |
|------|-------------|---------|
| **📊 KPIs** | Indicateurs clés, répartition CA | Période, Catégorie |
| **📈 Évolution CA** | Analyse temporelle, tendances | Catégorie, Granularité |
| **🔍 Corrélations** | Analyses bivariées | Type d'analyse |

---

## 🛠️ Technologies

| Outil | Version | Usage |
|-------|---------|-------|
| Streamlit | ≥1.30 | Framework web |
| Pandas | ≥2.0 | Manipulation données |
| Plotly | ≥5.18 | Graphiques interactifs |

---

## 📋 Données requises

L'application attend un fichier `transactions_enrichies.csv` dans :
```
data/processed/transactions_enrichies.csv
```

Colonnes attendues :
- `date` : Date de transaction
- `client_id` : Identifiant client
- `id_prod` : Identifiant produit
- `price` : Prix unitaire
- `categ` : Catégorie produit
- `sex` : Genre du client
- `birth` : Année de naissance

---

## 👥 Auteur

Projet P9 — OpenClassrooms