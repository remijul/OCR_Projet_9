# FastAPI — Composants essentiels
## Aide-mémoire pour démarrer

---

## 🚀 Installation et lancement

```bash
# Installation
pip install fastapi uvicorn

# Lancer l'application
uvicorn main:app --reload

# L'API s'ouvre sur http://localhost:8000
# Documentation sur http://localhost:8000/docs
```

---

## 📝 Application minimale

```python
from fastapi import FastAPI

# Créer l'application
app = FastAPI()

# Premier endpoint
@app.get("/")
def accueil():
    return {"message": "Bienvenue sur l'API Lapage"}
```

**Résultat** : `GET http://localhost:8000/` → `{"message": "Bienvenue sur l'API Lapage"}`

---

## 🔧 Les décorateurs de route

```python
from fastapi import FastAPI

app = FastAPI()

# GET - Lire des données
@app.get("/api/produits")
def lister_produits():
    return [{"id": 1, "nom": "Livre A"}]

# GET avec paramètre dans l'URL
@app.get("/api/produits/{produit_id}")
def get_produit(produit_id: int):
    return {"id": produit_id, "nom": f"Produit {produit_id}"}

# POST - Créer des données
@app.post("/api/produits")
def creer_produit():
    return {"message": "Produit créé"}
```

---

## 📦 Paramètres de requête (Query Parameters)

```python
@app.get("/api/produits")
def lister_produits(limit: int = 10, categorie: str = None):
    """
    Exemples d'appels :
    - /api/produits              → limit=10, categorie=None
    - /api/produits?limit=5      → limit=5, categorie=None
    - /api/produits?categorie=0  → limit=10, categorie="0"
    """
    return {
        "limit": limit,
        "categorie": categorie
    }
```

---

## 🔗 Paramètres de chemin (Path Parameters)

```python
@app.get("/api/produits/{produit_id}")
def get_produit(produit_id: int):
    """
    Exemple : /api/produits/42 → produit_id=42
    """
    return {"id": produit_id}

@app.get("/api/categories/{categorie}/produits")
def produits_par_categorie(categorie: str):
    """
    Exemple : /api/categories/livres/produits
    """
    return {"categorie": categorie}
```

---

## 🗄️ Connexion SQLite (sans ORM)

```python
import sqlite3

def get_db():
    """Retourne une connexion à la base."""
    conn = sqlite3.connect("data/lapage.db")
    conn.row_factory = sqlite3.Row  # Accès par nom de colonne
    return conn

@app.get("/api/produits")
def lister_produits():
    conn = get_db()
    cursor = conn.execute("SELECT * FROM products LIMIT 10")
    produits = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return produits
```

---

## 📊 Exemple complet : endpoint KPIs

```python
@app.get("/api/kpis")
def get_kpis():
    """Retourne les indicateurs clés."""
    conn = get_db()
    
    # CA total
    ca = conn.execute("SELECT SUM(price) as total FROM transactions").fetchone()
    
    # Nombre de clients
    clients = conn.execute("SELECT COUNT(DISTINCT client_id) as nb FROM transactions").fetchone()
    
    # Panier moyen
    panier = conn.execute("SELECT AVG(price) as moyenne FROM transactions").fetchone()
    
    conn.close()
    
    return {
        "ca_total": round(ca["total"], 2),
        "nb_clients": clients["nb"],
        "panier_moyen": round(panier["moyenne"], 2)
    }
```

---

## ⚠️ Gestion des erreurs

```python
from fastapi import HTTPException

@app.get("/api/produits/{produit_id}")
def get_produit(produit_id: int):
    conn = get_db()
    produit = conn.execute(
        "SELECT * FROM products WHERE id = ?", 
        (produit_id,)
    ).fetchone()
    conn.close()
    
    if produit is None:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    
    return dict(produit)
```

---

## 📚 Documentation automatique

FastAPI génère automatiquement la documentation :

| URL | Interface |
|-----|-----------|
| `/docs` | Swagger UI (interactif) |
| `/redoc` | ReDoc (lecture) |
| `/openapi.json` | Spécification OpenAPI |

### Personnaliser la documentation

```python
app = FastAPI(
    title="API Lapage",
    description="API REST pour les données de la librairie Lapage",
    version="1.0.0"
)

@app.get("/api/kpis", summary="Obtenir les KPIs", tags=["KPIs"])
def get_kpis():
    """
    Retourne les indicateurs clés de performance :
    - CA total
    - Nombre de clients
    - Panier moyen
    """
    return {...}
```

---

## 🏷️ Organiser avec des tags

```python
@app.get("/api/kpis", tags=["KPIs"])
def get_kpis():
    ...

@app.get("/api/produits", tags=["Produits"])
def lister_produits():
    ...

@app.get("/api/produits/{id}", tags=["Produits"])
def get_produit(id: int):
    ...
```

**Résultat** : Dans Swagger UI, les endpoints sont groupés par tag.

---

## 🔄 Codes de réponse HTTP

| Code | Signification | Usage |
|------|---------------|-------|
| `200` | OK | Requête réussie |
| `201` | Created | Ressource créée (POST) |
| `400` | Bad Request | Paramètres invalides |
| `404` | Not Found | Ressource inexistante |
| `500` | Server Error | Erreur interne |

```python
from fastapi import HTTPException

# Retourner une erreur 404
raise HTTPException(status_code=404, detail="Non trouvé")

# Retourner une erreur 400
raise HTTPException(status_code=400, detail="Paramètre invalide")
```

---

## 📁 Structure recommandée (simple)

```
api/
├── main.py              # Application FastAPI
├── database.py          # Connexion SQLite
├── data/
│   └── lapage.db        # Base de données
└── requirements.txt
```

---

## 🎯 Pattern typique d'une API

```python
from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI(title="API Lapage", version="1.0.0")

def get_db():
    conn = sqlite3.connect("data/lapage.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def root():
    return {"message": "API Lapage", "version": "1.0.0"}

@app.get("/api/kpis", tags=["KPIs"])
def get_kpis():
    conn = get_db()
    # ... requêtes SQL ...
    conn.close()
    return {"ca_total": ..., "nb_clients": ...}

@app.get("/api/produits", tags=["Produits"])
def lister_produits(limit: int = 10):
    conn = get_db()
    cursor = conn.execute("SELECT * FROM products LIMIT ?", (limit,))
    produits = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return produits
```

---

## 📚 Ressources officielles

| Ressource | URL |
|-----------|-----|
| **Documentation** | https://fastapi.tiangolo.com |
| **Tutorial** | https://fastapi.tiangolo.com/tutorial/ |
| **SQLite Python** | https://docs.python.org/3/library/sqlite3.html |