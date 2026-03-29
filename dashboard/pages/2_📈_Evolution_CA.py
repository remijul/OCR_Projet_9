"""
Page Évolution CA — Analyse temporelle
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
from data_loader import charger_transactions, get_filtres_disponibles

# Configuration
st.set_page_config(page_title="Évolution CA - Lapage", page_icon="📈", layout="wide")

# Données
df = charger_transactions()
filtres = get_filtres_disponibles()

# =============================================================================
# SIDEBAR - FILTRES
# =============================================================================

with st.sidebar:
    st.header("🔧 Paramètres")
    
    # Catégorie
    categorie = st.selectbox(
        "📚 Catégorie",
        options=["Toutes"] + filtres['categories']
    )
    
    # Granularité
    granularite = st.radio(
        "📅 Granularité",
        options=["Jour", "Semaine", "Mois"],
        index=2
    )
    
    # Moyenne mobile
    st.markdown("---")
    afficher_mm = st.checkbox("Moyenne mobile", value=True)
    if afficher_mm:
        fenetre = st.slider("Fenêtre", 2, 12, 3)

# Filtrer
df_f = df.copy()
if categorie != "Toutes":
    df_f = df_f[df_f['categ'] == categorie]

# =============================================================================
# CONTENU
# =============================================================================

st.title("📈 Évolution du Chiffre d'Affaires")

# Agréger selon granularité
freq_map = {"Jour": "D", "Semaine": "W", "Mois": "ME"}
freq = freq_map[granularite]

df_agg = df_f.groupby(pd.Grouper(key='date', freq=freq)).agg({
    'price': 'sum',
    'client_id': 'nunique'
}).reset_index()
df_agg.columns = ['date', 'ca', 'clients']

# Moyenne mobile
if afficher_mm:
    df_agg['mm'] = df_agg['ca'].rolling(window=fenetre, min_periods=1).mean()

# Graphique principal
st.markdown("---")

fig = go.Figure()

fig.add_trace(go.Bar(
    x=df_agg['date'], y=df_agg['ca'],
    name='CA', marker_color='#2196F3', opacity=0.7
))

if afficher_mm:
    fig.add_trace(go.Scatter(
        x=df_agg['date'], y=df_agg['mm'],
        name=f'MM {fenetre}', line=dict(color='#F44336', width=3)
    ))

fig.update_layout(
    template='plotly_white',
    xaxis_title="",
    yaxis_title="CA (€)",
    legend=dict(orientation='h', y=1.1),
    hovermode='x unified'
)

st.plotly_chart(fig, width='stretch')

# Stats
col1, col2, col3 = st.columns(3)
col1.metric("CA Total", f"{df_agg['ca'].sum():,.0f} €".replace(",", " "))
col2.metric(f"CA Moyen / {granularite}", f"{df_agg['ca'].mean():,.0f} €".replace(",", " "))
col3.metric("Période max", f"{df_agg['ca'].max():,.0f} €".replace(",", " "))

# Comparaison catégories
if categorie == "Toutes":
    st.markdown("---")
    st.subheader("📊 Comparaison par catégorie")
    
    df_categ = df.groupby([pd.Grouper(key='date', freq=freq), 'categ'])['price'].sum().reset_index()
    
    fig = px.line(df_categ, x='date', y='price', color='categ',
                  labels={'date': '', 'price': 'CA (€)', 'categ': 'Catégorie'})
    fig.update_layout(template='plotly_white', hovermode='x unified')
    st.plotly_chart(fig, width='stretch')

# Analyse jour de la semaine
st.markdown("---")
st.subheader("📅 CA par jour de la semaine")

jours_ordre = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
jours_fr = {'Monday': 'Lundi', 'Tuesday': 'Mardi', 'Wednesday': 'Mercredi', 
            'Thursday': 'Jeudi', 'Friday': 'Vendredi', 'Saturday': 'Samedi', 'Sunday': 'Dimanche'}

df_jour = df_f.groupby('jour_semaine')['price'].sum().reset_index()
df_jour['ordre'] = df_jour['jour_semaine'].map(lambda x: jours_ordre.index(x))
df_jour = df_jour.sort_values('ordre')
df_jour['jour'] = df_jour['jour_semaine'].map(jours_fr)

fig = px.bar(df_jour, x='jour', y='price', labels={'jour': '', 'price': 'CA (€)'})
fig.update_layout(template='plotly_white')
st.plotly_chart(fig, width='stretch')