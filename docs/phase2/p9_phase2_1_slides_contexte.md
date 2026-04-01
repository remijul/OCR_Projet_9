# Phase 2 — Du Notebook à l'Application
## Introduction au développement applicatif Data

---

# 📍 Où en sommes-nous ?

```
Phase 1                          Phase 2                          Phase 3+
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                                     
   📓 Notebooks              →    📱 Application           →    🚀 Production
   Analyses exploratoires         Dashboard interactif          CI/CD, API, MLOps
   
   ✅ Terminé                     📍 Vous êtes ici              À venir
```

**Changement de posture :**
- Phase 1 : Data **Analyst** → Exploration, compréhension
- Phase 2 : **Développeur** → Conception, réalisation

---

# 🎯 Pourquoi une application ?

## Le problème du notebook

| Notebook | Application |
|----------|-------------|
| ❌ Nécessite Python installé | ✅ Accessible via navigateur |
| ❌ Exécution cellule par cellule | ✅ Interface prête à l'emploi |
| ❌ Pas d'interactivité pour l'utilisateur | ✅ Filtres, sélections, exploration |
| ❌ Destiné aux data scientists | ✅ Destiné aux métiers (CODIR) |

## Le besoin métier

> *"Je veux pouvoir explorer les données moi-même, filtrer par période, comparer les catégories..."*
> — Sylvain, CODIR Lapage

---

# 🧠 Compétences Développeur IA mobilisées

## C14 — Analyser le besoin

> *"Analyser le besoin d'application d'un commanditaire intégrant un service d'IA, en rédigeant les **spécifications fonctionnelles** et en le modélisant"*

**Concrètement :**
- Traduire les demandes d'Annabelle et Julie en **user stories**
- Définir les **critères d'acceptation**
- Réaliser des **wireframes** (maquettes)

---

# 🧠 Compétences Développeur IA mobilisées

## C15 — Concevoir le cadre technique

> *"Concevoir le cadre technique d'une application, à partir de l'analyse du besoin, en spécifiant l'**architecture technique** et en préconisant les outils"*

**Concrètement :**
- Choisir le framework (Streamlit)
- Définir la structure du projet
- Documenter les dépendances

---

# 🧠 Compétences Développeur IA mobilisées

## C17 — Développer les composants

> *"Développer les composants techniques et les **interfaces** d'une application en utilisant les outils et langages adaptés"*

**Concrètement :**
- Coder les pages du dashboard
- Implémenter les graphiques interactifs
- Gérer les filtres et interactions

---

# 🛠️ Streamlit — C'est quoi ?

## Framework Python pour créer des apps web

```python
import streamlit as st
import pandas as pd

st.title("Mon Dashboard")

# Un slider
valeur = st.slider("Choisir une valeur", 0, 100, 50)

# Un graphique
df = pd.DataFrame({"x": [1, 2, 3], "y": [valeur, valeur*2, valeur*3]})
st.line_chart(df)
```

**Résultat** : Une application web interactive, sans HTML/CSS/JavaScript !

---

# ✅ Forces de Streamlit

| Avantage | Description |
|----------|-------------|
| **Rapidité** | Du code à l'app en quelques minutes |
| **Python natif** | Pas besoin d'apprendre un nouveau langage |
| **Interactivité** | Widgets intégrés (sliders, selectbox...) |
| **Data-friendly** | Intégration native avec Pandas, Plotly |
| **Gratuit** | Open source, déploiement gratuit possible |
| **Communauté** | Documentation riche, nombreux exemples |

**Cas d'usage idéal** : Prototypage rapide, dashboards internes, POC

---

# ⚠️ Limites de Streamlit

| Limite | Impact |
|--------|--------|
| **Pas de backend** | Logique métier côté client uniquement |
| **Rechargement complet** | Chaque interaction recharge le script |
| **Personnalisation limitée** | CSS possible mais pas natif |
| **Scalabilité** | Pas adapté pour des milliers d'utilisateurs |
| **État limité** | Gestion de session basique |

**Pas adapté pour** : Applications de production à grande échelle, apps avec authentification complexe

---

# 🔄 Streamlit vs Alternatives

| Critère | Streamlit | Dash | Flask + JS |
|---------|-----------|------|------------|
| **Courbe d'apprentissage** | ⭐ Facile | ⭐⭐ Moyen | ⭐⭐⭐ Difficile |
| **Rapidité de dev** | ⭐⭐⭐ Très rapide | ⭐⭐ Rapide | ⭐ Lent |
| **Personnalisation** | ⭐ Limitée | ⭐⭐ Moyenne | ⭐⭐⭐ Totale |
| **Production** | ⭐⭐ OK | ⭐⭐ OK | ⭐⭐⭐ Robuste |
| **Data Science** | ⭐⭐⭐ Excellent | ⭐⭐⭐ Excellent | ⭐⭐ Moyen |

**Pour ce projet** : Streamlit est le bon choix (prototypage, data-centric)

---

# 📐 Méthodologie Phase 2

## 1. Analyser → 2. Concevoir → 3. Développer

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  1. ANALYSER LE BESOIN                                          │
│     • Relire les demandes Annabelle/Julie                       │
│     • Rédiger les user stories                                  │
│     • Définir les critères d'acceptation                        │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  2. CONCEVOIR LA SOLUTION                                       │
│     • Esquisser les wireframes (maquettes)                      │
│     • Définir la structure des pages                            │
│     • Choisir les composants Streamlit                          │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  3. DÉVELOPPER L'APPLICATION                                    │
│     • Coder page par page                                       │
│     • Tester localement                                         │
│     • Documenter (README)                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

# 🎯 Objectif de cette session

## Ce qu'on va faire aujourd'hui

1. **Comprendre** les principes du maquettage
2. **Concevoir** les wireframes de l'application
3. **Découvrir** les composants Streamlit essentiels
4. **Démarrer** le développement de la V1

## Livrables attendus en fin de session

- [ ] User stories rédigées
- [ ] Wireframes esquissés (papier ou outil)
- [ ] Structure du projet créée
- [ ] Application V1 qui tourne en local

---

# 🚀 C'est parti !

## Prochaine étape : Le maquettage

> *"Un bon wireframe vaut mieux qu'un long discours"*