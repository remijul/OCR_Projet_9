# Phase 3 — Tests & CI/CD
## Industrialiser son application

---

# 📍 Où en sommes-nous ?

```
Phase 1                    Phase 2                    Phase 3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                                     
   📓 Notebooks         →    📱 Dashboard         →    🚀 Production
   Analyses                  App locale                Tests + Déploiement
   
   ✅ Terminé                ✅ Terminé                📍 Vous êtes ici
```

**Changement de posture :**
- Phase 2 : **Développeur** → Créer une application
- Phase 3 : **DevOps** → Industrialiser, automatiser, déployer

---

# 🎯 Objectifs de la Phase 3

## Ce que vous allez faire

1. **Écrire des tests** → Garantir que le code fonctionne
2. **Automatiser les tests** → Vérifier à chaque modification
3. **Déployer l'application** → La rendre accessible en ligne

## Ce que vous allez livrer

| Livrable | Résultat |
|----------|----------|
| Tests pytest | `pytest tests/ -v` → 3 tests ✅ |
| Pipeline CI | Badge vert sur GitHub |
| Application en ligne | URL publique accessible |

---

# 🤔 Pourquoi tester son code ?

## Le problème sans tests

```
Lundi    : "Mon code marche !" ✅
Mardi    : "J'ajoute une fonctionnalité..."
Mercredi : "Bizarre, le filtre ne marche plus..." 🐛
Jeudi    : "Ah, j'ai cassé le chargement des données aussi..." 💥
Vendredi : "Je ne sais plus ce qui marchait avant..." 😱
```

## La solution avec tests

```
Lundi    : "Mon code marche, mes 3 tests passent !" ✅
Mardi    : "J'ajoute une fonctionnalité..."
Mardi    : "Oups, un test échoue → j'ai cassé quelque chose"
Mardi    : "Je corrige → tous les tests passent" ✅
```

**Les tests détectent les régressions immédiatement.**

---

# 🧪 Les tests automatisés

## Qu'est-ce qu'un test ?

```python
def test_calcul_ca():
    # Données de test
    prix = [10, 20, 30]
    
    # Calcul
    ca_total = sum(prix)
    
    # Vérification
    assert ca_total == 60, "Le CA devrait être 60"
```

## Pyramide des tests

```
         /\
        /  \        Tests E2E (End-to-End)
       /────\       → Scénarios complets, lents
      /      \
     /────────\     Tests d'intégration
    /          \    → Plusieurs composants ensemble
   /────────────\
  /              \  Tests unitaires
 /────────────────\ → Fonctions isolées, rapides ⭐
```

**Pour ce projet** : Tests unitaires avec pytest

---

# 🔄 CI/CD — C'est quoi ?

## CI = Continuous Integration (Intégration Continue)

> À chaque modification du code, **exécuter automatiquement les tests**

```
git push → GitHub Actions → pytest → ✅ ou ❌
```

## CD = Continuous Deployment (Déploiement Continu)

> Si les tests passent, **déployer automatiquement**

```
Tests ✅ → Streamlit Cloud → URL mise à jour
```

---

# 🔄 Le workflow complet

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   CODE      │     │    CI       │     │    CD       │
│   LOCAL     │────▶│   GitHub    │────▶│  Streamlit  │
│             │     │   Actions   │     │   Cloud     │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  Tests OK ? │
                    └─────────────┘
                      │       │
                     ✅       ❌
                      │       │
                      ▼       ▼
                  Déploie   Bloque
```

**Automatisation complète** : du commit au déploiement.

---

# 💪 Intérêts des tests et CI/CD

## Pour vous (développeur)

| Avantage | Description |
|----------|-------------|
| **Confiance** | "Mon code fonctionne, les tests le prouvent" |
| **Rapidité** | Détection immédiate des bugs |
| **Documentation** | Les tests montrent comment utiliser le code |
| **Refactoring** | Modifier sans peur de tout casser |

## Pour l'équipe / l'entreprise

| Avantage | Description |
|----------|-------------|
| **Qualité** | Code vérifié avant mise en production |
| **Collaboration** | Tout le monde peut contribuer sans casser |
| **Historique** | Traçabilité des modifications |
| **Déploiement** | Mises en production fréquentes et sûres |

---

# ✅ Forces

| Force | Explication |
|-------|-------------|
| **Automatisation** | Plus besoin de tester manuellement |
| **Reproductibilité** | Mêmes tests, mêmes conditions, à chaque fois |
| **Feedback rapide** | Erreur détectée en quelques minutes |
| **Confiance** | Oser modifier le code |
| **Standard industrie** | Pratique attendue en entreprise |

---

# ⚠️ Limites

| Limite | Explication |
|--------|-------------|
| **Temps initial** | Écrire les tests prend du temps |
| **Maintenance** | Les tests doivent évoluer avec le code |
| **Faux sentiment** | "Tests verts ≠ zéro bug" |
| **Complexité** | CI/CD peut devenir complexe à grande échelle |
| **Couverture** | Tester 100% du code n'est pas réaliste |

## Le bon équilibre

> **Tester ce qui est critique**, pas tout.
> 
> 3 bons tests > 30 tests inutiles

---

# 🎓 Compétences Développeur IA

## C18 — Automatiser les tests

> *"Automatiser les phases de tests du code source lors du versionnement des sources à l'aide d'un outil d'intégration continue de manière à garantir la qualité technique des réalisations."*

**Ce que vous faites :**
- Écrire des tests pytest
- Configurer GitHub Actions
- Exécuter les tests automatiquement sur push

---

# 🎓 Compétences Développeur IA

## C19 — Livraison continue

> *"Créer un processus de livraison continue d'une application en s'appuyant sur une chaîne d'intégration continue et en paramétrant les outils d'automatisation."*

**Ce que vous faites :**
- Connecter le repo à Streamlit Cloud
- Déploiement automatique après tests
- URL publique accessible

---

# 🛠️ Outils utilisés

| Outil | Rôle | Logo |
|-------|------|------|
| **pytest** | Framework de tests Python | 🧪 |
| **GitHub Actions** | Exécution CI/CD | ⚙️ |
| **Streamlit Cloud** | Hébergement gratuit | ☁️ |

## Workflow final

```bash
# Local
pytest tests/ -v          # Tester
git add . && git commit   # Commiter
git push                  # Pousser

# Automatique
→ GitHub Actions lance les tests
→ Si OK, Streamlit Cloud redéploie
→ URL mise à jour en ~2 min
```

---

# 🎯 Ce qu'on attend de vous

## Livrables

- [ ] **3 tests** pytest fonctionnels
- [ ] **Pipeline CI** GitHub Actions opérationnel
- [ ] **Application déployée** sur Streamlit Cloud
- [ ] **README** avec badge CI + lien production

## Résultat final

```markdown
# 🏪 Dashboard Lapage

[![CI](https://github.com/user/repo/actions/workflows/ci.yml/badge.svg)](...)

🚀 **Application** : https://lapage-dashboard.streamlit.app
```

---

# 🚀 C'est parti !

## Prochaines étapes

1. **Écrire les tests** → `tests/test_app.py`
2. **Configurer le pipeline** → `.github/workflows/ci.yml`
3. **Déployer** → Streamlit Cloud
4. **Mettre à jour le README** → Badge + URL

> *"Le code qui n'est pas testé est du code qui ne marche pas... on ne le sait juste pas encore."*