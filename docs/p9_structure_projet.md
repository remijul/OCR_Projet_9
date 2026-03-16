# P9 - Structure du projet

**Structure évolutive proposée :**

```
lapage_project/
│
├── README.md                    # Description projet, instructions
├── requirements.txt             # Dépendances Python (environnement)
├── .gitignore                   # Fichiers à ignorer (liste à définir)
│
├── .github/
│   └── workflows/
│       └── ci.yml           # Pipeline CI
│
├── data/                        # 📊 Données (toutes phases)
│   ├── raw/                     # Données brutes originales
│   │   ├── customers.csv
│   │   ├── products.csv
│   │   └── transactions.csv
│   └── processed/               # Données transformées
│       └── .gitkeep
│
├── notebooks/                   # 📓 Phase 1 - Analyses
│   ├── 01_exploration.ipynb
│   ├── 02_analyses_annabelle.ipynb
│   ├── 03_analyses_julie.ipynb
│   └── exports/                 # Exports HTML (si nécessaire)
│       └── .gitkeep
│
├── reports/                     # 📑 Phase 1 - Présentation
│   ├── presentation.pptx
│   └── figures/                 # Images pour PPT (si nécessaire)
│       └── .gitkeep
│
├── dashboard/                   # 📱 Phase 2 - Streamlit
│   ├── app.py                   # Point d'entrée
│   ├── pages/                   # Dashboard multi-pages
│   │   └── .gitkeep
│   └── components/              # Composants réutilisables (si nécessaire)
│       └── .gitkeep
│
├── src/                         # 🔧 Code réutilisable (toutes phases)
│   ├── __init__.py
│   ├── data_loader.py           # Chargement données
│   ├── analysis.py              # Fonctions d'analyse
│   ├── visualization.py         # Fonctions graphiques
│   └── statistics.py            # Tests statistiques
│
├── tests/                       # 🧪 Phase 3 - Tests
│   ├── __init__.py
│   └── .gitkeep
│
├── api/                         # 🔌 Phase 4 - FastAPI
│   └── .gitkeep
│
├── models/                      # 🤖 Phase 5 - ML
│   └── .gitkeep
│
└── docs/                        # 📚 Documentation
    ├── specifications.md        # Phase 2 - Specs
    └── .gitkeep
```
