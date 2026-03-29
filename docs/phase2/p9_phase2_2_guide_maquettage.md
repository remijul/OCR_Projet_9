# Guide de Maquettage
## De l'idée au wireframe

---

## 🎯 Pourquoi maquetter ?

### Le problème sans maquette

```
Client : "Je veux un dashboard avec des graphiques"
         ↓
   [Développement 2 semaines]
         ↓
Client : "Ce n'est pas du tout ce que j'avais en tête..."
```

### La solution avec maquette

```
Client : "Je veux un dashboard avec des graphiques"
         ↓
   [Maquette en 30 minutes]
         ↓
Client : "Ah non, je voulais plutôt ça..."  →  [Correction en 5 min]
         ↓
   [Développement aligné]
         ↓
Client : "Parfait !" ✅
```

---

## 📐 Les 3 niveaux de maquettage

| Niveau | Nom | Détail | Temps | Outil |
|--------|-----|--------|-------|-------|
| 1 | **Sketch** | Croquis rapide | 5 min | Papier, tableau |
| 2 | **Wireframe** | Structure sans style | 30 min | Excalidraw, Figma |
| 3 | **Mockup** | Design complet | 2h+ | Figma, Adobe XD |

**Pour ce projet** : Niveau 2 (Wireframe) est suffisant.

---

## ✏️ Niveau 1 : Le Sketch (5 min)

### Objectif
Capturer l'idée générale, la disposition des éléments.

### Comment faire
1. Prendre une feuille A4 ou un tableau blanc
2. Dessiner un rectangle = l'écran
3. Placer les blocs principaux (titre, menu, contenu)
4. Annoter

### Exemple

```
┌─────────────────────────────────────┐
│  LOGO      Menu1  Menu2  Menu3     │
├─────────────────────────────────────┤
│                                     │
│   [Titre de la page]                │
│                                     │
│   ┌─────────┐  ┌─────────┐          │
│   │ KPI 1   │  │ KPI 2   │          │
│   └─────────┘  └─────────┘          │
│                                     │
│   ┌─────────────────────────────┐   │
│   │                             │   │
│   │     GRAPHIQUE               │   │
│   │                             │   │
│   └─────────────────────────────┘   │
│                                     │
└─────────────────────────────────────┘
```

---

## 📊 Niveau 2 : Le Wireframe (30 min)

### Objectif
Définir précisément la structure, les composants, les interactions.

### Règles
- **Pas de couleurs** (gris uniquement)
- **Pas de vrais contenus** (Lorem ipsum, données fictives)
- **Focus sur la structure** et les interactions

### Outils recommandés
- **Excalidraw** (gratuit, web) : https://excalidraw.com
- **Figma** (gratuit, web) : https://figma.com
- **Balsamiq** (payant, spécialisé wireframes)
- **Papier** (toujours efficace !)

---

## 🧩 Vocabulaire du wireframe

### Les éléments de base

| Symbole | Nom | Description |
|---------|-----|-------------|
| `[  ]` | Box / Card | Conteneur d'information |
| `[====]` | Input / Champ | Zone de saisie |
| `[▼]` | Dropdown / Select | Liste déroulante |
| `[ ○ ○ ○ ]` | Slider | Curseur de sélection |
| `[BTN]` | Button | Action cliquable |
| `───────` | Separator | Ligne de séparation |
| `≡` | Menu hamburger | Navigation mobile |

### Annotations importantes
- **Flèches** : liens entre pages
- **Numéros** : ordre de lecture
- **Notes** : comportements, interactions

---

## 🖥️ Structure type d'un dashboard

### Layout classique

```
┌─────────────────────────────────────────────────────────┐
│                       HEADER                            │
│   Logo            Navigation              User          │
├──────────┬──────────────────────────────────────────────┤
│          │                                              │
│          │              CONTENU PRINCIPAL               │
│  SIDEBAR │                                              │
│          │   ┌─────────┐  ┌─────────┐  ┌─────────┐     │
│  Filtres │   │  KPI 1  │  │  KPI 2  │  │  KPI 3  │     │
│          │   └─────────┘  └─────────┘  └─────────┘     │
│  ─────── │                                              │
│          │   ┌─────────────────────────────────────┐   │
│  Menu    │   │                                     │   │
│          │   │           GRAPHIQUE                 │   │
│          │   │                                     │   │
│          │   └─────────────────────────────────────┘   │
│          │                                              │
└──────────┴──────────────────────────────────────────────┘
```

### Avec Streamlit
- **Sidebar** = `st.sidebar`
- **Colonnes** = `st.columns()`
- **Conteneur** = `st.container()`

---

## 📝 Exercice : Maquetter le dashboard Lapage

### Contexte
Sylvain (CODIR) veut explorer les données de ventes.
Annabelle (Marketing) veut analyser les profils clients.
Julie (BI) veut visualiser les corrélations.

### Étape 1 : Lister les besoins

| Utilisateur | Besoin | Fonctionnalité |
|-------------|--------|----------------|
| Sylvain | Vue globale des ventes | KPIs + évolution CA |
| Sylvain | Comparer les périodes | Filtre temporel |
| Annabelle | Profils clients | Top/Flop, Lorenz |
| Julie | Corrélations | Graphiques quali/quanti |

### Étape 2 : Définir les pages

| Page | Contenu principal | Filtres |
|------|-------------------|---------|
| Accueil / KPIs | Chiffres clés, tendances | Période |
| Évolution CA | Graphique temporel | Période, Catégorie |
| Analyse clients | Lorenz, Top/Flop | Catégorie |
| Corrélations | Heatmap, Scatter | Variables |

---

## ✍️ Template de wireframe — Page KPIs

### À compléter sur papier ou Excalidraw

```
┌─────────────────────────────────────────────────────────┐
│  🏪 LAPAGE                    KPIs | CA | Clients | ... │
├──────────┬──────────────────────────────────────────────┤
│          │                                              │
│ FILTRES  │  📊 Tableau de bord                          │
│          │                                              │
│ Période  │  ┌────────┐  ┌────────┐  ┌────────┐         │
│ [▼ 2021] │  │  CA    │  │ Clients│  │ Panier │         │
│          │  │ XXX €  │  │  XXX   │  │  XX €  │         │
│ ──────── │  └────────┘  └────────┘  └────────┘         │
│          │                                              │
│ Catégorie│  ┌─────────────────────────────────────┐    │
│ [▼ Tous] │  │                                     │    │
│          │  │    Évolution mensuelle du CA        │    │
│          │  │         📈 (line chart)             │    │
│          │  │                                     │    │
│          │  └─────────────────────────────────────┘    │
│          │                                              │
│          │  ┌────────────────┐  ┌────────────────┐     │
│          │  │ Top catégories │  │ Répartition    │     │
│          │  │   (bar chart)  │  │   (pie chart)  │     │
│          │  └────────────────┘  └────────────────┘     │
│          │                                              │
└──────────┴──────────────────────────────────────────────┘
```

---

## 📋 Checklist maquettage

### Avant de coder, vérifier que :

- [ ] **Chaque page a un objectif clair** (qu'est-ce que l'utilisateur veut accomplir ?)
- [ ] **Les filtres sont identifiés** (quelles interactions ?)
- [ ] **La navigation est définie** (comment passer d'une page à l'autre ?)
- [ ] **Les KPIs sont listés** (quels chiffres afficher ?)
- [ ] **Les graphiques sont choisis** (quel type pour quelle donnée ?)

### Questions à se poser

1. **Qui** va utiliser cette page ?
2. **Que** cherche-t-il à comprendre ?
3. **Comment** va-t-il interagir ?
4. **Quand** cette donnée est-elle utile ?

---

## 🎯 Livrable attendu

### Format
- Papier scanné/photo OU
- Excalidraw (export PNG) OU
- Figma (lien partagé)

### Contenu minimum
- 1 wireframe par page prévue (minimum 3 pages)
- Annotations des composants
- Indication des filtres et interactions

### Critères de validation
- [ ] Structure lisible
- [ ] Composants identifiés
- [ ] Interactions annotées
- [ ] Cohérence entre pages

---

## 🔗 Ressources

### Outils de wireframing gratuits
- **Excalidraw** : https://excalidraw.com (simple, collaboratif)
- **Figma** : https://figma.com (complet, professionnel)
- **Whimsical** : https://whimsical.com (flowcharts + wireframes)

### Inspiration dashboards
- **Streamlit Gallery** : https://streamlit.io/gallery
- **Dribbble** : https://dribbble.com/search/dashboard
- **Pinterest** : rechercher "dashboard wireframe"

### Bonnes pratiques
- **Laws of UX** : https://lawsofux.com
- **Refactoring UI** (tips design) : https://twitter.com/refaboringui