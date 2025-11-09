"""
Script pour créer Senchess Ultimate v1.0
Fusion des datasets Haki (1000 images) + Gear (693 images) = 1693 images
"""

import os
import shutil
from pathlib import Path
import yaml
from datetime import datetime

def create_ultimate_dataset():
    """Fusionne les datasets chess_decoder_1000 et processed pour créer un dataset ultimate"""
    
    print("\n" + "="*70)
    print("🚀 CRÉATION DU DATASET SENCHESS ULTIMATE")
    print("="*70 + "\n")
    
    base_dir = Path("data")
    
    # Chemins des datasets source
    dataset_haki = base_dir / "chess_decoder_1000"  # 1000 images
    dataset_gear = base_dir / "processed"  # 693 images
    
    # Créer le dossier ultimate
    dataset_ultimate = base_dir / "chess_ultimate_1693"
    
    if dataset_ultimate.exists():
        print(f"⚠️  Le dossier {dataset_ultimate} existe déjà.")
        response = input("   Voulez-vous le supprimer et recommencer ? (o/n): ")
        if response.lower() == 'o':
            shutil.rmtree(dataset_ultimate)
            print("   ✅ Ancien dossier supprimé")
        else:
            print("   ⏭️  Utilisation du dossier existant")
            return dataset_ultimate
    
    # Créer la structure
    print("\n📁 Création de la structure du dataset ultimate...")
    for split in ['train', 'valid', 'test']:
        (dataset_ultimate / split / 'images').mkdir(parents=True, exist_ok=True)
        (dataset_ultimate / split / 'labels').mkdir(parents=True, exist_ok=True)
    
    print("   ✅ Structure créée\n")
    
    # Copier les données de chess_decoder_1000 (Haki)
    print("📦 Copie du dataset Haki (chess_decoder_1000)...")
    stats_haki = copy_dataset(dataset_haki, dataset_ultimate, prefix="haki")
    print(f"   ✅ {stats_haki['total']} images copiées depuis Haki\n")
    
    # Copier les données de processed (Gear)
    print("📦 Copie du dataset Gear (processed)...")
    stats_gear = copy_dataset(dataset_gear, dataset_ultimate, prefix="gear")
    print(f"   ✅ {stats_gear['total']} images copiées depuis Gear\n")
    
    # Créer le fichier de configuration
    print("📝 Création du fichier data.yaml...")
    create_yaml_config(dataset_ultimate, stats_haki, stats_gear)
    print("   ✅ Fichier data.yaml créé\n")
    
    # Résumé
    total_images = stats_haki['total'] + stats_gear['total']
    print("="*70)
    print("✅ DATASET ULTIMATE CRÉÉ AVEC SUCCÈS")
    print("="*70)
    print(f"\n📊 Statistiques:")
    print(f"   Images Haki   : {stats_haki['total']}")
    print(f"   Images Gear   : {stats_gear['total']}")
    print(f"   Total         : {total_images}")
    print(f"\n   Train         : {stats_haki['train'] + stats_gear['train']}")
    print(f"   Valid         : {stats_haki['valid'] + stats_gear['valid']}")
    print(f"   Test          : {stats_haki['test'] + stats_gear['test']}")
    print(f"\n📁 Emplacement  : {dataset_ultimate}")
    print()
    
    return dataset_ultimate


def copy_dataset(source_dir, dest_dir, prefix):
    """Copie un dataset dans le dataset ultimate avec un préfixe pour éviter les collisions"""
    stats = {'train': 0, 'valid': 0, 'test': 0, 'total': 0}
    
    for split in ['train', 'valid', 'test']:
        # Essayer d'abord la structure classique (train/images)
        source_images = source_dir / split / 'images'
        source_labels = source_dir / split / 'labels'
        
        # Si ça n'existe pas, essayer images/train (structure chess_decoder_1000)
        if not source_images.exists():
            source_images = source_dir / 'images' / split
            source_labels = source_dir / 'labels' / split
        
        # Mapper 'val' à 'valid'
        if not source_images.exists() and split == 'valid':
            source_images = source_dir / 'images' / 'val'
            source_labels = source_dir / 'labels' / 'val'
        
        if not source_images.exists():
            continue
        
        dest_images = dest_dir / split / 'images'
        dest_labels = dest_dir / split / 'labels'
        
        # Copier les images
        image_files = list(source_images.glob('*.jpg')) + list(source_images.glob('*.png'))
        
        for img_file in image_files:
            # Nouveau nom avec préfixe pour éviter les collisions
            new_name = f"{prefix}_{img_file.name}"
            
            # Copier l'image
            shutil.copy2(img_file, dest_images / new_name)
            
            # Copier le label correspondant
            label_file = source_labels / f"{img_file.stem}.txt"
            if label_file.exists():
                new_label_name = f"{prefix}_{img_file.stem}.txt"
                shutil.copy2(label_file, dest_labels / new_label_name)
            
            stats[split] += 1
            stats['total'] += 1
    
    return stats


def create_yaml_config(dataset_path, stats_haki, stats_gear):
    """Crée le fichier de configuration YAML pour le dataset ultimate"""
    
    config = {
        'path': str(dataset_path.absolute()),
        'train': 'train/images',
        'val': 'valid/images',
        'test': 'test/images',
        'names': {
            0: 'bishop',
            1: 'black-bishop',
            2: 'black-king',
            3: 'black-knight',
            4: 'black-pawn',
            5: 'black-queen',
            6: 'black-rook',
            7: 'white-bishop',
            8: 'white-king',
            9: 'white-knight',
            10: 'white-pawn',
            11: 'white-queen',
            12: 'white-rook'
        }
    }
    
    yaml_path = dataset_path / 'data.yaml'
    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    
    # Créer aussi un README
    readme_content = f"""# Senchess Ultimate Dataset v1.0

## Description
Dataset fusionné combinant les datasets Haki et Gear pour créer un modèle universel
de détection de pièces d'échecs capable de reconnaître tous les styles.

## Composition
- **Dataset Haki** : {stats_haki['total']} images (diagrammes 2D générés)
- **Dataset Gear** : {stats_gear['total']} images (photos physiques 3D)
- **Total** : {stats_haki['total'] + stats_gear['total']} images

## Répartition
- Train : {stats_haki['train'] + stats_gear['train']} images
- Valid : {stats_haki['valid'] + stats_gear['valid']} images
- Test  : {stats_haki['test'] + stats_gear['test']} images

## Classes (13)
Pièces blanches et noires standard d'échecs

## Date de création
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Utilisation
Ce dataset est conçu pour entraîner Senchess Ultimate v1.0
"""
    
    readme_path = dataset_path / 'README.md'
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)


if __name__ == '__main__':
    dataset_path = create_ultimate_dataset()
    
    print("\n🎯 Prochaine étape :")
    print(f"   Entraîner le modèle avec :")
    print(f"   python train_ultimate.py")
    print()
