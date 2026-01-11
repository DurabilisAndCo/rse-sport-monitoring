#!/bin/bash
# Script pour aider à pousser le code sur GitHub

echo "--- Configuration GitHub ---"
read -p "Entrez votre nom d'utilisateur GitHub : " username
read -p "Entrez le nom du dépôt (ex: rse-sport-matrix) : " repo_name

# Ajouter le remote
git remote add origin https://github.com/$username/$repo_name.git

echo "--- Instructions ---"
echo "1. Créez un dépôt vide nommé '$repo_name' sur GitHub."
echo "2. Exécutez la commande suivante pour pousser votre code :"
echo "   git push -u origin main"
