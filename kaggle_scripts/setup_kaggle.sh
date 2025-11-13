#!/bin/bash

# Script d'installation et configuration de Kaggle CLI
# Usage: ./setup_kaggle.sh

echo "================================================"
echo "🎯 Configuration de Kaggle CLI"
echo "================================================"
echo ""

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python n'est pas installé"
    exit 1
fi

echo "✅ Python détecté: $(python3 --version)"
echo ""

# Installer Kaggle CLI
echo "📦 Installation de Kaggle CLI..."
pip3 install kaggle --quiet

if [ $? -eq 0 ]; then
    echo "✅ Kaggle CLI installé avec succès"
else
    echo "❌ Erreur lors de l'installation"
    exit 1
fi

echo ""
echo "================================================"
echo "🔑 Configuration des Credentials"
echo "================================================"
echo ""

# Vérifier si le dossier .kaggle existe
if [ ! -d "$HOME/.kaggle" ]; then
    echo "📁 Création du dossier ~/.kaggle..."
    mkdir -p "$HOME/.kaggle"
    echo "✅ Dossier créé"
else
    echo "✅ Dossier ~/.kaggle existe déjà"
fi

# Vérifier si kaggle.json existe
if [ -f "$HOME/.kaggle/kaggle.json" ]; then
    echo "✅ Fichier kaggle.json trouvé"
    chmod 600 "$HOME/.kaggle/kaggle.json"
    echo "✅ Permissions configurées (600)"
else
    echo "⚠️  Fichier kaggle.json non trouvé"
    echo ""
    echo "📋 Pour obtenir votre kaggle.json:"
    echo "1. Allez sur: https://www.kaggle.com/settings"
    echo "2. Scrollez jusqu'à 'API'"
    echo "3. Cliquez sur 'Create New API Token'"
    echo "4. Téléchargez le fichier kaggle.json"
    echo ""
    read -p "Avez-vous téléchargé kaggle.json? (o/n) " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Oo]$ ]]; then
        echo ""
        echo "📋 Chemin par défaut: ~/Downloads/kaggle.json"
        read -p "Entrez le chemin complet du fichier (ou appuyez sur Entrée): " json_path
        
        if [ -z "$json_path" ]; then
            json_path="$HOME/Downloads/kaggle.json"
        fi
        
        if [ -f "$json_path" ]; then
            cp "$json_path" "$HOME/.kaggle/kaggle.json"
            chmod 600 "$HOME/.kaggle/kaggle.json"
            echo "✅ kaggle.json copié et configuré"
        else
            echo "❌ Fichier non trouvé: $json_path"
            exit 1
        fi
    else
        echo "⚠️  Téléchargez kaggle.json et relancez ce script"
        exit 1
    fi
fi

echo ""
echo "================================================"
echo "🧪 Test de Connexion"
echo "================================================"
echo ""

# Tester la connexion
echo "🔄 Test de connexion à Kaggle..."
kaggle competitions list --page-size 1 > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Connexion à Kaggle réussie !"
    echo ""
    echo "📊 Informations du compte:"
    kaggle config view
else
    echo "❌ Erreur de connexion"
    echo "Vérifiez vos credentials dans ~/.kaggle/kaggle.json"
    exit 1
fi

echo ""
echo "================================================"
echo "✅ CONFIGURATION TERMINÉE"
echo "================================================"
echo ""
echo "🚀 Prochaines étapes:"
echo "1. Préparer le dataset:"
echo "   python kaggle_scripts/prepare_dataset.py"
echo ""
echo "2. Uploader le dataset:"
echo "   cd kaggle_dataset"
echo "   kaggle datasets create -p ."
echo ""
echo "3. Créer un notebook sur Kaggle:"
echo "   https://www.kaggle.com/code"
echo ""
echo "Voir docs/KAGGLE_TRAINING.md pour plus de détails"
echo "================================================"
