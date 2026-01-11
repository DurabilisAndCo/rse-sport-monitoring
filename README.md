# 📊 Data Monitoring – Projet RSE & Sport

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

Plateforme de suivi et d'analyse des projets RSE dans le secteur sportif développée par **Durabilis & Co**.

## 🚀 Fonctionnalités

### 📋 Gestion de Projets
- **Formulaire Multi-étapes** : Création de projets avec 4 sections structurées
  - Informations générales
  - Sport & discipline
  - Alignement ODD / Agenda 2063
  - Indicateurs & suivi
- **Sélection Intelligente** : Plus de 150 sports catalogués par catégorie
### 📊 Dashboard Interactif
- **Vue Globale** : Cartographie des projets et indicateurs clés (KPIs)
- **Analyse d'Impact** : Graphiques dynamiques et suivi des ODD

### 💡 Intelligence & Recommandations
- **Moteur de Recommandations** : Suggestions automatiques pour optimiser l'impact
- **Alignement ODD** : Analyse de la couverture des objectifs de développement durable

### 📄 Rapports Professionnels
- **Export PDF & HTML** : Rapports style AFD (Agence Française de Développement) prêts à partager, incluant graphiques et analyses
- **Personnalisation** : Rapports adaptés au projet sélectionné

### 🗂️ Gestion de Projets
- **Administration** : Création, édition et suppression de projets
- **Export Données** : Export global au format CSV
- **Mode Démo** : Données fictives réalistes pour tester la plateforme
- **Contenu Complet** : Résumé exécutif, visualisations, recommandations

## 🛠️ Installation Locale

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/DurabilisAndCo/rse-sport-monitoring.git
   cd rse-sport-monitoring
   ```

2. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancer l'application** :
   ```bash
   streamlit run app.py
   ```

L'application sera accessible sur `http://localhost:8501`

## 🌐 Déploiement sur Streamlit Cloud

1. Forkez ou importez ce repository sur GitHub
2. Connectez-vous sur [share.streamlit.io](https://share.streamlit.io)
3. Créez une nouvelle app :
   - Repository : `DurabilisAndCo/rse-sport-monitoring`
   - Branch : `main`
   - Main file path : `app.py`
4. Cliquez sur "Deploy"

## 📦 Structure du Projet

```
rse-sport-monitoring/
├── app.py                  # Application principale
├── mock_data.py           # Générateur de données de démonstration
├── recommendations.py     # Moteur de recommandations
├── requirements.txt       # Dépendances Python
├── .streamlit/
│   └── config.toml       # Configuration Streamlit
└── README.md             # Documentation
```

## 🌍 Alignements Stratégiques

### ODD (Objectifs de Développement Durable)
Les 17 ODD de l'Agenda 2030 des Nations Unies sont intégrés pour permettre l'alignement stratégique des projets sur les objectifs mondiaux de développement durable.

### Agenda 2063
Le cadre stratégique de l'Union Africaine pour la transformation socio-économique du continent est également intégré avec ses 7 aspirations principales.

## 🎨 Design & Branding

L'application utilise la charte graphique **Durabilis & Co** :
- Bleu principal : `#00A9E0`
- Bleu secondaire : `#2E3192`
- Typographie : Inter (Google Fonts)
- Design moderne avec glassmorphism et animations fluides

## 📊 Technologies

- **Framework** : Streamlit 1.28+
- **Visualisations** : Plotly 5.17+
- **Data Processing** : Pandas 2.0+, NumPy 1.24+
- **Styling** : CSS personnalisé

## 👥 Auteur

**Durabilis & Co** - Conseil en stratégie RSE et impact social

## 📄 Licence

Ce projet est propriété de Durabilis & Co.

---

*Pour toute question ou support, contactez l'équipe Durabilis & Co.*
