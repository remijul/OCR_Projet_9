"""
Router KPIs
===========

Endpoints pour les indicateurs clés de performance.
"""

from fastapi import APIRouter
from src.database import get_db

# Création du router
router = APIRouter(
    prefix="/api/kpis",
    tags=["KPIs"]
)


@router.get("")
def get_kpis():
    """
    Retourne les indicateurs clés de performance.
    
    **Indicateurs retournés :**
    - ca_total : Chiffre d'affaires total (€)
    - nb_transactions : Nombre de transactions
    - nb_clients : Nombre de clients uniques
    - nb_products : Nombre de produits distincts
    - panier_moyen : Panier moyen (€)
    - periode : Dates min et max des données
    """
    conn = get_db()
    
    try:
        # Récupérer les KPIs précalculés
        row = conn.execute("SELECT * FROM kpis_cache WHERE id = 1").fetchone()
        
        if row is None:
            # Calculer à la volée si pas de cache
            row = conn.execute("""
                SELECT 
                    SUM(price) as ca_total,
                    COUNT(*) as nb_transactions,
                    COUNT(DISTINCT client_id) as nb_clients,
                    COUNT(DISTINCT id_prod) as nb_products,
                    AVG(price) as panier_moyen,
                    MIN(date) as date_min,
                    MAX(date) as date_max
                FROM transactions
            """).fetchone()
        
        return {
            "ca_total": round(row["ca_total"], 2),
            "nb_transactions": row["nb_transactions"],
            "nb_clients": row["nb_clients"],
            "nb_products": row["nb_products"],
            "panier_moyen": round(row["panier_moyen"], 2),
            "periode": {
                "debut": row["date_min"][:10] if row["date_min"] else None,
                "fin": row["date_max"][:10] if row["date_max"] else None
            }
        }
    
    finally:
        conn.close()