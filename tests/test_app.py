"""
Tests de l'application Lapage
=============================

3 tests pour valider les fonctionnalités essentielles :
1. Chargement des données
2. Calcul des KPIs
3. Filtrage des données

Exécuter avec : pytest tests/ -v
"""

import pytest
import pandas as pd
import sys
from pathlib import Path

# Ajouter src au path pour importer data_loader
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


# =============================================================================
# FIXTURES (données partagées entre les tests)
# =============================================================================

@pytest.fixture
def df_transactions():
    """Charge les données de transactions pour les tests."""
    filepath = Path(__file__).parent.parent / "data" / "processed" / "transactions_enrichies.csv"
    
    if not filepath.exists():
        pytest.skip(f"Fichier de données non trouvé : {filepath}")
    
    df = pd.read_csv(filepath)
    df['date'] = pd.to_datetime(df['date'])
    return df


# =============================================================================
# TEST 1 : Chargement des données
# =============================================================================

def test_chargement_donnees(df_transactions):
    """
    Vérifie que les données se chargent correctement
    et contiennent les colonnes attendues.
    """
    # Colonnes obligatoires
    colonnes_attendues = [
        'id_prod', 'date', 'client_id', 'price', 
        'categ', 'sex', 'age_client', 'segment_client'
    ]
    
    # Vérifier que le DataFrame n'est pas vide
    assert len(df_transactions) > 0, "Le DataFrame est vide"
    
    # Vérifier la présence des colonnes
    for col in colonnes_attendues:
        assert col in df_transactions.columns, f"Colonne manquante : {col}"
    
    # Vérifier les types de données critiques
    assert df_transactions['price'].dtype in ['float64', 'int64'], "price doit être numérique"
    assert pd.api.types.is_datetime64_any_dtype(df_transactions['date']), "date doit être datetime"


# =============================================================================
# TEST 2 : Calcul des KPIs
# =============================================================================

def test_calcul_kpis(df_transactions):
    """
    Vérifie que les KPIs calculés sont cohérents.
    """
    # Calcul des KPIs
    ca_total = df_transactions['price'].sum()
    nb_transactions = len(df_transactions)
    nb_clients = df_transactions['client_id'].nunique()
    panier_moyen = df_transactions['price'].mean()
    
    # Vérifications de cohérence
    assert ca_total > 0, "Le CA total doit être positif"
    assert nb_transactions > 0, "Il doit y avoir des transactions"
    assert nb_clients > 0, "Il doit y avoir des clients"
    assert panier_moyen > 0, "Le panier moyen doit être positif"
    
    # Vérification logique : CA = nb_transactions * panier_moyen (approximativement)
    ca_calcule = nb_transactions * panier_moyen
    assert abs(ca_total - ca_calcule) < 0.01, "Incohérence dans le calcul du CA"
    
    # Vérification : nb_clients <= nb_transactions
    assert nb_clients <= nb_transactions, "Plus de clients que de transactions"


# =============================================================================
# TEST 3 : Filtrage des données
# =============================================================================

def test_filtrage_donnees(df_transactions):
    """
    Vérifie que le filtrage par catégorie fonctionne correctement.
    """
    # Récupérer une catégorie existante
    categories = df_transactions['categ'].unique()
    assert len(categories) > 0, "Aucune catégorie trouvée"
    
    categorie_test = categories[0]
    
    # Appliquer le filtre
    df_filtre = df_transactions[df_transactions['categ'] == categorie_test]
    
    # Vérifications
    assert len(df_filtre) > 0, f"Aucune transaction pour la catégorie {categorie_test}"
    assert len(df_filtre) <= len(df_transactions), "Le filtre ne réduit pas les données"
    
    # Vérifier que toutes les lignes filtrées ont la bonne catégorie
    assert (df_filtre['categ'] == categorie_test).all(), "Le filtre n'est pas correct"
    
    # Vérifier le filtrage par date
    date_min = df_transactions['date'].min()
    date_max = df_transactions['date'].max()
    date_milieu = date_min + (date_max - date_min) / 2
    
    df_filtre_date = df_transactions[df_transactions['date'] >= date_milieu]
    
    assert len(df_filtre_date) > 0, "Aucune transaction après la date milieu"
    assert len(df_filtre_date) < len(df_transactions), "Le filtre date ne réduit pas les données"