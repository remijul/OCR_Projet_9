# Streamlit — Composants essentiels
## Aide-mémoire pour démarrer

---

## 🚀 Lancement

```bash
# Installation
pip install streamlit

# Lancer l'application
streamlit run app.py

# L'app s'ouvre sur http://localhost:8501
```

---

## 📝 Texte et titres

```python
import streamlit as st

# Titres
st.title("Titre principal")           # H1
st.header("Section")                   # H2
st.subheader("Sous-section")           # H3

# Texte
st.write("Texte simple ou **markdown**")
st.markdown("Texte avec *mise en forme*")
st.text("Texte brut (police fixe)")
st.caption("Petite légende grise")

# Blocs spéciaux
st.info("ℹ️ Information")
st.success("✅ Succès")
st.warning("⚠️ Attention")
st.error("❌ Erreur")
```

---

## 📊 Afficher des données

```python
import pandas as pd

df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

# Tableau interactif
st.dataframe(df)              # Trié, filtré

# Tableau statique
st.table(df)                  # Simple

# Métriques (KPIs)
st.metric(
    label="Chiffre d'affaires",
    value="125 000 €",
    delta="+12%"              # Variation (optionnel)
)

# Plusieurs métriques côte à côte
col1, col2, col3 = st.columns(3)
col1.metric("CA", "125K€", "+12%")
col2.metric("Clients", "2 340", "-5%")
col3.metric("Panier", "53€", "+3%")
```

---

## 📈 Graphiques

### Graphiques natifs (simples)

```python
# Line chart
st.line_chart(df)

# Bar chart
st.bar_chart(df)

# Area chart
st.area_chart(df)
```

### Avec Plotly (recommandé)

```python
import plotly.express as px

# Créer le graphique
fig = px.line(df, x="date", y="ca", title="Évolution du CA")

# Afficher dans Streamlit
st.plotly_chart(fig, use_container_width=True)
```

### Avec Matplotlib/Seaborn

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(df["x"], df["y"])

st.pyplot(fig)
```

---

## 🎛️ Widgets d'interaction

### Sélection

```python
# Liste déroulante
choix = st.selectbox("Choisir une catégorie", ["A", "B", "C"])

# Sélection multiple
choix_multi = st.multiselect("Choisir plusieurs", ["A", "B", "C"])

# Boutons radio
option = st.radio("Affichage", ["Tableau", "Graphique"])
```

### Valeurs numériques

```python
# Slider simple
valeur = st.slider("Année", 2020, 2024, 2022)

# Slider intervalle
debut, fin = st.slider("Période", 2020, 2024, (2021, 2023))

# Champ numérique
nombre = st.number_input("Quantité", min_value=0, max_value=100, value=10)
```

### Texte et dates

```python
# Champ texte
texte = st.text_input("Rechercher", "")

# Zone de texte
long_texte = st.text_area("Commentaire")

# Date
date = st.date_input("Date de début")

# Période
dates = st.date_input("Période", [date_debut, date_fin])
```

### Actions

```python
# Bouton
if st.button("Calculer"):
    st.write("Calcul en cours...")

# Checkbox
if st.checkbox("Afficher les détails"):
    st.write("Détails...")

# Toggle (switch)
actif = st.toggle("Mode avancé")
```

---

## 📐 Mise en page

### Colonnes

```python
# Deux colonnes égales
col1, col2 = st.columns(2)

with col1:
    st.write("Contenu gauche")
    
with col2:
    st.write("Contenu droite")

# Colonnes de largeurs différentes
col1, col2, col3 = st.columns([2, 1, 1])  # Ratios
```

### Sidebar

```python
# Tout ce qui est dans le sidebar
with st.sidebar:
    st.title("Filtres")
    categorie = st.selectbox("Catégorie", ["A", "B", "C"])
    
# Ou syntaxe alternative
st.sidebar.title("Filtres")
categorie = st.sidebar.selectbox("Catégorie", ["A", "B", "C"])
```

### Conteneurs et expandeurs

```python
# Conteneur
with st.container():
    st.write("Contenu groupé")

# Section dépliable
with st.expander("Voir les détails"):
    st.write("Contenu caché par défaut")
    
# Onglets
tab1, tab2 = st.tabs(["Graphique", "Données"])

with tab1:
    st.plotly_chart(fig)
    
with tab2:
    st.dataframe(df)
```

---

## 📁 Application multi-pages

### Structure

```
dashboard/
├── app.py                    # Page d'accueil
└── pages/
    ├── 1_📊_KPIs.py          # Page 1
    ├── 2_📈_Evolution.py     # Page 2
    └── 3_🔍_Analyse.py       # Page 3
```

### Règles de nommage
- Les fichiers dans `pages/` sont automatiquement des pages
- Le préfixe numérique définit l'ordre : `1_`, `2_`, `3_`
- Les emojis sont supportés : `1_📊_KPIs.py`
- Le nom affiché = nom du fichier sans préfixe ni extension

### app.py (page d'accueil)

```python
import streamlit as st

st.set_page_config(
    page_title="Dashboard Lapage",
    page_icon="🏪",
    layout="wide"
)

st.title("🏪 Dashboard Lapage")
st.write("Bienvenue ! Utilisez le menu à gauche pour naviguer.")
```

---

## 💾 Gestion de l'état (session)

```python
# Initialiser une variable de session
if "compteur" not in st.session_state:
    st.session_state.compteur = 0

# Modifier
st.session_state.compteur += 1

# Lire
st.write(f"Compteur : {st.session_state.compteur}")
```

---

## ⚡ Cache (performance)

```python
@st.cache_data  # Pour les données (DataFrames)
def charger_donnees():
    df = pd.read_csv("data.csv")
    return df

@st.cache_resource  # Pour les ressources (modèles, connexions)
def charger_modele():
    return load_model("model.pkl")

# Utilisation
df = charger_donnees()  # Exécuté une seule fois
```

---

## 📚 Ressources officielles

| Ressource | URL |
|-----------|-----|
| **Documentation** | https://docs.streamlit.io |
| **Cheat Sheet** | https://docs.streamlit.io/library/cheatsheet |
| **API Reference** | https://docs.streamlit.io/library/api-reference |
| **Gallery** | https://streamlit.io/gallery |
| **Forum** | https://discuss.streamlit.io |

---

## 🎯 Pattern typique d'une page

```python
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration
st.set_page_config(page_title="Ma Page", layout="wide")

# Chargement données (avec cache)
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

df = load_data()

# Sidebar : filtres
with st.sidebar:
    st.header("Filtres")
    categorie = st.selectbox("Catégorie", df["categ"].unique())

# Filtrer les données
df_filtre = df[df["categ"] == categorie]

# Contenu principal
st.title("📊 Analyse")

# KPIs
col1, col2 = st.columns(2)
col1.metric("Total", f"{len(df_filtre):,}")
col2.metric("Moyenne", f"{df_filtre['price'].mean():.2f} €")

# Graphique
fig = px.bar(df_filtre.groupby("mois")["price"].sum().reset_index(),
             x="mois", y="price")
st.plotly_chart(fig, use_container_width=True)
```