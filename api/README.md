# 🔌 API Lapage

API REST pour les données de la librairie en ligne Lapage.

## 🚀 Installation

```bash
# Depuis la racine du projet OCR_Projet_9/

# Installer les dépendances en intégrant fastapi
pip install -r requirements.txt

# Initialiser la base de données
python src/init_db.py

# Lancer l'API
cd api
uvicorn app.main:app --reload
```

L'API est accessible sur `http://localhost:8000`

## 📚 Documentation

| URL | Description |
|-----|-------------|
| http://localhost:8000/docs | Swagger UI (interactif) |
| http://localhost:8000/redoc | ReDoc (documentation) |

## 🔗 Endpoints

### Info

| Endpoint | Description |
|----------|-------------|
| `GET /` | Informations sur l'API |
| `GET /health` | Health check |

### KPIs

| Endpoint | Description |
|----------|-------------|
| `GET /api/kpis` | Indicateurs clés (CA, clients, panier moyen) |

### Produits

| Endpoint | Description |
|----------|-------------|
| `GET /api/products` | Liste des produits avec stats |
| `GET /api/products/categories` | Liste des catégories |

## 📦 Exemples

### Obtenir les KPIs

```bash
# Linux/Mac
curl http://localhost:8000/api/kpis

# Windows PowerShell
Invoke-RestMethod http://localhost:8000/api/kpis
# ou depuis Windows +10 : curl.exe http://localhost:8000/api/kpis
```

```json
{
  "ca_total": 125000.50,
  "nb_transactions": 15000,
  "nb_clients": 2340,
  "nb_products": 1500,
  "panier_moyen": 53.42,
  "periode": {
    "debut": "2021-03-01",
    "fin": "2022-02-28"
  }
}
```

### Obtenir les produits

```bash
# Top 10 produits par ventes
curl "http://localhost:8000/api/products?limit=10"

# Produits de la catégorie 0
curl "http://localhost:8000/api/products?categ=0"

# Produits triés par prix moyen
curl "http://localhost:8000/api/products?sort_by=price_avg&order=desc"
```

## 📁 Structure du projet

```
OCR_Projet_9/
├── src/                         # Utilitaires partagés
│   ├── __init__.py
│   ├── database.py              # Connexion SQLite
│   └── init_db.py               # Script création BDD
├── data/
│   ├── db/
│   │   └── lapage.db            # Base SQLite (générée)
│   └── processed/
│       └── transactions_enrichies.csv
├── api/
│   ├── __init__.py
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # Point d'entrée FastAPI
│   │   └── routers/
│   │       ├── __init__.py
│   │       ├── kpis.py          # Endpoints /api/kpis
│   │       └── products.py      # Endpoints /api/products
│   └── README.md
├── dashboard/                   # Dashboard Streamlit
├── requirements.txt             # Dépendances du projet
└── ...
```

## 🗄️ Base de données

### Tables

| Table | Description |
|-------|-------------|
| `transactions` | Toutes les transactions |
| `products` | Produits agrégés (stats) |
| `kpis_cache` | KPIs précalculés |

### Schéma simplifié

```
transactions
├── id (PK)
├── id_prod
├── date
├── client_id
├── price
├── categ
├── sex
└── age_client

products
├── id_prod (PK)
├── categ
├── price_min / max / avg
└── nb_ventes
```

## 👥 Auteur

Projet P9 — OpenClassrooms — Développeur IA