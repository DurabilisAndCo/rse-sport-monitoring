# 🌱 Outil d'Auto-Audit CSA-IRA

**Évalue ton projet agricole responsable selon les principes CSA-IRA**

Un outil numérique mobile-first permettant aux jeunes agriculteurs d'auto-évaluer la maturité de leur projet agricole, de mesurer son alignement avec les 10 Principes du CSA pour un Investissement Responsable dans l'Agriculture et les Systèmes Alimentaires, et de recevoir des recommandations personnalisées.

---

## 🎯 Objectifs

- **Auto-évaluer** la maturité de ton projet agricole
- **Mesurer** l'alignement avec les 10 principes CSA-IRA
- **Déterminer** l'éligibilité à l'investissement responsable (seuil ≥ 50%)
- **Recevoir** des recommandations concrètes et actionnables

---

## ✨ Fonctionnalités

### 📊 Diagnostic Complet
- Questionnaire guidé basé sur les 10 principes CSA-IRA
- Système de scoring transparent (0, 0.5, 1 par question)
- Calcul automatique du score global et par principe
- Classification en 4 profils (A, B, C, D)

### 🎯 Recommandations Personnalisées
- **Actions rapides** (0-3 mois) sans investissement
- **Actions structurantes** (3-12 mois) pour consolider
- **Actions stratégiques** (12+ mois) pour investissement

### 🗺️ Feuille de Route IRA
- 4 phases de progression clairement définies
- Timeline visuelle avec jalons
- Estimation du temps pour atteindre le seuil IRA

### 💡 Inspiration Terrain
- Cas d'études concrets (Mohamed & Fadi, Inès)
- Exemples adaptés à ton type d'activité
- Actions inspirées de projets réels

### 📄 Export & Partage
- Téléchargement du diagnostic en PDF/TXT
- Sauvegarde locale pour suivi dans le temps
- Partage avec incubateurs et financeurs

---

## 🚀 Démarrage Rapide

### Ouvrir l'application

```bash
# Option 1: Serveur Python simple
cd ira-audit-tool
python3 -m http.server 8000
# Ouvrir http://localhost:8000

# Option 2: Ouvrir directement index.html dans le navigateur
open index.html
```

### Utilisation

1. **Accueil** - Lance ton diagnostic (5-7 minutes)
2. **Profil** - Décris ton projet agricole
3. **Évaluation** - Réponds aux questions par principe
4. **Résultats** - Découvre ton score global et profil
5. **Roadmap** - Visualise ton parcours IRA
6. **Actions** - Reçois ton plan d'action personnalisé
7. **Inspiration** - Inspire-toi d'exemples concrets
8. **Export** - Télécharge et partage ton diagnostic

---

## 📁 Structure du Projet

```
ira-audit-tool/
├── index.html                    # Application principale
├── styles.css                    # Design system mobile-first
├── app.js                        # Contrôleur principal
├── data/
│   ├── questions.js              # 10 principes CSA-IRA (20 questions)
│   └── case-studies.js           # Cas Mohamed & Fadi, Inès
├── modules/
│   ├── scoring-engine.js         # Calcul des scores
│   ├── recommendation-engine.js  # Génération recommandations
│   ├── roadmap-generator.js      # Feuille de route personnalisée
│   └── export-pdf.js             # Export PDF/TXT
└── assets/
    ├── icons/                    # Icônes des 10 principes
    └── images/                   # Photos cas d'études
```

---

## 🎨 Design System

### Couleurs
- **Primaire**: HSL(142, 71%, 45%) - Vert responsable
- **Score < 30%**: Rouge (Structuration)
- **Score 30-49%**: Orange (Transition)
- **Score 50-69%**: Vert clair (Éligible)
- **Score ≥ 70%**: Vert foncé (Exemplaire)

### Typographie
- **Famille**: Inter (Google Fonts)
- **Mobile-first**: Tailles adaptatives
- **Lisibilité**: Contraste WCAG AA

### Composants
- Cards avec glassmorphism
- Boutons avec micro-animations
- Progress bars animées
- Timeline interactive

---

## 📊 Logique de Scoring

### Par Question
- `0` = Non appliqué / inexistant
- `0.5` = Partiellement appliqué / informel
- `1` = Appliqué clairement / structuré

### Par Principe
- Score = Moyenne des questions du principe

### Global
- Score = Moyenne des 10 principes × 100%
- **Seuil IRA**: ≥ 50%

### Classification
- **A (< 30%)**: Projet en structuration
- **B (30-49%)**: Projet en transition IRA
- **C (50-69%)**: Projet éligible IRA
- **D (≥ 70%)**: Projet exemplaire IRA

---

## 🧩 Les 10 Principes CSA-IRA

1. 🍚 **Sécurité alimentaire et nutrition**
2. 💰 **Développement économique durable et inclusif**
3. ⚖️ **Égalité femmes-hommes**
4. 🧑‍🌾 **Jeunes et autonomisation**
5. 🌍 **Régimes fonciers et accès aux ressources**
6. 🌱 **Ressources naturelles et résilience climatique**
7. 📚 **Patrimoine culturel et savoirs traditionnels**
8. 🏥 **Systèmes alimentaires sûrs et sains**
9. 👥 **Gouvernance et transparence**
10. 📊 **Suivi, impacts et responsabilité**

---

## 🛠️ Technologies

- **HTML5** - Structure sémantique
- **CSS3** - Design mobile-first, animations
- **JavaScript Vanilla** - Pas de dépendances lourdes
- **LocalStorage** - Persistance des données
- **jsPDF** (optionnel) - Export PDF avancé

---

## 🌍 Cas d'Études Inspirants

### Mohamed & Fadi
**Élevage laitier + Fromagerie artisanale**
- Valorisation race locale
- Partenariat producteur-transformateur
- Création emplois locaux
- Impact: +15 à +20 points IRA

### Inès
**Agriculture intégrée agroécologique**
- Techniques ancestrales (jarres romaines)
- Égalité salariale formalisée
- Rotation cultures durables
- Impact: +12 à +18 points IRA

---

## 📱 Compatibilité

- ✅ iOS Safari
- ✅ Android Chrome
- ✅ Desktop (Chrome, Firefox, Safari, Edge)
- ✅ Tablettes
- ✅ Responsive 320px - 1920px

---

## 🔐 Données & Confidentialité

- **Stockage local** uniquement (localStorage)
- **Aucune donnée serveur** dans version actuelle
- **Contrôle utilisateur** total sur ses données
- **Export** pour partage volontaire

---

## 🚀 Roadmap Futures Améliorations

- [ ] Version multilingue (Français, Anglais, Arabe)
- [ ] Synchronisation cloud optionnelle
- [ ] Comparaison avec projets similaires
- [ ] Intégration API financeurs IRA
- [ ] Application mobile native (PWA)
- [ ] Dashboard administrateur pour incubateurs

---

## 📞 Support

Pour toute question ou suggestion:
- Email: support@csa-ira-tool.org
- GitHub: [Issues](https://github.com/your-org/ira-audit-tool/issues)

---

## 📄 Licence

Ce projet est développé dans le cadre de l'initiative CSA-IRA pour promouvoir l'investissement agricole responsable en Afrique et Méditerranée.

---

**Développé avec 🌱 pour les jeunes agriculteurs**

*CSA-IRA : Comité de la Sécurité Alimentaire - Investissement Responsable dans l'Agriculture*
