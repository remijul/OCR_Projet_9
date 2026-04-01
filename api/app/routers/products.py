"""
Router Produits
===============

Endpoints pour les produits et catégories.
"""

from fastapi import APIRouter, Query
from src.database import get_db

# Création du router
router = APIRouter(
    prefix="/api/products",
    tags=["Produits"]
)


@router.get("")
def get_products(
    limit: int = Query(default=50, ge=1, le=500, description="Nombre max de produits"),
    categ: str = Query(default=None, description="Filtrer par catégorie"),
    sort_by: str = Query(default="nb_ventes", description="Tri : nb_ventes, price_avg"),
    order: str = Query(default="desc", description="Ordre : asc, desc")
):
    """
    Retourne la liste des produits avec leurs statistiques.
    
    **Paramètres :**
    - limit : Nombre maximum de produits (1-500, défaut: 50)
    - categ : Filtrer par catégorie (optionnel)
    - sort_by : Colonne de tri (nb_ventes ou price_avg)
    - order : Ordre de tri (asc ou desc)
    
    **Données retournées par produit :**
    - id_prod : Identifiant du produit
    - categ : Catégorie
    - price_min, price_max, price_avg : Statistiques de prix
    - nb_ventes : Nombre de ventes
    """
    conn = get_db()
    
    try:
        # Construction de la requête
        query = "SELECT * FROM products"
        params = []
        
        # Filtre catégorie
        if categ:
            query += " WHERE categ = ?"
            params.append(categ)
        
        # Tri (sécurisé contre injection SQL)
        sort_column = "nb_ventes" if sort_by not in ["nb_ventes", "price_avg"] else sort_by
        sort_order = "DESC" if order.lower() != "asc" else "ASC"
        query += f" ORDER BY {sort_column} {sort_order}"
        
        # Limite
        query += " LIMIT ?"
        params.append(limit)
        
        # Exécution
        cursor = conn.execute(query, params)
        products = []
        
        for row in cursor.fetchall():
            products.append({
                "id_prod": row["id_prod"],
                "categ": row["categ"],
                "price_min": round(row["price_min"], 2),
                "price_max": round(row["price_max"], 2),
                "price_avg": round(row["price_avg"], 2),
                "nb_ventes": row["nb_ventes"]
            })
        
        return {
            "count": len(products),
            "products": products
        }
    
    finally:
        conn.close()


@router.get("/categories")
def get_categories():
    """
    Retourne la liste des catégories avec leurs statistiques.
    
    **Données retournées par catégorie :**
    - categ : Identifiant de la catégorie
    - nb_products : Nombre de produits
    - total_ventes : Nombre total de ventes
    - prix_moyen : Prix moyen des produits
    """
    conn = get_db()
    
    try:
        cursor = conn.execute("""
            SELECT 
                categ,
                COUNT(*) as nb_products,
                SUM(nb_ventes) as total_ventes,
                AVG(price_avg) as prix_moyen
            FROM products
            GROUP BY categ
            ORDER BY total_ventes DESC
        """)
        
        categories = []
        for row in cursor.fetchall():
            categories.append({
                "categ": row["categ"],
                "nb_products": row["nb_products"],
                "total_ventes": row["total_ventes"],
                "prix_moyen": round(row["prix_moyen"], 2)
            })
        
        return {"categories": categories}
    
    finally:
        conn.close()