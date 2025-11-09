# Training Scripts

Scripts d'entraînement des modèles YOLO pour la détection des pièces d'échecs.

## Scripts Disponibles

### train_intel.py ⭐ PRODUCTION
Script d'entraînement optimisé pour CPU Intel avec MKL.

**Caractéristiques:**
- Optimisations Intel MKL (OMP_NUM_THREADS=8)
- 8 workers dataloader
- AdamW optimizer (auto-tuned)
- Support mode --quick (10 epochs) et --full (100 epochs)

**Usage:**
```bash
# Entraînement rapide (10 epochs, ~45 min)
python scripts/training/train_intel.py --quick

# Entraînement complet (100 epochs, ~7.5 heures)
python scripts/training/train_intel.py --full
```

**Sorties:**
- Modèle: `models/senchess_intel_v1.0_quick<N>/weights/best.pt`
- Métriques: `models/senchess_intel_v1.0_quick<N>/results.csv`

### train_ultimate.py
Entraînement sur le dataset ultimate (chess_ultimate_1693).

**Dataset:** 1693 images, 13 classes (12 pièces + empty)

### train_new_model.py
Entraînement nouveau modèle sur chess_dataset_1000.

**Dataset:** 1000 images, 13 classes

### ensemble_model.py
Création d'un modèle ensemble combinant plusieurs modèles.

**Concept:** Combine prédictions de gear + haki pour améliorer précision.

## Configuration Dataset

**Localisation:** `data/chess_dataset_1000/data.yaml`

```yaml
path: C:/Users/MSGB/Downloads/Senchess-AI-main/data/chess_dataset_1000
train: images/train
val: images/val
test: images/test

nc: 13
names:
  0: white-bishop
  1: white-king
  2: white-knight
  3: white-pawn
  4: white-queen
  5: white-rook
  6: black-bishop
  7: black-king
  8: black-knight
  9: black-pawn
  10: black-queen
  11: black-rook
  12: empty
```

## Performances

**Configuration CPU Intel i7-1185G7:**
- Epoch time: ~5 minutes
- Training 10 epochs: ~45 minutes
- Training 100 epochs: ~7.5 heures

**Résultats typiques (après 10 epochs):**
- mAP50: ~78%
- mAP50-95: ~66%
- Precision: ~72%
- Recall: ~72%

## Troubleshooting

### Label Class Warnings
```
Label class 12 exceeds dataset class count 12. Possible class labels are 0-11
```
**Solution:** Ces avertissements sont normaux si certaines images ont la classe 12 (empty) mais que le fichier yaml était configuré à 12 classes au lieu de 13. L'entraînement continue correctement.

### Out of Memory
Réduire `batch_size` dans le script (actuellement 16 en mode quick).

### Slow Training
Vérifier que `workers=8` et que Intel MKL est activé.
