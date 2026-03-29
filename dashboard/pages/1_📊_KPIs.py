"""
Page KPIs — Indicateurs clés avec filtres
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
from data_loader import charger_transactions, get_filtres_disponibles

# Configuration
st.set_page_config(page_title="KPIs - Lapage", page_icon="📊", layout="wide")

# Données
df = charger_transactions()
filtres = get_filtres_disponibles()

# =============================================================================
# SIDEBAR - FILTRES
# =============================================================================

with st.sidebar:
    st.header("🔧 Filtres")
    
    # Période
    dates = st.date_input(
        "📅 Période",
        value=(filtres['date_min'], filtres['date_max']),
        min_value=filtres['date_min'],
        max_value=filtres['date_max']
    )
    
    # Catégorie
    categories_select = st.multiselect(
        "📚 Catégories",
        options=filtres['categories'],
        default=filtres['categories']
    )
    
    # Segment
    segments_select = st.multiselect(
        "👥 Segments",
        options=filtres['segments'],
        default=filtres['segments']
    )

# Appliquer les filtres
df_f = df.copy()

if len(dates) == 2:
    df_f = df_f[(df_f['date'].dt.date >= dates[0]) & (df_f['date'].dt.date <= dates[1])]

if categories_select:
    df_f = df_f[df_f['categ'].isin(categories_select)]

if segments_select:
    df_f = df_f[df_f['segment_client'].isin(segments_select)]

# =============================================================================
# CONTENU
# =============================================================================

st.title("📊 Indicateurs Clés")

# KPIs
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

ca = df_f['price'].sum()
nb_tx = len(df_f)
nb_clients = df_f['client_id'].nunique()
panier = df_f['price'].mean() if nb_tx > 0 else 0

col1.metric("💰 CA", f"{ca:,.0f} €".replace(",", " "))
col2.metric("🛒 Transactions", f"{nb_tx:,}".replace(",", " "))
col3.metric("👥 Clients", f"{nb_clients:,}".replace(",", " "))
col4.metric("🧺 Panier moyen", f"{panier:.2f} €")

# Graphiques
st.markdown("---")

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📈 CA mensuel")
    
    df_mensuel = df_f.groupby(pd.Grouper(key='date', freq='ME'))['price'].sum().reset_index()
    df_mensuel.columns = ['date', 'ca']
    
    fig = px.bar(df_mensuel, x='date', y='ca', 
                 labels={'date': '', 'ca': 'CA (€)'})
    fig.update_layout(template='plotly_white', showlegend=False)
    st.plotly_chart(fig, width='stretch')

with col_right:
    st.subheader("📊 CA par catégorie")
    
    df_categ = df_f.groupby('categ')['price'].sum().reset_index()
    df_categ.columns = ['categ', 'ca']
    df_categ = df_categ.sort_values('ca', ascending=True)
    
    fig = px.bar(df_categ, x='ca', y='categ', orientation='h',
                 labels={'ca': 'CA (€)', 'categ': ''})
    fig.update_layout(template='plotly_white', showlegend=False)
    st.plotly_chart(fig, width='stretch')

# Deuxième ligne
st.markdown("---")

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🥧 Répartition par segment")
    
    df_seg = df_f.groupby('segment_client')['price'].sum().reset_index()
    
    fig = px.pie(df_seg, values='price', names='segment_client', hole=0.4)
    fig.update_layout(template='plotly_white')
    st.plotly_chart(fig, width='stretch')

with col_right:
    st.subheader("👥 Répartition par genre")
    
    df_genre = df_f.groupby('sex')['price'].sum().reset_index()
    df_genre['sex'] = df_genre['sex'].map({'f': 'Femme', 'm': 'Homme'})
    
    fig = px.pie(df_genre, values='price', names='sex', hole=0.4,
                 color_discrete_sequence=['#E91E63', '#2196F3'])
    fig.update_layout(template='plotly_white')
    st.plotly_chart(fig, width='stretch')