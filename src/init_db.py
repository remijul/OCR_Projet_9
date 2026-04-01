"""
Script d'initialisation de la base de données SQLite
=====================================================

Ce script :
1. Crée la base de données lapage.db
2. Crée les tables (transactions, products, kpis_cache)
3. Importe les données depuis le CSV

Usage : python src/init_db.py (depuis OCR_Projet_9/)
"""

import sqlite3
import csv
from pathlib import Path


def init_database():
    """Initialise la base de données SQLite."""
    
    # Chemins (depuis OCR_Projet_9/src/)
    project_root = Path(__file__).parent.parent
    db_path = project_root / "data" / "db" / "lapage.db"
    csv_path = project_root / "data" / "processed" / "transactions_enrichies.csv"
    
    # Créer le dossier data/db si nécessaire
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Supprimer la base existante
    if db_path.exists():
        db_path.unlink()
        print(f"🗑️  Base existante supprimée")
    
    # Connexion
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"📂 Création de la base : {db_path}")
    
    # =========================================================================
    # CRÉATION DES TABLES
    # =========================================================================
    
    # Table transactions
    cursor.execute("""
        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_prod TEXT,
            date TEXT,
            session_id TEXT,
            client_id TEXT,
            price REAL,
            categ TEXT,
            sex TEXT,
            birth INTEGER,
            segment_client TEXT,
            age_client INTEGER
        )
    """)
    print("✅ Table 'transactions' créée")
    
    # Table products (agrégée depuis transactions)
    cursor.execute("""
        CREATE TABLE products (
            id_prod TEXT PRIMARY KEY,
            categ TEXT,
            price_min REAL,
            price_max REAL,
            price_avg REAL,
            nb_ventes INTEGER
        )
    """)
    print("✅ Table 'products' créée")
    
    # Table kpis_cache (pour stocker les KPIs précalculés)
    cursor.execute("""
        CREATE TABLE kpis_cache (
            id INTEGER PRIMARY KEY,
            ca_total REAL,
            nb_transactions INTEGER,
            nb_clients INTEGER,
            nb_products INTEGER,
            panier_moyen REAL,
            date_min TEXT,
            date_max TEXT,
            updated_at TEXT
        )
    """)
    print("✅ Table 'kpis_cache' créée")
    
    # =========================================================================
    # IMPORT DES DONNÉES
    # =========================================================================
    
    if not csv_path.exists():
        print(f"⚠️  Fichier CSV non trouvé : {csv_path}")
        print("   Créez d'abord le fichier transactions_enrichies.csv")
        conn.close()
        return
    
    # Lire le CSV et insérer dans transactions
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        rows = []
        for row in reader:
            rows.append((
                row['id_prod'],
                row['date'],
                row['session_id'],
                row['client_id'],
                float(row['price']),
                row['categ'],
                row['sex'],
                int(row['birth']) if row['birth'] else None,
                row['segment_client'],
                int(row['age_client']) if row['age_client'] else None
            ))
        
        cursor.executemany("""
            INSERT INTO transactions 
            (id_prod, date, session_id, client_id, price, categ, sex, birth, segment_client, age_client)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, rows)
        
        print(f"✅ {len(rows):,} transactions importées")
    
    # =========================================================================
    # AGRÉGATION DES PRODUITS
    # =========================================================================
    
    cursor.execute("""
        INSERT INTO products (id_prod, categ, price_min, price_max, price_avg, nb_ventes)
        SELECT 
            id_prod,
            categ,
            MIN(price),
            MAX(price),
            AVG(price),
            COUNT(*)
        FROM transactions
        GROUP BY id_prod
    """)
    
    nb_products = cursor.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    print(f"✅ {nb_products:,} produits agrégés")
    
    # =========================================================================
    # CALCUL DES KPIS
    # =========================================================================
    
    cursor.execute("""
        INSERT INTO kpis_cache (id, ca_total, nb_transactions, nb_clients, nb_products, panier_moyen, date_min, date_max, updated_at)
        SELECT 
            1,
            SUM(price),
            COUNT(*),
            COUNT(DISTINCT client_id),
            COUNT(DISTINCT id_prod),
            AVG(price),
            MIN(date),
            MAX(date),
            datetime('now')
        FROM transactions
    """)
    print("✅ KPIs précalculés")
    
    # =========================================================================
    # INDEX POUR PERFORMANCE
    # =========================================================================
    
    cursor.execute("CREATE INDEX idx_transactions_client ON transactions(client_id)")
    cursor.execute("CREATE INDEX idx_transactions_categ ON transactions(categ)")
    cursor.execute("CREATE INDEX idx_transactions_date ON transactions(date)")
    cursor.execute("CREATE INDEX idx_products_categ ON products(categ)")
    print("✅ Index créés")
    
    # Commit et fermeture
    conn.commit()
    conn.close()
    
    print(f"\n🎉 Base de données initialisée avec succès !")
    print(f"   Chemin : {db_path}")


if __name__ == "__main__":
    init_database()