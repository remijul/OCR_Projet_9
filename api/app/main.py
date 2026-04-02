"""
API Lapage — Point d'entrée principal
=====================================

API REST pour l'accès aux données et prédictions de la librairie Lapage.

Endpoints disponibles :
- /api/kpis : Indicateurs clés de performance
- /api/products : Liste des produits et catégories
- /api/predict : Prévisions de CA (SARIMA)

Usage :
    cd api
    uvicorn app.main:app --reload
"""

import sys
from pathlib import Path

# Ajouter la racine du projet au PYTHONPATH
# Cela permet d'importer depuis src/ et app/
PROJECT_ROOT = Path(__file__).parent.parent.parent  # api/app/main.py -> OCR_Projet_9
sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import des routers
from app.routers import kpis, products, predictions


# Création de l'application
app = FastAPI(
    title="API Lapage",
    description="""
## API de la librairie Lapage

Cette API expose les données de ventes et les prédictions de CA.

### Endpoints disponibles

- **KPIs** (`/api/kpis`) : Indicateurs clés de performance
- **Produits** (`/api/products`) : Catalogue et statistiques produits
- **Prédictions** (`/api/predict`) : Prévisions de CA (modèle SARIMA)

### Documentation

- Swagger UI : `/docs`
- ReDoc : `/redoc`
    """,
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# Configuration CORS pour permettre l'accès depuis Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",      # Streamlit local
        "http://127.0.0.1:8501",
        "https://*.streamlit.app",    # Streamlit Cloud
        "*"                           # Dev : tout autoriser
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Inclusion des routers
app.include_router(kpis.router)
app.include_router(products.router)
app.include_router(predictions.router)


@app.get("/", tags=["Info"])
def root():
    """
    Point d'entrée de l'API.
    
    Retourne les informations de base et les endpoints disponibles.
    """
    return {
        "api": "Lapage",
        "version": "2.0.0",
        "description": "API de la librairie Lapage - Données et prédictions",
        "endpoints": {
            "kpis": "/api/kpis",
            "products": "/api/products",
            "categories": "/api/products/categories",
            "predict": "/api/predict",
            "model_info": "/api/predict/info"
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }


@app.get("/health", tags=["Info"])
def health_check():
    """
    Vérification de l'état de l'API.
    
    Utilisé pour le monitoring et les health checks.
    """
    # Vérifier la connexion DB
    try:
        from src.database import get_db
        conn = get_db()
        conn.execute("SELECT 1")
        conn.close()
        db_status = "ok"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    # Vérifier le modèle
    model_path = PROJECT_ROOT / "data" / "models" / "saved" / "best_model_sarima.pkl"
    model_status = "ok" if model_path.exists() else "not_found"
    
    return {
        "status": "healthy" if db_status == "ok" else "degraded",
        "database": db_status,
        "model": model_status,
        "version": "2.0.0"
    }