# Guide de déploiement — Streamlit Cloud
## Rendre votre dashboard accessible en ligne

---

## 🎯 Objectif

Déployer votre application Streamlit sur **Streamlit Cloud** pour obtenir une URL publique accessible par n'importe qui.

**Résultat** : `https://votre-app.streamlit.app`

---

## 📋 Prérequis

- [ ] Compte GitHub avec votre code pushé
- [ ] Repository **public**
- [ ] Fichier `requirements.txt` à la racine
- [ ] Application Streamlit fonctionnelle en local

---

## 🚀 Étapes de déploiement

### Étape 1 : Créer un compte Streamlit Cloud

1. Aller sur **https://share.streamlit.io**
2. Cliquer sur **"Sign up"**
3. Se connecter avec son **compte GitHub**
4. Autoriser Streamlit à accéder aux repositories

---

### Étape 2 : Préparer le repository

Vérifier que votre repo contient :

```
OCR_Projet_9/
├── dashboard/
│   ├── app.py              ← Point d'entrée
│   └── pages/
│       └── ...
├── src/
│   └── data_loader.py
├── data/
│   └── processed/
│       └── transactions_enrichies.csv
├── requirements.txt        ← Obligatoire !
└── README.md
```

**Important** : Le fichier `requirements.txt` doit être à la **racine** du repo.

---

### Étape 3 : Déployer l'application

1. Sur Streamlit Cloud, cliquer sur **"New app"**

2. Remplir le formulaire :

| Champ | Valeur |
|-------|--------|
| **Repository** | `votre-username/OCR_Projet_9` |
| **Branch** | `main` (ou `master`) |
| **Main file path** | `dashboard/app.py` |

3. Cliquer sur **"Deploy!"**

---

### Étape 4 : Patienter

- Le déploiement prend **2-5 minutes**
- Streamlit installe les dépendances et lance l'app
- Une fois terminé, vous obtenez votre URL :

```
https://votre-username-ocr-projet-9.streamlit.app
```

---

## ⚙️ Configuration avancée (optionnel)

### Personnaliser l'URL

Dans les **Settings** de l'app, vous pouvez modifier le sous-domaine :
- `lapage-dashboard.streamlit.app`
- `mon-nom-projet9.streamlit.app`

### Variables d'environnement (secrets)

Si votre app utilise des secrets (API keys, etc.) :

1. Aller dans **Settings > Secrets**
2. Ajouter au format TOML :

```toml
[database]
password = "mon_mot_de_passe"
```

3. Dans le code, accéder via :

```python
st.secrets["database"]["password"]
```

---

## 🔄 Mises à jour automatiques

**Streamlit Cloud redéploie automatiquement** à chaque push sur la branche configurée.

```
Modification locale → git push → Redéploiement auto (1-2 min)
```

---

## 🐛 Dépannage

### L'app ne se lance pas

| Problème | Solution |
|----------|----------|
| `ModuleNotFoundError` | Ajouter le module dans `requirements.txt` |
| `FileNotFoundError` | Vérifier les chemins relatifs (pas de `C:\...`) |
| Timeout au démarrage | Réduire les données chargées, utiliser `@st.cache_data` |

### Vérifier les logs

1. Aller sur votre app dans Streamlit Cloud
2. Cliquer sur **"Manage app"** (en bas à droite)
3. Consulter les **logs** pour voir les erreurs

---

## ✅ Checklist finale

- [ ] App déployée et accessible
- [ ] URL testée dans un navigateur privé
- [ ] URL ajoutée dans le README
- [ ] Badge CI visible dans le README

---

## 📝 Ajouter au README

```markdown
## 🚀 Application en ligne

[![CI](https://github.com/VOTRE_USERNAME/OCR_Projet_9/actions/workflows/ci.yml/badge.svg)](https://github.com/VOTRE_USERNAME/OCR_Projet_9/actions)

**Dashboard Lapage** : [https://votre-app.streamlit.app](https://votre-app.streamlit.app)
```

---

## 🔗 Ressources

- [Documentation Streamlit Cloud](https://docs.streamlit.io/streamlit-community-cloud)
- [FAQ Streamlit Cloud](https://docs.streamlit.io/streamlit-community-cloud/troubleshooting)
- [Limites du plan gratuit](https://docs.streamlit.io/streamlit-community-cloud/get-started/limitations)