"""
API Lapage — Point d'entrée
===========================

API REST exposant les données de la librairie Lapage.

Lancer avec : uvicorn app.main:app --reload (depuis api/)
Documentation : http://localhost:8000/docs
"""

# =============================================================================
# CONFIGURATION DU PATH (pour accéder à src/ depuis api/)
# =============================================================================
import sys
from pathlib import Path

# Ajouter la racine du projet au PYTHONPATH
PROJECT_ROOT = Path(__file__).parent.parent.parent  # api/app/main.py -> OCR_Projet_9/
sys.path.insert(0, str(PROJECT_ROOT))

# =============================================================================
# IMPORTS
# =============================================================================
from fastapi import FastAPI
from src.database import get_db
from app.routers import kpis, products

# =============================================================================
# CRÉATION DE L'APPLICATION
# =============================================================================

app = FastAPI(
    title="API Lapage",
    description="API REST pour les données de la librairie en ligne Lapage",
    version="1.0.0"
)

# =============================================================================
# ENREGISTREMENT DES ROUTERS
# =============================================================================

app.include_router(kpis.router)
app.include_router(products.router)


# =============================================================================
# ENDPOINTS RACINE
# =============================================================================

@app.get("/", tags=["Info"])
def root():
    """
    Point d'entrée de l'API.
    Retourne les informations de base et la liste des endpoints.
    """
    return {
        "api": "Lapage",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "kpis": "/api/kpis",
            "products": "/api/products",
            "categories": "/api/products/categories"
        }
    }


@app.get("/health", tags=["Info"])
def health_check():
    """
    Vérifie que l'API et la base de données fonctionnent.
    Utile pour le monitoring et les health checks de déploiement.
    """
    try:
        conn = get_db()
        conn.execute("SELECT 1")
        conn.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}