"""
Module de connexion à la base de données
========================================

Utilitaire partagé pour tout le projet (API, dashboard, notebooks...).

Fournit la fonction get_db() pour obtenir une connexion SQLite.
"""

import sqlite3
from pathlib import Path

# Chemin vers la base de données
# Structure : OCR_Projet_9/src/database.py -> OCR_Projet_9/data/db/lapage.db
DB_PATH = Path(__file__).parent.parent / "data" / "db" / "lapage.db"


def get_db():
    """
    Retourne une connexion à la base SQLite.
    
    row_factory = sqlite3.Row permet d'accéder aux colonnes par nom.
    
    Usage:
        conn = get_db()
        cursor = conn.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        conn.close()
    """
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Base de données non trouvée : {DB_PATH}\n"
            "Exécutez 'python src/init_db.py' depuis la racine du projet."
        )
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn