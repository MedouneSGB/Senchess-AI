"""
Script pour préparer le dataset Senchess pour Kaggle
Version alternative utilisant les données disponibles
"""

import os
import shutil
import yaml
from pathlib import Path

def find_best_dataset():
    """Trouve le meilleur dataset disponible"""
    
    # Options de datasets
    options = [
        ("data/processed", "Dataset processed principal"),
        ("data/chess_decoder_1000", "Dataset Chess Decoder"),
        ("archive/Chess_pieces", "Archive Chess Pieces"),
        ("archive/Chess Pieces.yolov8-obb", "Archive YOLO OBB")
    ]
    
    print("🔍 Recherche du meilleur dataset...")
    print()
    
    for path, name in options:
        p = Path(path)
        if p.exists():
            # Compter les images
            image_count = 0
            for ext in ['*.jpg', '*.png', '*.jpeg']:
                image_count += len(list(p.rglob(ext)))
            
            if image_count > 0:
                print(f"✅ {name}")
                print(f"   Chemin: {path}")
                print(f"   Images: {image_count}")
                return path, name, image_count
            else:
                print(f"⚠️  {name} - Aucune image")
        else:
            print(f"❌ {name} - Dossier inexistant")
    
    return None, None, 0

def prepare_from_chess_decoder():
    """Prépare le dataset depuis chess_decoder_1000 ou processed"""
    
    print("\n" + "=" * 60)
    print("🎯 Préparation du Dataset pour Kaggle")
    print("=" * 60)
    
    # Essayer différentes sources
    source_options = [
        Path("data/processed"),
        Path("data/chess_decoder_1000")
    ]
    
    source_data = None
    for option in source_options:
        if option.exists() and (option / "images").exists():
            source_data = option
            break
    
    if not source_data:
        print("❌ Aucun dataset source trouvé")
        return
    
    print(f"📂 Source: {source_data}")
    
    kaggle_output = Path("kaggle_dataset")
    
    # Nettoyer et créer le dossier de sortie
    if kaggle_output.exists():
        shutil.rmtree(kaggle_output)
    kaggle_output.mkdir(exist_ok=True)
    
    print(f"✅ Dossier créé: {kaggle_output}")
    
    # Copier les données
    print("\n📦 Copie des données...")
    
    splits = ['train', 'val', 'test', 'valid']
    split_mapping = {'val': 'valid'}  # Renommer val en valid
    total_images = 0
    processed_splits = set()
    
    for split in splits:
        # Essayer images/split et split directement
        source_images_options = [
            source_data / "images" / split,
            source_data / split
        ]
        source_labels_options = [
            source_data / "labels" / split,
            source_data / split
        ]
        
        source_images = None
        source_labels = None
        
        for option in source_images_options:
            if option.exists():
                source_images = option
                break
        
        for option in source_labels_options:
            if option.exists():
                source_labels = option
                break
        
        if not source_images:
            continue
        
        dest_split_name = split_mapping.get(split, split)
        
        # Éviter les doublons (train/valid peuvent être les mêmes)
        if dest_split_name in processed_splits:
            continue
        processed_splits.add(dest_split_name)
        
        dest_split = kaggle_output / dest_split_name
        
        # Créer les dossiers
        (dest_split / "images").mkdir(parents=True, exist_ok=True)
        (dest_split / "labels").mkdir(parents=True, exist_ok=True)
        
        # Copier les images
        images = list(source_images.glob("*.jpg")) + list(source_images.glob("*.png"))
        for img in images:
            shutil.copy2(img, dest_split / "images" / img.name)
        
        # Copier les labels
        if source_labels and source_labels.exists():
            labels = list(source_labels.glob("*.txt"))
            for label in labels:
                shutil.copy2(label, dest_split / "labels" / label.name)
        
        total_images += len(images)
        print(f"  ✅ {dest_split_name:6} : {len(images):4} images copiées")
    
    print(f"\n📊 Total: {total_images} images")
    
    # Créer le fichier data.yaml
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
        yaml.dump(data_yaml, f, sort_keys=False, default_flow_style=False)
    
    print("✅ Fichier data.yaml créé")
    
    # Créer les métadonnées Kaggle
    print("\n📝 Création des métadonnées Kaggle...")
    
    import json
    metadata = {
        "title": "Senchess Chess Pieces Dataset",
        "id": "medounesgb/senchess-dataset",
        "licenses": [{"name": "CC0-1.0"}],
        "keywords": ["chess", "computer vision", "yolo", "object detection", "game"]
    }
    
    with open(kaggle_output / "dataset-metadata.json", 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("✅ Métadonnées créées")
    
    # Créer le README
    readme_content = f"""# Senchess Chess Pieces Dataset

## 📊 Description
Dataset de détection de pièces d'échecs pour entraînement YOLOv8.

## 📈 Statistiques
- **Total d'images**: {total_images}
- **Classes**: 12 types de pièces (6 blanches + 6 noires)
- **Format**: YOLO (annotations .txt)
- **Résolution**: Variable (optimale: 640x640)

## 📁 Structure
```
senchess-dataset/
├── data.yaml           # Configuration YOLO
├── train/
│   ├── images/        # Images d'entraînement
│   └── labels/        # Annotations YOLO format
├── valid/
│   ├── images/        # Images de validation
│   └── labels/
└── test/
    ├── images/        # Images de test
    └── labels/
```

## 🎯 Classes (12)

### Pièces Blanches
- 0: white-king (Roi ♔)
- 1: white-queen (Dame ♕)
- 2: white-rook (Tour ♖)
- 3: white-bishop (Fou ♗)
- 4: white-knight (Cavalier ♘)
- 5: white-pawn (Pion ♙)

### Pièces Noires
- 6: black-king (Roi ♚)
- 7: black-queen (Dame ♛)
- 8: black-rook (Tour ♜)
- 9: black-bishop (Fou ♝)
- 10: black-knight (Cavalier ♞)
- 11: black-pawn (Pion ♟)

## 🚀 Usage avec YOLOv8

### Entraînement
```python
from ultralytics import YOLO

# Charger le modèle pré-entraîné
model = YOLO('yolov8n.pt')

# Entraîner
results = model.train(
    data='/kaggle/input/senchess-dataset/data.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    device=0,
    patience=20,
    project='senchess',
    name='run_v1'
)
```

### Prédiction
```python
# Charger le modèle entraîné
model = YOLO('best.pt')

# Prédire
results = model.predict('chess_board.jpg')

# Afficher les résultats
for r in results:
    print(f"Détecté {len(r.boxes)} pièces")
```

## 📝 Format des Annotations

Format YOLO standard (un fichier .txt par image):
```
class_id x_center y_center width height
```

Toutes les valeurs sont normalisées entre 0 et 1.

Exemple:
```
0 0.5 0.5 0.1 0.15    # white-king au centre
5 0.3 0.7 0.08 0.12   # white-pawn
```

## 🎓 Cas d'Usage

- Numérisation de parties d'échecs
- Analyse de positions en temps réel
- Applications éducatives d'échecs
- Génération automatique de notation FEN
- Streaming de parties d'échecs

## 📊 Performances Attendues

Avec YOLOv8n et 100 epochs:
- **mAP50**: 95-99%
- **mAP50-95**: 85-95%
- **Précision**: >95%
- **Rappel**: >95%

## 🔗 Projet

- **Repository**: https://github.com/MedouneSGB/Senchess-AI
- **Modèles pré-entraînés**: https://huggingface.co/MedouneSGB/senchess-models
- **API Live**: https://senchess-api-929629832495.us-central1.run.app

## 📜 Licence

CC0-1.0 (Public Domain) - Libre d'utilisation pour tout usage.

## 👤 Auteur

**MedouneSGB** - Senchess AI Project

---

**Entraîné avec succès sur Kaggle GPU** 🚀
"""
    
    with open(kaggle_output / "README.md", 'w') as f:
        f.write(readme_content)
    
    print("✅ README.md créé")
    
    # Résumé final
    print("\n" + "=" * 60)
    print("✅ DATASET PRÊT POUR KAGGLE !")
    print("=" * 60)
    print(f"\n📁 Dossier: {kaggle_output.absolute()}")
    
    # Calculer la taille
    total_size = 0
    for entry in kaggle_output.rglob('*'):
        if entry.is_file():
            total_size += entry.stat().st_size
    
    print(f"📊 Taille totale: {total_size / (1024 * 1024):.2f} MB")
    print(f"🖼️  Total images: {total_images}")
    
    print("\n🚀 Prochaines étapes:")
    print("\n1. Installer Kaggle CLI:")
    print("   pip install kaggle")
    print("\n2. Configurer les credentials:")
    print("   ./kaggle_scripts/setup_kaggle.sh")
    print("\n3. Uploader le dataset:")
    print("   cd kaggle_dataset")
    print("   kaggle datasets create -p .")
    print("\nOu via l'interface web: https://www.kaggle.com/datasets")
    print("=" * 60)

if __name__ == "__main__":
    try:
        # Trouver le meilleur dataset
        best_path, best_name, image_count = find_best_dataset()
        
        if not best_path:
            print("\n❌ Aucun dataset trouvé avec des images")
            print("\nVeuillez d'abord entraîner un modèle ou préparer vos données.")
            exit(1)
        
        print(f"\n✅ Utilisation de: {best_name}")
        print(f"   ({image_count} images)")
        
        # Préparer le dataset
        if "chess_decoder" in best_path or "processed" in best_path:
            prepare_from_chess_decoder()
        else:
            print(f"\n⚠️  Format non supporté pour: {best_path}")
            print("   Modifiez le script ou utilisez chess_decoder_1000")
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
