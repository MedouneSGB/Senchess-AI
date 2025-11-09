#!/bin/bash

# Fine-tuning rapide de Gear v1.0 -> v1.1
# Objectif: Améliorer de 98.5% à 99%+ mAP50

echo "╔═══════════════════════════════════════════════════════════════════════╗"
echo "║           🥈 GEAR V1.1 FINE-TUNING (Quick Win)                       ║"
echo "╚═══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Stratégie : Fine-tune depuis Gear v1.0"
echo "Dataset   : 693 images (photos physiques)"
echo "Objectif  : 98.5% → 99%+ mAP50"
echo "Durée     : ~2-3 heures"
echo ""

source .venv/bin/activate

python src/train.py \
    --model models/senchess_gear_v1.0/weights/best.pt \
    --data-yaml data/chess_dataset.yaml \
    --epochs 50 \
    --img-size 640 \
    --batch-size 8 \
    --project models \
    --name senchess_gear_v1.1

echo ""
echo "✅ Gear v1.1 créé ! Testez avec :"
echo "   python src/evaluate.py --model models/senchess_gear_v1.1/weights/best.pt"
