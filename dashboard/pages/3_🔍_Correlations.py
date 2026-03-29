"""
Page Corrélations — Analyses bivariées
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
from data_loader import charger_transactions, charger_clients

# Configuration
st.set_page_config(page_title="Corrélations - Lapage", page_icon="🔍", layout="wide")

# Données
df = charger_transactions()
df_clients = charger_clients()

# Convertir categ en string pour éviter les mixed types
df['categ'] = df['categ'].astype(str)

# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:
    st.header("🔧 Analyse")
    
    analyse = st.radio(
        "Choisir",
        ["Genre × Catégorie", "Âge × Montant", "Catégorie × Prix"]
    )

# =============================================================================
# CONTENU
# =============================================================================

st.title("🔍 Analyse des Corrélations")
st.markdown("---")

# -----------------------------------------------------------------------------
# GENRE × CATÉGORIE
# -----------------------------------------------------------------------------
if analyse == "Genre × Catégorie":
    st.subheader("👤 Genre ↔ Catégorie")
    st.caption("Les hommes et femmes achètent-ils les mêmes catégories ?")
    
    # Tableau croisé
    table = pd.crosstab(df['sex'], df['categ'], normalize='index') * 100
    table.index = table.index.map({'f': 'Femme', 'm': 'Homme'})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Heatmap (% par genre)**")
        fig = px.imshow(
            table.values,
            x=table.columns.tolist(),
            y=table.index.tolist(),
            color_continuous_scale='Blues',
            text_auto='.1f',
            aspect='auto'
        )
        fig.update_layout(template='plotly_white', coloraxis_showscale=False)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.markdown("**Comparaison**")
        df_plot = table.reset_index().melt(id_vars='sex', var_name='Catégorie', value_name='%')
        fig = px.bar(df_plot, x='Catégorie', y='%', color='sex', barmode='group',
                     color_discrete_map={'Femme': '#E91E63', 'Homme': '#2196F3'})
        fig.update_layout(template='plotly_white', legend_title='')
        st.plotly_chart(fig, width='stretch')
    
    # Tableau des effectifs
    with st.expander("📋 Tableau de contingence (effectifs)"):
        table_eff = pd.crosstab(df['sex'], df['categ'], margins=True, margins_name='Total')
        table_eff.index = table_eff.index.map(lambda x: {'f': 'Femme', 'm': 'Homme'}.get(x, x))
        st.dataframe(table_eff)
    
    st.info("**Test approprié** : Chi² + V de Cramer")

# -----------------------------------------------------------------------------
# ÂGE × MONTANT
# -----------------------------------------------------------------------------
elif analyse == "Âge × Montant":
    st.subheader("📊 Âge ↔ Montant total")
    st.caption("Les clients plus âgés dépensent-ils plus ?")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = px.scatter(
            df_clients, x='age', y='montant_total',
            opacity=0.5, trendline='ols',
            labels={'age': 'Âge', 'montant_total': 'Montant total (€)'}
        )
        fig.update_layout(template='plotly_white')
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        # Corrélation
        r = df_clients['age'].corr(df_clients['montant_total'])
        
        st.metric("Corrélation (r)", f"{r:.3f}")
        
        if abs(r) < 0.1:
            force = "négligeable"
        elif abs(r) < 0.3:
            force = "faible"
        elif abs(r) < 0.5:
            force = "modérée"
        else:
            force = "forte"
        
        st.info(f"Force : **{force}**")
        
        st.markdown("---")
        st.markdown("**Stats**")
        st.write(f"Clients : {len(df_clients):,}")
        st.write(f"Âge moyen : {df_clients['age'].mean():.0f} ans")
        st.write(f"Montant moyen : {df_clients['montant_total'].mean():.0f} €")
    
    # Distributions
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.histogram(df_clients, x='age', nbins=25, title="Distribution de l'âge")
        fig.update_layout(template='plotly_white', showlegend=False)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        fig = px.histogram(df_clients, x='montant_total', nbins=25, title="Distribution du montant")
        fig.update_layout(template='plotly_white', showlegend=False)
        st.plotly_chart(fig, width='stretch')
    
    st.info("**Test approprié** : Pearson (si normal) ou Spearman")

# -----------------------------------------------------------------------------
# CATÉGORIE × PRIX
# -----------------------------------------------------------------------------
elif analyse == "Catégorie × Prix":
    st.subheader("💰 Catégorie ↔ Prix")
    st.caption("Les prix varient-ils selon la catégorie ?")
    
    # Ordre par médiane
    ordre = df.groupby('categ')['price'].median().sort_values(ascending=False).index.tolist()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = px.box(
            df, x='categ', y='price',
            category_orders={'categ': ordre},
            labels={'categ': 'Catégorie', 'price': 'Prix (€)'}
        )
        fig.update_layout(template='plotly_white')
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.markdown("**Stats par catégorie**")
        stats = df.groupby('categ')['price'].agg(['median', 'mean', 'std']).round(2)
        stats.columns = ['Médiane', 'Moyenne', 'Écart-type']
        stats = stats.sort_values('Médiane', ascending=False)
        st.dataframe(stats)
    
    # Violin plot
    st.markdown("---")
    st.markdown("**Distribution détaillée**")
    
    fig = px.violin(
        df, x='categ', y='price', box=True,
        category_orders={'categ': ordre},
        labels={'categ': 'Catégorie', 'price': 'Prix (€)'}
    )
    fig.update_layout(template='plotly_white')
    st.plotly_chart(fig, width='stretch')
    
    st.info("**Test approprié** : ANOVA (si normal) ou Kruskal-Wallis")