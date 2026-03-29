# 🏪 Dashboard Lapage

Dashboard Streamlit pour l'analyse des ventes de la librairie Lapage.

## 🚀 Lancement

```bash
# Depuis le dossier OCR_Projet_9/
cd dashboard
streamlit run app.py
```

L'application s'ouvre sur http://localhost:8501

## 📁 Structure

```
OCR_Projet_9/
├── dashboard/
│   ├── app.py                    # Page d'accueil
│   └── pages/
│       ├── 1_📊_KPIs.py          # Indicateurs clés
│       ├── 2_📈_Evolution_CA.py  # Analyse temporelle
│       └── 3_🔍_Correlations.py  # Analyses bivariées
├── src/
│   └── data_loader.py            # Chargement données
└── data/
    └── processed/
        └── transactions_enrichies.csv
```

## 📊 Pages

| Page | Fonctionnalités |
|------|-----------------|
| **KPIs** | CA, transactions, clients + filtres période/catégorie/segment |
| **Évolution CA** | Graphique temporel, moyenne mobile, comparaison catégories |
| **Corrélations** | Genre×Catégorie, Âge×Montant, Catégorie×Prix |

## 🛠️ Dépendances

```
streamlit>=1.30.0
pandas>=2.0.0
plotly>=5.18.0
```

## 👥 Auteur

Projet P9 — OpenClassrooms