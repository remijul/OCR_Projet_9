# Phase 4 — API REST
## Exposer ses données au monde

---

# 📍 Où en sommes-nous ?

```
Phase 1          Phase 2          Phase 3          Phase 4
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                                     
 📓 Notebooks  →  📱 Dashboard  →  🚀 CI/CD     →  🔌 API
 Analyses         App Streamlit    Tests/Deploy    Données exposées
   
 ✅ Terminé       ✅ Terminé       ✅ Terminé      📍 Vous êtes ici
```

**Changement de posture :**
- Phase 3 : **DevOps** → Automatiser, déployer
- Phase 4 : **Backend Developer** → Exposer les données via une API

---

# 🤔 C'est quoi une API ?

## API = Application Programming Interface

> Une **interface** qui permet à deux applications de **communiquer** entre elles.

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Client    │  ────▶  │    API      │  ────▶  │   Données   │
│  (App, Web) │  ◀────  │  (FastAPI)  │  ◀────  │   (SQLite)  │
└─────────────┘         └─────────────┘         └─────────────┘
     Requête               Traitement              Stockage
     Réponse
```

## Analogie : Le serveur au restaurant 🍽️

- **Vous** (client) → Passez commande
- **Serveur** (API) → Transmet à la cuisine, rapporte le plat
- **Cuisine** (base de données) → Prépare la commande

---

# 🌍 Pourquoi une API ?

## Le problème sans API

| Application | Accès aux données |
|-------------|-------------------|
| Dashboard Streamlit | Lit le CSV directement |
| App mobile | ❌ Comment accéder au CSV ? |
| Partenaire externe | ❌ Accès au serveur ? Sécurité ? |
| Autre équipe | ❌ Dépendance au format CSV |

## La solution avec API

| Application | Accès aux données |
|-------------|-------------------|
| Dashboard Streamlit | `GET /api/kpis` |
| App mobile | `GET /api/kpis` |
| Partenaire externe | `GET /api/kpis` (avec API key) |
| Autre équipe | `GET /api/kpis` |

**Une seule source de vérité, accessible partout.**

---

# 📡 Le standard REST

## REST = Representational State Transfer

Un **style d'architecture** pour concevoir des APIs web.

## Principes clés

| Principe | Description |
|----------|-------------|
| **Ressources** | Tout est une ressource (produits, clients, KPIs) |
| **URLs** | Chaque ressource a une URL unique |
| **Méthodes HTTP** | GET, POST, PUT, DELETE |
| **Sans état** | Chaque requête est indépendante |
| **Format standard** | JSON (généralement) |

---

# 🔧 Les méthodes HTTP

| Méthode | Action | Exemple |
|---------|--------|---------|
| **GET** | Lire | `GET /api/products` → Liste des produits |
| **POST** | Créer | `POST /api/products` → Nouveau produit |
| **PUT** | Modifier | `PUT /api/products/42` → Modifier produit 42 |
| **DELETE** | Supprimer | `DELETE /api/products/42` → Supprimer |

## Pour ce projet

On utilise principalement **GET** (lecture seule).

```
GET /api/kpis        → Récupérer les KPIs
GET /api/products    → Récupérer les produits
```

---

# 📦 Anatomie d'une requête/réponse

## Requête (Client → API)

```http
GET /api/kpis HTTP/1.1
Host: localhost:8000
Accept: application/json
```

## Réponse (API → Client)

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "ca_total": 125000,
  "nb_clients": 2340,
  "panier_moyen": 53.42
}
```

---

# ⚡ Pourquoi FastAPI ?

## Comparatif des frameworks Python

| Framework | Vitesse | Facilité | Doc auto | Typing |
|-----------|---------|----------|----------|--------|
| **Flask** | ⭐⭐ | ⭐⭐⭐ | ❌ | ❌ |
| **Django REST** | ⭐⭐ | ⭐⭐ | ⚠️ | ❌ |
| **FastAPI** | ⭐⭐⭐ | ⭐⭐⭐ | ✅ | ✅ |

## Avantages FastAPI

- **Rapide** : Performances comparables à Node.js/Go
- **Simple** : Peu de code pour beaucoup de fonctionnalités
- **Documentation auto** : Swagger UI généré automatiquement
- **Moderne** : Basé sur les standards Python récents

---

# ✅ Forces de FastAPI

| Force | Description |
|-------|-------------|
| **Performance** | Un des frameworks Python les plus rapides |
| **Documentation auto** | `/docs` → Swagger UI prêt à l'emploi |
| **Validation** | Vérification automatique des données |
| **Asynchrone** | Support natif de `async/await` |
| **Standards** | OpenAPI, JSON Schema |
| **Communauté** | Documentation excellente, adoption croissante |

---

# ⚠️ Limites de FastAPI

| Limite | Description |
|--------|-------------|
| **Jeune** | Moins mature que Flask/Django |
| **Écosystème** | Moins de plugins que Flask |
| **Courbe** | Concepts avancés (async, typing) |
| **Overkill** | Pour des APIs très simples |

## Pour ce projet

FastAPI est **idéal** : 
- API de taille moyenne
- Documentation automatique importante
- Apprentissage des bonnes pratiques

---

# 🎯 API dans un projet Data

## Cas d'usage typiques

| Cas | Description |
|-----|-------------|
| **Dashboard** | Le front-end appelle l'API pour les données |
| **Modèle ML** | API qui expose les prédictions |
| **ETL** | API pour déclencher des pipelines |
| **Partenaires** | Accès contrôlé aux données |

## Architecture moderne

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Frontend    │────▶│    API       │────▶│   Database   │
│  (React,     │◀────│  (FastAPI)   │◀────│   (SQLite)   │
│   Streamlit) │     │              │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │   Modèle ML  │
                     │   (optionnel)│
                     └──────────────┘
```

---

# 🎓 Compétences Développeur IA

## C4 — Créer une base de données

> *"Créer une base de données dans le respect du RGPD en élaborant les modèles conceptuels et physiques des données."*

**Ce que vous faites :**
- Créer la base SQLite
- Structurer les tables
- Documenter le schéma

---

# 🎓 Compétences Développeur IA

## C5 — Développer une API REST

> *"Développer une API mettant à disposition le jeu de données en utilisant l'architecture REST afin de permettre l'exploitation du jeu de données par les autres composants du projet."*

**Ce que vous faites :**
- Créer les endpoints FastAPI
- Exposer les données en JSON
- Documenter via Swagger

---

# 🛠️ Stack technique

| Composant | Technologie | Rôle |
|-----------|-------------|------|
| **Framework** | FastAPI | Serveur API |
| **Serveur** | Uvicorn | Exécution ASGI |
| **Base de données** | SQLite | Stockage |
| **Format** | JSON | Échange de données |
| **Documentation** | Swagger UI | Interface `/docs` |

## Installation

```bash
pip install fastapi uvicorn
```

## Lancement

```bash
uvicorn main:app --reload
```

---

# 🎯 Ce qu'on attend de vous

## Livrables

- [ ] **Base SQLite** créée et peuplée
- [ ] **2 endpoints** minimum (`/api/kpis`, `/api/products`)
- [ ] **Documentation Swagger** accessible sur `/docs`
- [ ] **Code versionné** sur Git

## Endpoints à implémenter

| Endpoint | Description |
|----------|-------------|
| `GET /api/kpis` | CA total, nb clients, panier moyen |
| `GET /api/products` | Liste des produits avec stats |

---

# 🚀 C'est parti !

## Prochaines étapes

1. **Créer la base SQLite** → Importer les données
2. **Développer l'API** → `main.py` avec FastAPI
3. **Tester** → Swagger UI sur `/docs`
4. **Documenter** → README

> *"Une bonne API, c'est une API que les autres peuvent utiliser sans lire le code."*