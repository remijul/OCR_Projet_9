"""
Page Prévisions CA
==================

Affiche les prévisions de chiffre d'affaires générées par le modèle SARIMA
via l'API endpoint /api/predict.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from datetime import datetime, timedelta

# Configuration de la page
st.set_page_config(
    page_title="Prévisions CA — Lapage",
    page_icon="🔮",
    layout="wide"
)

# Configuration API
API_BASE_URL = st.sidebar.text_input(
    "🔗 URL de l'API",
    value="http://127.0.0.1:8000",
    help="URL de base de l'API FastAPI"
)


def fetch_predictions(horizon_days: int) -> dict:
    """
    Récupère les prévisions depuis l'API.
    
    Args:
        horizon_days: Nombre de jours à prédire
        
    Returns:
        dict: Réponse de l'API avec predictions et model_info
    """
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/predict",
            params={"horizon_days": horizon_days},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error(f"""
        ❌ **Connexion impossible à l'API**
        
        Vérifiez que l'API est lancée :
        ```bash
        cd api
        uvicorn app.main:app --reload
        ```
        
        URL testée : `{API_BASE_URL}`
        """)
        return None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 503:
            st.error("""
            ⚠️ **Modèle non disponible**
            
            Le modèle SARIMA n'a pas été entraîné. Exécutez d'abord le notebook d'entraînement.
            """)
        else:
            st.error(f"Erreur API : {e}")
        return None
    except Exception as e:
        st.error(f"Erreur : {e}")
        return None


def fetch_model_info() -> dict:
    """Récupère les informations du modèle."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/predict/info", timeout=10)
        response.raise_for_status()
        return response.json()
    except:
        return None


def create_forecast_chart(predictions: list, model_info: dict) -> go.Figure:
    """
    Crée le graphique des prévisions avec intervalle de confiance.
    
    Args:
        predictions: Liste des prédictions
        model_info: Informations du modèle
        
    Returns:
        go.Figure: Graphique Plotly
    """
    df = pd.DataFrame(predictions)
    df['date'] = pd.to_datetime(df['date'])
    
    fig = go.Figure()
    
    # Intervalle de confiance (zone ombrée)
    fig.add_trace(go.Scatter(
        x=pd.concat([df['date'], df['date'][::-1]]),
        y=pd.concat([df['upper'], df['lower'][::-1]]),
        fill='toself',
        fillcolor='rgba(0, 100, 255, 0.15)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo='skip',
        showlegend=True,
        name='Intervalle de confiance (95%)'
    ))
    
    # Ligne de prévision principale
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['ca_predicted'],
        mode='lines+markers',
        name='Prévision CA',
        line=dict(color='#0066FF', width=3),
        marker=dict(size=6),
        hovertemplate='<b>%{x|%d/%m/%Y}</b><br>CA prévu: %{y:,.0f}€<extra></extra>'
    ))
    
    # Bornes supérieure et inférieure (lignes pointillées)
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['upper'],
        mode='lines',
        name='Borne supérieure',
        line=dict(color='#0066FF', width=1, dash='dash'),
        hovertemplate='Borne sup: %{y:,.0f}€<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['lower'],
        mode='lines',
        name='Borne inférieure',
        line=dict(color='#0066FF', width=1, dash='dash'),
        hovertemplate='Borne inf: %{y:,.0f}€<extra></extra>'
    ))
    
    # Mise en forme
    mape = model_info.get('metrics', {}).get('mape', 'N/A')
    title = f"🔮 Prévisions CA — Modèle SARIMA (MAPE: {mape}%)"
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20)),
        xaxis_title="Date",
        yaxis_title="Chiffre d'affaires (€)",
        template='plotly_white',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=500
    )
    
    # Format des axes
    fig.update_yaxes(tickformat=",", ticksuffix="€")
    fig.update_xaxes(tickformat="%d/%m")
    
    return fig


def create_daily_breakdown_chart(predictions: list) -> go.Figure:
    """Crée un graphique en barres par jour de la semaine."""
    df = pd.DataFrame(predictions)
    df['date'] = pd.to_datetime(df['date'])
    df['day_name'] = df['date'].dt.day_name()
    df['day_num'] = df['date'].dt.dayofweek
    
    # Agrégation par jour de la semaine
    daily_avg = df.groupby(['day_num', 'day_name'])['ca_predicted'].mean().reset_index()
    daily_avg = daily_avg.sort_values('day_num')
    
    # Traduction des jours
    day_translation = {
        'Monday': 'Lundi', 'Tuesday': 'Mardi', 'Wednesday': 'Mercredi',
        'Thursday': 'Jeudi', 'Friday': 'Vendredi', 'Saturday': 'Samedi', 'Sunday': 'Dimanche'
    }
    daily_avg['day_fr'] = daily_avg['day_name'].map(day_translation)
    
    # Couleurs : week-end en couleur différente
    colors = ['#0066FF' if d < 5 else '#FF6B6B' for d in daily_avg['day_num']]
    
    fig = go.Figure(data=[
        go.Bar(
            x=daily_avg['day_fr'],
            y=daily_avg['ca_predicted'],
            marker_color=colors,
            hovertemplate='<b>%{x}</b><br>CA moyen prévu: %{y:,.0f}€<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="📊 CA moyen prévu par jour de la semaine",
        xaxis_title="",
        yaxis_title="CA moyen (€)",
        template='plotly_white',
        height=400
    )
    
    fig.update_yaxes(tickformat=",", ticksuffix="€")
    
    return fig


# =============================================================================
# INTERFACE PRINCIPALE
# =============================================================================

st.title("🔮 Prévisions du Chiffre d'Affaires")
st.markdown("---")

# Sidebar : Paramètres
st.sidebar.header("⚙️ Paramètres")

horizon_days = st.sidebar.slider(
    "📅 Horizon de prévision (jours)",
    min_value=7,
    max_value=90,
    value=30,
    step=7,
    help="Nombre de jours à prédire"
)

# Bouton de rafraîchissement
if st.sidebar.button("🔄 Actualiser les prévisions", type="primary"):
    st.cache_data.clear()

# Vérification du modèle
st.sidebar.markdown("---")
st.sidebar.subheader("📊 État du modèle")

model_info_sidebar = fetch_model_info()
if model_info_sidebar:
    st.sidebar.success("✅ Modèle chargé")
    st.sidebar.markdown(f"""
    - **Type** : {model_info_sidebar['model']['type']}
    - **MAE** : {model_info_sidebar['metrics']['mae']}€
    - **MAPE** : {model_info_sidebar['metrics']['mape']}%
    """)
else:
    st.sidebar.error("❌ Modèle non disponible")


# =============================================================================
# CONTENU PRINCIPAL
# =============================================================================

# Récupérer les prévisions
with st.spinner("Chargement des prévisions..."):
    data = fetch_predictions(horizon_days)

if data:
    predictions = data['predictions']
    model_info = data['model_info']
    
    # Métriques en haut
    col1, col2, col3, col4 = st.columns(4)
    
    df_pred = pd.DataFrame(predictions)
    total_ca = df_pred['ca_predicted'].sum()
    avg_ca = df_pred['ca_predicted'].mean()
    min_ca = df_pred['ca_predicted'].min()
    max_ca = df_pred['ca_predicted'].max()
    
    col1.metric("📈 CA total prévu", f"{total_ca:,.0f}€")
    col2.metric("📊 CA moyen/jour", f"{avg_ca:,.0f}€")
    col3.metric("⬇️ CA min prévu", f"{min_ca:,.0f}€")
    col4.metric("⬆️ CA max prévu", f"{max_ca:,.0f}€")
    
    st.markdown("---")
    
    # Graphique principal
    st.subheader("📈 Courbe de prévision")
    fig_forecast = create_forecast_chart(predictions, model_info)
    st.plotly_chart(fig_forecast, width='stretch')
    
    # Deux colonnes : Breakdown + Tableau
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.subheader("📊 Répartition hebdomadaire")
        fig_daily = create_daily_breakdown_chart(predictions)
        st.plotly_chart(fig_daily, width='stretch')
    
    with col_right:
        st.subheader("📋 Détail des prévisions")
        
        # Formater le tableau
        df_display = df_pred.copy()
        df_display['date'] = pd.to_datetime(df_display['date']).dt.strftime('%d/%m/%Y')
        df_display['ca_predicted'] = df_display['ca_predicted'].apply(lambda x: f"{x:,.0f}€")
        df_display['lower'] = df_display['lower'].apply(lambda x: f"{x:,.0f}€")
        df_display['upper'] = df_display['upper'].apply(lambda x: f"{x:,.0f}€")
        df_display.columns = ['Date', 'CA prévu', 'Borne inf.', 'Borne sup.']
        
        st.dataframe(
            df_display,
            width='stretch',
            height=400
        )
    
    # Informations du modèle
    st.markdown("---")
    st.subheader("🤖 Informations du modèle")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    
    with col_m1:
        st.markdown(f"""
        **Configuration**
        - Type : `{model_info['type']}`
        - Order : `{model_info['order']}`
        - Seasonal : `{model_info['seasonal_order']}`
        """)
    
    with col_m2:
        metrics = model_info['metrics']
        st.markdown(f"""
        **Métriques de performance**
        - MAE : `{metrics['mae']}€`
        - RMSE : `{metrics['rmse']}€`
        - MAPE : `{metrics['mape']}%`
        """)
    
    with col_m3:
        st.markdown(f"""
        **Entraînement**
        - Dernière date : `{model_info['last_training_date']}`
        - Horizon max : `90 jours`
        """)
    
    # Export des données
    st.markdown("---")
    st.subheader("📥 Export")
    
    csv_data = df_pred.to_csv(index=False)
    st.download_button(
        label="📥 Télécharger les prévisions (CSV)",
        data=csv_data,
        file_name=f"previsions_ca_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

else:
    # Message d'erreur si pas de données
    st.warning("""
    ## ⚠️ Prévisions non disponibles
    
    Pour afficher les prévisions, assurez-vous que :
    
    1. **L'API est lancée** :
       ```bash
       cd api
       uvicorn app.main:app --reload
       ```
    
    2. **Le modèle est entraîné** :
       - Exécutez le notebook `P9_Notebook_Comparaison_Modeles.ipynb`
       - Vérifiez que `data/models/saved/best_model_sarima.pkl` existe
    
    3. **L'URL de l'API est correcte** (sidebar)
    """)


# Footer
st.markdown("---")
st.caption("🔮 Prévisions générées par le modèle SARIMA — Projet P9 Lapage")