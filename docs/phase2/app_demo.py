"""
Dashboard Lapage — Application principale
==========================================

Point d'entrée de l'application Streamlit.
Les pages sont dans le dossier /pages

Lancer avec : streamlit run app.py
"""

import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Lapage",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre principal
st.title("🏪 Dashboard Lapage")
st.markdown("### Analyse des ventes de la librairie en ligne")

# Description
st.markdown("""
---

Bienvenue sur le tableau de bord analytique de **Lapage**.

Ce dashboard permet d'explorer les données de ventes et d'obtenir des insights 
pour le pilotage stratégique de l'activité e-commerce.

### 📑 Pages disponibles

Utilisez le **menu à gauche** pour naviguer entre les différentes sections :

| Page | Description |
|------|-------------|
| 📊 **KPIs** | Indicateurs clés et vue d'ensemble |
| 📈 **Évolution CA** | Analyse temporelle du chiffre d'affaires |
| 🔍 **Corrélations** | Relations entre les variables |

---

### 🎯 Contexte

Ce dashboard a été développé pour répondre aux besoins de :
- **Sylvain** (CODIR) : Vue globale et pilotage
- **Annabelle** (Marketing) : Analyse des profils clients
- **Julie** (BI Analyst) : Corrélations et analyses statistiques

""")

# Footer
st.markdown("---")
st.caption("Dashboard Lapage — Projet P9 OpenClassrooms")