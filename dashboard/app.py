"""
Dashboard Lapage — Page d'accueil
=================================

Lancer avec : streamlit run dashboard/app.py
Depuis le dossier OCR_Projet_9/
"""

import streamlit as st
import sys
from pathlib import Path

# Ajouter src au path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data_loader import charger_transactions, get_filtres_disponibles

# Configuration
st.set_page_config(
    page_title="Dashboard Lapage",
    page_icon="🏪",
    layout="wide"
)

# Charger les données pour vérifier
df = charger_transactions()
filtres = get_filtres_disponibles()

# Header
st.title("🏪 Dashboard Lapage")
st.caption("Analyse des ventes — Librairie en ligne")

st.markdown("---")

# KPIs rapides
col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 CA Total", f"{df['price'].sum():,.0f} €".replace(",", " "))
col2.metric("🛒 Transactions", f"{len(df):,}".replace(",", " "))
col3.metric("👥 Clients", f"{df['client_id'].nunique():,}".replace(",", " "))
col4.metric("🧺 Panier moyen", f"{df['price'].mean():.2f} €")

st.markdown("---")

# Présentation
st.markdown("""
### 📑 Navigation

Utilisez le **menu latéral** pour accéder aux analyses :

| Page | Description |
|------|-------------|
| **📊 KPIs** | Indicateurs clés avec filtres |
| **📈 Évolution CA** | Analyse temporelle |
| **🔍 Corrélations** | Relations entre variables |

---

### 📋 Données chargées

""")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    **Période** : {filtres['date_min']} → {filtres['date_max']}
    
    **Catégories** : {len(filtres['categories'])}
    """)

with col2:
    st.markdown(f"""
    **Segments** : {', '.join(filtres['segments'])}
    
    **Années** : {', '.join(map(str, filtres['annees']))}
    """)

# Aperçu données
with st.expander("👀 Aperçu des données"):
    st.dataframe(df.head(10), width='stretch')