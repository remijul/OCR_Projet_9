"""
Module de chargement des données
================================

Fonctions de chargement avec cache Streamlit.
À placer dans : OCR_Projet_9/src/data_loader.py
"""

import streamlit as st
import pandas as pd
from pathlib import Path


def get_data_path():
    """Retourne le chemin vers le dossier data/processed."""
    # Remonte depuis src/ vers la racine du projet
    return Path(__file__).parent.parent / "data" / "processed"


@st.cache_data
def charger_transactions():
    """
    Charge les transactions enrichies.
    
    Returns:
        pd.DataFrame: Transactions avec toutes les colonnes
    """
    filepath = get_data_path() / "transactions_enrichies.csv"
    
    if not filepath.exists():
        st.error(f"❌ Fichier non trouvé : {filepath}")
        st.stop()
    
    df = pd.read_csv(filepath)
    df['date'] = pd.to_datetime(df['date'])
    
    # Extraire le mois et l'année pour les analyses temporelles
    df['mois'] = df['date'].dt.to_period('M').astype(str)
    df['annee'] = df['date'].dt.year
    df['jour_semaine'] = df['date'].dt.day_name()
    
    return df


@st.cache_data
def charger_clients():
    """
    Agrège les données par client.
    
    Returns:
        pd.DataFrame: Un client par ligne
    """
    df = charger_transactions()
    
    clients = df.groupby('client_id').agg({
        'age_client': 'first',
        'sex': 'first',
        'segment_client': 'first',
        'price': ['sum', 'mean', 'count'],
        'categ': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else x.iloc[0]
    }).reset_index()
    
    # Aplatir les colonnes
    clients.columns = [
        'client_id', 'age', 'sex', 'segment', 
        'montant_total', 'panier_moyen', 'nb_achats', 'categ_preferee'
    ]
    
    return clients


@st.cache_data
def get_filtres_disponibles():
    """
    Retourne les valeurs uniques pour les filtres.
    
    Returns:
        dict: Dictionnaire des options de filtres
    """
    df = charger_transactions()
    
    return {
        'categories': sorted(df['categ'].unique().tolist()),
        'segments': sorted(df['segment_client'].unique().tolist()),
        'genres': ['f', 'm'],
        'date_min': df['date'].min().date(),
        'date_max': df['date'].max().date(),
        'annees': sorted(df['annee'].unique().tolist())
    }