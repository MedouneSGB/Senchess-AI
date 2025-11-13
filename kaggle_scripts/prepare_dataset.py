"""
Script pour préparer le dataset Senchess pour upload sur Kaggle
"""

import os
import shutil
import yaml
from pathlib import Path

def create_kaggle_dataset():
    """Prépare le dataset pour Kaggle"""
    
    print("=" * 60)
    print("🎯 Préparation du Dataset pour Kaggle")
    print("=" * 60)
    
    # Dossiers source
    source_data = Path("data/processed")
    kaggle_output = Path("kaggle_dataset")
    
    # Créer le dossier de sortie
    if kaggle_output.exists():
        print(f"⚠️  Le dossier {kaggle_output} existe déjà. Suppression...")
        shutil.rmtree(kaggle_output)
    
    kaggle_output.mkdir(exist_ok=True)
    print(f"✅ Dossier créé: {kaggle_output}")
    
    # Copier les données
    print("\n📦 Copie des données...")
    
    splits = ['train', 'valid', 'test']
    total_images = 0
    
    for split in splits:
        source_split = source_data / "images" / split
        dest_split = kaggle_output / split
        
        if not source_split.exists():
            print(f"⚠️  Dossier manquant: {source_split}")
            continue
        
        # Créer les dossiers images et labels
        (dest_split / "images").mkdir(parents=True, exist_ok=True)
        (dest_split / "labels").mkdir(parents=True, exist_ok=True)
        
        # Copier les images
        images = list(source_split.glob("*.jpg")) + list(source_split.glob("*.png"))
        for img in images:
            shutil.copy2(img, dest_split / "images" / img.name)
        
        # Copier les labels
        source_labels = source_data / "labels" / split
        if source_labels.exists():
            labels = list(source_labels.glob("*.txt"))
            for label in labels:
                shutil.copy2(label, dest_split / "labels" / label.name)
        
        total_images += len(images)
        print(f"  ✅ {split:6} : {len(images):4} images copiées")
    
    print(f"\n📊 Total: {total_images} images")
    
    # Créer le fichier data.yaml pour YOLO
    print("\n📝 Création du fichier data.yaml...")
    
    data_yaml = {
        'path': '/kaggle/input/senchess-dataset',
        'train': 'train/images',
        'val': 'valid/images',
        'test': 'test/images',
        'names': {
            0: 'white-king',
            1: 'white-queen',
            2: 'white-rook',
            3: 'white-bishop',
            4: 'white-knight',
            5: 'white-pawn',
            6: 'black-king',
            7: 'black-queen',
            8: 'black-rook',
            9: 'black-bishop',
            10: 'black-knight',
            11: 'black-pawn'
        },
        'nc': 12
    }
    
    with open(kaggle_output / "data.yaml", 'w') as f:
        yaml.dump(data_yaml, f, sort_keys=False)
    
    print("✅ Fichier data.yaml créé")
    
    # Créer le dataset-metadata.json pour Kaggle
    print("\n📝 Création des métadonnées Kaggle...")
    
    metadata = {
        "title": "Senchess Chess Pieces Dataset",
        "id": "medounesgb/senchess-dataset",
        "licenses": [{"name": "CC0-1.0"}],
        "keywords": ["chess", "computer vision", "yolo", "object detection"]
    }
    
    import json
    with open(kaggle_output / "dataset-metadata.json", 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("✅ Métadonnées créées")
    
    # Créer un README pour le dataset
    readme_content = f"""# Senchess Chess Pieces Dataset

## Description
Dataset de détection de pièces d'échecs pour entraînement YOLOv8.

## Statistiques
- **Total d'images**: {total_images}
- **Classes**: 12 (6 pièces blanches + 6 pièces noires)
- **Format**: YOLO (txt annotations)

## Structure
```
senchess-dataset/
├── data.yaml           # Configuration YOLO
├── train/
│   ├── images/        # Images d'entraînement
│   └── labels/        # Annotations YOLO
├── valid/
│   ├── images/        # Images de validation
│   └── labels/
└── test/
    ├── images/        # Images de test
    └── labels/
```

## Classes
0. white-king
1. white-queen
2. white-rook
3. white-bishop
4. white-knight
5. white-pawn
6. black-king
7. black-queen
8. black-rook
9. black-bishop
10. black-knight
11. black-pawn

## Usage avec YOLOv8
```python
from ultralytics import YOLO

# Charger le modèle
model = YOLO('yolov8n.pt')

# Entraîner
results = model.train(
    data='/kaggle/input/senchess-dataset/data.yaml',
    epochs=100,
    imgsz=640,
    batch=16
)
```

## Licence
CC0-1.0 (Public Domain)

## Auteur
MedouneSGB - Senchess AI Project
"""
    
    with open(kaggle_output / "README.md", 'w') as f:
        f.write(readme_content)
    
    print("✅ README.md créé")
    
    # Afficher le résumé
    print("\n" + "=" * 60)
    print("✅ DATASET PRÊT POUR KAGGLE !")
    print("=" * 60)
    print(f"\n📁 Dossier: {kaggle_output.absolute()}")
    print(f"📊 Taille totale: {get_dir_size(kaggle_output):.2f} MB")
    
    print("\n🚀 Prochaines étapes:")
    print("1. Installer Kaggle CLI:")
    print("   pip install kaggle")
    print("\n2. Configurer les credentials:")
    print("   - Téléchargez kaggle.json depuis https://www.kaggle.com/settings")
    print("   - Placez-le dans ~/.kaggle/kaggle.json")
    print("   - chmod 600 ~/.kaggle/kaggle.json")
    print("\n3. Uploader le dataset:")
    print(f"   cd {kaggle_output}")
    print("   kaggle datasets create -p .")
    print("\nOu utilisez l'interface web: https://www.kaggle.com/datasets")
    print("=" * 60)

def get_dir_size(path):
    """Calcule la taille d'un dossier en MB"""
    total = 0
    for entry in Path(path).rglob('*'):
        if entry.is_file():
            total += entry.stat().st_size
    return total / (1024 * 1024)

if __name__ == "__main__":
    try:
        create_kaggle_dataset()
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
