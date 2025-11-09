#!/bin/bash

# Script de lancement du fine-tuning Gear-Haki
# Usage: ./run_finetune.sh

echo "╔═══════════════════════════════════════════════════════════════════════╗"
echo "║        🎯 SENCHESS GEAR-HAKI FINE-TUNING                             ║"
echo "╚═══════════════════════════════════════════════════════════════════════╝"
echo ""

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source .venv/bin/activate

# Lancer le fine-tuning
echo "🚀 Lancement du fine-tuning..."
echo ""

python src/finetune.py \
    --gear-data data/processed \
    --haki-data data/chess_decoder_1000 \
    --output-data data/gear_haki_merged \
    --base-model models/senchess_haki_v1.0/weights/best.pt \
    --epochs 50 \
    --lr0 0.001 \
    --name senchess_gear_haki_finetune

echo ""
echo "╔═══════════════════════════════════════════════════════════════════════╗"
echo "║                    ✅ FINE-TUNING TERMINÉ                             ║"
echo "╚═══════════════════════════════════════════════════════════════════════╝"
