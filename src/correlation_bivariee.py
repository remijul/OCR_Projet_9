# -*- coding: utf-8 -*-
"""
Fonction d'analyse de corrélation bivariée (version simplifiée)
================================================================

Usage : L'utilisateur prépare ses données en amont, puis appelle la fonction.

Exemple :
---------
# Quali × Quali (niveau transaction)
correlation_bivariee(df, 'sex', 'categ')

# Quanti × Quanti (niveau client - agrégé en amont)
df_clients = df.groupby('client_id').agg({'age': 'first', 'price': 'sum'}).reset_index()
correlation_bivariee(df_clients, 'age', 'price')
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import chi2_contingency, pearsonr, spearmanr, shapiro, f_oneway, kruskal


def correlation_bivariee(df, var1, var2, seuil=0.05):
    """
    Analyse la corrélation entre deux variables et affiche les résultats.
    
    ⚠️ IMPORTANT : Si nécessaire, agrégez vos données AVANT d'appeler cette fonction.
    
    Args:
        df (pd.DataFrame): Le DataFrame contenant les données (déjà agrégé si besoin).
        var1 (str): Le nom de la première variable.
        var2 (str): Le nom de la deuxième variable.
        seuil (float): Le seuil de significativité (défaut : 0.05).
        
    Returns:
        dict: Un dictionnaire contenant les résultats de la corrélation.
    """
    
    # =========================================================================
    # 1. INITIALISATION
    # =========================================================================
    print("=" * 70)
    print(f"📊 ANALYSE DE CORRÉLATION : {var1} ↔ {var2}")
    print("=" * 70)
    print(f"   Nombre d'observations : {len(df):,}")
    
    # Identifier les types de variables
    type_var1 = df[var1].dtype
    type_var2 = df[var2].dtype
    
    # Swap si quanti-quali pour avoir quali en premier (convention)
    if (type_var1 in ['int64', 'float64']) and (type_var2 == 'object'):
        var1, var2 = var2, var1
        type_var1, type_var2 = type_var2, type_var1
    
    print(f"   {var1} : {type_var1}")
    print(f"   {var2} : {type_var2}")
    
    # =========================================================================
    # 2. DÉTERMINER LE PROTOCOLE
    # =========================================================================
    if type_var1 == 'object' and type_var2 == 'object':
        protocole = {
            'type': "quali-quali",
            'test': "Chi²",
            'graph': "heatmap"
        }
    elif (type_var1 in ['int64', 'float64']) and (type_var2 in ['int64', 'float64']):
        protocole = {
            'type': "quanti-quanti",
            'test': "Pearson ou Spearman",
            'graph': "scatterplot"
        }
    elif type_var1 == 'object' and type_var2 in ['int64', 'float64']:
        protocole = {
            'type': "quali-quanti",
            'test': "ANOVA ou Kruskal-Wallis",
            'graph': "boxplot"
        }
    else:
        print("❌ Type de variables non pris en charge.")
        return None
    
    print(f"\n   → Type : {protocole['type']}")
    print(f"   → Test : {protocole['test']}")
    print(f"   → Graphique : {protocole['graph']}")
    
    # =========================================================================
    # 3. ANALYSE SELON LE TYPE
    # =========================================================================
    
    if protocole['type'] == "quali-quali":
        resultats = _analyser_quali_quali(df, var1, var2, seuil)
        
    elif protocole['type'] == "quanti-quanti":
        resultats = _analyser_quanti_quanti(df, var1, var2, seuil)
        
    elif protocole['type'] == "quali-quanti":
        resultats = _analyser_quali_quanti(df, var1, var2, seuil)
    
    # Ajouter les métadonnées
    resultats['var1'] = var1
    resultats['var2'] = var2
    resultats['type'] = protocole['type']
    resultats['n'] = len(df)
    
    # =========================================================================
    # 4. CONCLUSION
    # =========================================================================
    print("\n" + "=" * 70)
    print("📋 CONCLUSION")
    print("=" * 70)
    
    if resultats['significatif']:
        print(f"   ✅ Relation SIGNIFICATIVE (p = {resultats['p_value']:.4f} < {seuil})")
        print(f"   → Force : {resultats['force']}")
    else:
        print(f"   ❌ Relation NON significative (p = {resultats['p_value']:.4f} ≥ {seuil})")
    
    print("=" * 70)
    
    return resultats


# =============================================================================
# FONCTIONS INTERNES
# =============================================================================

def _analyser_quali_quali(df, var1, var2, seuil):
    """Analyse quali × quali avec Chi²."""
    
    print("\n" + "-" * 70)
    print("📊 ANALYSE QUALI × QUALI")
    print("-" * 70)
    
    # Tableau de contingence
    table = pd.crosstab(df[var1], df[var2])
    print(f"\n🔹 Tableau de contingence :")
    print(table)
    
    # Test du Chi²
    chi2, p_value, dof, expected = chi2_contingency(table)
    
    # Vérifier condition effectifs théoriques ≥ 5
    effectif_min = expected.min()
    condition_ok = effectif_min >= 5
    
    print(f"\n🔹 Test du Chi² :")
    print(f"   χ² = {chi2:.2f}")
    print(f"   ddl = {dof}")
    print(f"   p-value = {p_value:.4f}")
    
    if not condition_ok:
        print(f"   ⚠️ Attention : effectif théorique min = {effectif_min:.1f} < 5")
    
    # V de Cramer (force de l'association)
    n = table.sum().sum()
    r, c = table.shape
    v_cramer = np.sqrt(chi2 / (n * (min(r, c) - 1)))
    
    force = _interpreter_force_v_cramer(v_cramer)
    
    print(f"\n🔹 V de Cramer = {v_cramer:.3f} → {force}")
    
    # Visualisation
    print("\n🔹 Visualisation :")
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    sns.heatmap(table, annot=True, fmt='d', cmap='Blues', ax=axes[0])
    axes[0].set_title(f"Effectifs : {var1} × {var2}")
    
    table_pct = pd.crosstab(df[var1], df[var2], normalize='index') * 100
    sns.heatmap(table_pct, annot=True, fmt='.1f', cmap='Oranges', ax=axes[1])
    axes[1].set_title(f"Pourcentages par {var1}")
    
    plt.tight_layout()
    plt.show()
    
    return {
        'test': 'Chi²',
        'chi2': chi2,
        'p_value': p_value,
        'v_cramer': v_cramer,
        'force': force,
        'significatif': p_value < seuil,
        'condition_ok': condition_ok
    }


def _analyser_quanti_quanti(df, var1, var2, seuil):
    """Analyse quanti × quanti avec test de normalité + Pearson/Spearman."""
    
    print("\n" + "-" * 70)
    print("📊 ANALYSE QUANTI × QUANTI")
    print("-" * 70)
    
    # Données
    x = df[var1].dropna()
    y = df[var2].dropna()
    data = df[[var1, var2]].dropna()
    x, y = data[var1], data[var2]
    
    # Test de normalité
    print(f"\n🔹 Tests de normalité (Shapiro-Wilk) :")
    
    # Échantillonner si > 5000 observations
    n_test = min(5000, len(x))
    if len(x) > 5000:
        idx = np.random.choice(len(x), n_test, replace=False)
        x_test, y_test = x.iloc[idx], y.iloc[idx]
    else:
        x_test, y_test = x, y
    
    _, p_norm1 = shapiro(x_test)
    _, p_norm2 = shapiro(y_test)
    
    normale1 = p_norm1 >= seuil
    normale2 = p_norm2 >= seuil
    
    print(f"   {var1} : p = {p_norm1:.4f} → {'✅ Normale' if normale1 else '❌ Non normale'}")
    print(f"   {var2} : p = {p_norm2:.4f} → {'✅ Normale' if normale2 else '❌ Non normale'}")
    
    # Choix du test
    if normale1 and normale2:
        test_choisi = 'Pearson'
        coef, p_value = pearsonr(x, y)
        symbole = 'r'
    else:
        test_choisi = 'Spearman'
        coef, p_value = spearmanr(x, y)
        symbole = 'ρ'
    
    print(f"\n   → Test choisi : {test_choisi}")
    
    # Résultats
    print(f"\n🔹 Test de {test_choisi} :")
    print(f"   {symbole} = {coef:+.4f}")
    print(f"   p-value = {p_value:.4f}")
    
    # Interprétation
    direction = "positive" if coef > 0 else "négative" if coef < 0 else "nulle"
    force = _interpreter_force_correlation(coef)
    
    print(f"\n🔹 Corrélation {direction}, force {force}")
    
    # Visualisation
    print("\n🔹 Visualisation :")
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Scatterplot
    axes[0].scatter(x, y, alpha=0.5, s=20)
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    x_line = np.linspace(x.min(), x.max(), 100)
    axes[0].plot(x_line, p(x_line), 'r-', linewidth=2)
    axes[0].set_xlabel(var1)
    axes[0].set_ylabel(var2)
    axes[0].set_title(f"Scatterplot ({symbole} = {coef:+.3f})")
    
    # Distribution var1
    axes[1].hist(x, bins=30, edgecolor='white', alpha=0.7)
    axes[1].axvline(x.mean(), color='red', linestyle='--')
    axes[1].set_title(f"Distribution {var1}")
    
    # Distribution var2
    axes[2].hist(y, bins=30, edgecolor='white', alpha=0.7, color='green')
    axes[2].axvline(y.mean(), color='red', linestyle='--')
    axes[2].set_title(f"Distribution {var2}")
    
    plt.tight_layout()
    plt.show()
    
    return {
        'test': test_choisi,
        'coefficient': coef,
        'p_value': p_value,
        'direction': direction,
        'force': force,
        'significatif': p_value < seuil,
        'normale_var1': normale1,
        'normale_var2': normale2
    }


def _analyser_quali_quanti(df, var_quali, var_quanti, seuil):
    """Analyse quali × quanti avec test de normalité + ANOVA/Kruskal."""
    
    print("\n" + "-" * 70)
    print("📊 ANALYSE QUALI × QUANTI")
    print("-" * 70)
    
    # Données agrégées
    table = df.groupby(var_quali)[var_quanti].agg(['count', 'mean', 'std', 'median']).round(2)
    print(f"\n🔹 Statistiques par groupe :")
    print(table)
    
    # Groupes pour les tests
    groupes = [groupe[var_quanti].dropna().values for _, groupe in df.groupby(var_quali)]
    modalites = df[var_quali].unique()
    
    # Test de normalité par groupe
    print(f"\n🔹 Tests de normalité (Shapiro-Wilk) par groupe :")
    
    tous_normaux = True
    for modalite in modalites:
        groupe_data = df[df[var_quali] == modalite][var_quanti].dropna()
        if len(groupe_data) >= 3:
            n_test = min(5000, len(groupe_data))
            if len(groupe_data) > 5000:
                groupe_test = groupe_data.sample(n=n_test, random_state=42)
            else:
                groupe_test = groupe_data
            _, p_norm = shapiro(groupe_test)
            normale = p_norm >= seuil
            if not normale:
                tous_normaux = False
            print(f"   {var_quali}={modalite} : p = {p_norm:.4f} → {'✅' if normale else '❌'}")
        else:
            print(f"   {var_quali}={modalite} : n = {len(groupe_data)} (trop peu)")
    
    # Choix du test
    if tous_normaux:
        test_choisi = 'ANOVA'
        stat, p_value = f_oneway(*groupes)
    else:
        test_choisi = 'Kruskal-Wallis'
        stat, p_value = kruskal(*groupes)
    
    print(f"\n   → Test choisi : {test_choisi}")
    
    # Résultats
    print(f"\n🔹 Test {test_choisi} :")
    print(f"   Statistique = {stat:.2f}")
    print(f"   p-value = {p_value:.4f}")
    
    # Taille d'effet (Eta² pour ANOVA)
    if test_choisi == 'ANOVA':
        ss_between = sum(len(g) * (np.mean(g) - df[var_quanti].mean())**2 for g in groupes)
        ss_total = sum((df[var_quanti] - df[var_quanti].mean())**2)
        eta2 = ss_between / ss_total if ss_total > 0 else 0
        effet = eta2
        nom_effet = "η²"
    else:
        n = len(df)
        k = len(groupes)
        epsilon2 = (stat - k + 1) / (n - k) if n > k else 0
        effet = max(0, epsilon2)
        nom_effet = "ε²"
    
    force = _interpreter_force_eta2(effet)
    
    print(f"   {nom_effet} = {effet:.4f} → Effet {force}")
    
    # Visualisation
    print("\n🔹 Visualisation :")
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Boxplot
    ordre = df.groupby(var_quali)[var_quanti].median().sort_values(ascending=False).index
    sns.boxplot(data=df, x=var_quali, y=var_quanti, order=ordre, ax=axes[0])
    axes[0].set_title(f"Boxplot : {var_quanti} par {var_quali}")
    axes[0].tick_params(axis='x', rotation=45)
    
    # Barplot des moyennes
    sns.barplot(data=df, x=var_quali, y=var_quanti, order=ordre, ax=axes[1], errorbar='sd')
    axes[1].set_title(f"Moyenne ± écart-type")
    axes[1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()
    
    return {
        'test': test_choisi,
        'statistique': stat,
        'p_value': p_value,
        'taille_effet': effet,
        'nom_effet': nom_effet,
        'force': force,
        'significatif': p_value < seuil,
        'tous_normaux': tous_normaux
    }


# =============================================================================
# FONCTIONS D'INTERPRÉTATION
# =============================================================================

def _interpreter_force_v_cramer(v):
    """Interprète la force du V de Cramer."""
    if v < 0.1:
        return "négligeable"
    elif v < 0.2:
        return "faible"
    elif v < 0.3:
        return "modérée"
    else:
        return "forte"

def _interpreter_force_correlation(r):
    """Interprète la force d'un coefficient de corrélation."""
    r_abs = abs(r)
    if r_abs < 0.1:
        return "négligeable"
    elif r_abs < 0.3:
        return "faible"
    elif r_abs < 0.5:
        return "modérée"
    elif r_abs < 0.7:
        return "forte"
    else:
        return "très forte"

def _interpreter_force_eta2(eta2):
    """Interprète la force d'un Eta²."""
    if eta2 < 0.01:
        return "négligeable"
    elif eta2 < 0.06:
        return "faible"
    elif eta2 < 0.14:
        return "modéré"
    else:
        return "fort"


# =============================================================================
# EXEMPLE D'UTILISATION
# =============================================================================

if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════════════╗
    ║  FONCTION correlation_bivariee()                                   ║
    ╠════════════════════════════════════════════════════════════════════╣
    ║                                                                    ║
    ║  IMPORTANT : Agrégez vos données AVANT si nécessaire !             ║
    ║                                                                    ║
    ║  Exemples :                                                        ║
    ║  ─────────                                                         ║
    ║                                                                    ║
    ║  # Quali × Quali (niveau transaction)                              ║
    ║  correlation_bivariee(df, 'sex', 'categ')                          ║
    ║                                                                    ║
    ║  # Quanti × Quanti (niveau client)                                 ║
    ║  df_clients = df.groupby('client_id').agg({                        ║
    ║      'age': 'first',                                               ║
    ║      'price': 'sum'                                                ║
    ║  }).reset_index()                                                  ║
    ║  correlation_bivariee(df_clients, 'age', 'price')                  ║
    ║                                                                    ║
    ║  # Quali × Quanti (niveau transaction)                             ║
    ║  correlation_bivariee(df, 'categ', 'price')                        ║
    ║                                                                    ║
    ╚════════════════════════════════════════════════════════════════════╝
    """)