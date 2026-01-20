# Déploiement CSA-IRA Tool

## Option 1 : GitHub Pages (Recommandé) 🚀

### Étapes rapides

```bash
# 1. Naviguer vers le dossier
cd "/Users/mac/IRA CSA/rse-sport-monitoring"

# 2. Ajouter les fichiers
git add ira-audit-tool/

# 3. Commit
git commit -m "Add CSA-IRA self-audit tool"

# 4. Push vers GitHub
git push origin main

# 5. Activer GitHub Pages
# Aller sur GitHub.com → Settings → Pages → Source: main branch → /ira-audit-tool
```

**URL finale** : `https://[votre-username].github.io/rse-sport-monitoring/ira-audit-tool/`

---

## Option 2 : Netlify (Alternative) ⚡

### Via Netlify Drop

1. Aller sur [netlify.com/drop](https://app.netlify.com/drop)
2. Glisser-déposer le dossier `ira-audit-tool`
3. URL générée automatiquement

### Via GitHub (automatique)

1. Connecter votre repo GitHub à Netlify
2. Build settings :
   - **Build command** : (laisser vide)
   - **Publish directory** : `ira-audit-tool`
3. Deploy automatique à chaque push

---

## Option 3 : Vercel 🔷

```bash
# Installer Vercel CLI
npm i -g vercel

# Déployer
cd ira-audit-tool
vercel --prod
```

---

## Configuration Recommandée

### Pour GitHub Pages

Créer `ira-audit-tool/.nojekyll` (fichier vide) pour éviter les problèmes avec Jekyll.

### Amélioration Performance

**Optionnel** : Ajouter un fichier `.htaccess` ou configuration pour cache :

```
# Cache assets pour 1 an
<FilesMatch "\.(jpg|jpeg|png|gif|svg|css|js)$">
    Header set Cache-Control "max-age=31536000, public"
</FilesMatch>
```

---

## Domaine Personnalisé (Optionnel)

### GitHub Pages
1. Créer fichier `CNAME` dans `ira-audit-tool/`
2. Contenu : `audit-ira.votredomaine.com`
3. Configurer DNS chez votre registrar

### Netlify/Vercel
Configuration dans le dashboard (plus simple)

---

## Vérification Déploiement

Après déploiement, vérifier :
- ✅ Page d'accueil charge
- ✅ Images cas d'études affichées
- ✅ Formulaires fonctionnent
- ✅ Navigation entre écrans
- ✅ LocalStorage sauvegarde
- ✅ Export PDF/TXT

---

## Commandes Git Rapides

```bash
# Statut actuel
git status

# Ajouter l'outil
git add ira-audit-tool/

# Commit
git commit -m "🌱 Add CSA-IRA self-audit tool

- 7-screen mobile-first application
- 10 CSA-IRA principles assessment
- Personalized recommendations
- Roadmap generator
- Case studies (Mohamed & Fadi, Inès)
- PDF/TXT export"

# Push
git push origin main
```

---

## 🎯 Recommandation Finale

**Pour vous** : Je recommande **GitHub Pages** car :
- ✅ Gratuit
- ✅ Intégré avec votre repo existant
- ✅ Simple à activer
- ✅ URL propre
- ✅ Support HTTPS automatique

Voulez-vous que je procède au déploiement ?
