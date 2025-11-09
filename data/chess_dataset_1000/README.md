# Dataset d'Échecs pour Détection d'Objets

## Structure

```
dataset/
├── images/
│   ├── train/    # Images d'entraînement
│   ├── val/      # Images de validation
│   └── test/     # Images de test
├── labels/
│   ├── train/    # Annotations YOLO (.txt)
│   ├── val/
│   └── test/
├── classes.txt   # Liste des classes
└── dataset.yaml  # Configuration YOLO
```

## Statistiques

- **Total d'images**: 1000
- **Entraînement**: 800 (80%)
- **Validation**: 100 (10%)
- **Test**: 99 (10%)
- **Nombre de classes**: 13

## Classes

0. empty (case vide)
1. white_king
2. white_queen
3. white_rook
4. white_bishop
5. white_knight
6. white_pawn
7. black_king
8. black_queen
9. black_rook
10. black_bishop
11. black_knight
12. black_pawn

## Utilisation avec YOLO

```python
from ultralytics import YOLO

# Charger un modèle
model = YOLO('yolov8n.pt')

# Entraîner
model.train(data='dataset.yaml', epochs=100, imgsz=640)
```
