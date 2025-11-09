"""
Script de fine-tuning pour créer Senchess Gear-Haki Ultimate
Combine les datasets et fine-tune depuis le meilleur modèle
"""
import argparse
from pathlib import Path
from ultralytics import YOLO
import yaml
import shutil
from datetime import datetime


def merge_datasets(gear_path, haki_path, output_path):
    """
    Fusionne les datasets Gear et Haki
    
    Args:
        gear_path: Chemin vers dataset Gear (processed)
        haki_path: Chemin vers dataset Haki (chess_decoder_1000)
        output_path: Chemin de sortie pour dataset fusionné
    """
    print("\n" + "="*70)
    print("📦 FUSION DES DATASETS")
    print("="*70)
    
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Créer la structure
    for split in ['train', 'val', 'test']:
        (output_path / 'images' / split).mkdir(parents=True, exist_ok=True)
        (output_path / 'labels' / split).mkdir(parents=True, exist_ok=True)
    
    total_copied = 0
    
    # Copier Gear dataset
    print("\n🥈 Copie dataset Gear (photos physiques)...")
    gear_path = Path(gear_path)
    
    # Gear: train -> train, valid -> val, test -> test
    gear_mapping = {
        'train': 'train',
        'valid': 'val',
        'test': 'test'
    }
    
    for gear_split, output_split in gear_mapping.items():
        gear_images = gear_path / gear_split / 'images'
        gear_labels = gear_path / gear_split / 'labels'
        
        if gear_images.exists():
            images = list(gear_images.glob('*.jpg'))
            for img in images:
                # Copier image avec préfixe 'gear_'
                new_name = f"gear_{img.name}"
                shutil.copy(img, output_path / 'images' / output_split / new_name)
                
                # Copier label correspondant
                label = gear_labels / f"{img.stem}.txt"
                if label.exists():
                    shutil.copy(label, output_path / 'labels' / output_split / f"gear_{label.name}")
                
                total_copied += 1
            
            print(f"  {gear_split:6} -> {output_split:5} : {len(images)} images")
    
    # Copier Haki dataset
    print("\n🥇 Copie dataset Haki (diagrammes 2D)...")
    haki_path = Path(haki_path)
    
    # Haki: train -> train, val -> val, test -> test
    for split in ['train', 'val', 'test']:
        haki_images = haki_path / 'images' / split
        haki_labels = haki_path / 'labels' / split
        
        if haki_images.exists():
            images = list(haki_images.glob('*.png')) + list(haki_images.glob('*.jpg'))
            for img in images:
                # Copier image avec préfixe 'haki_'
                new_name = f"haki_{img.name}"
                shutil.copy(img, output_path / 'images' / split / new_name)
                
                # Copier label correspondant
                label = haki_labels / f"{img.stem}.txt"
                if label.exists():
                    shutil.copy(label, output_path / 'labels' / split / f"haki_{label.name}")
                
                total_copied += 1
            
            print(f"  {split:6} -> {split:5} : {len(images)} images")
    
    # Créer data.yaml
    data_yaml = {
        'path': str(output_path.absolute()),
        'train': 'images/train',
        'val': 'images/val',
        'test': 'images/test',
        'nc': 13,
        'names': [
            'black-bishop', 'black-king', 'black-knight', 'black-pawn',
            'black-queen', 'black-rook', 'white-bishop', 'white-king',
            'white-knight', 'white-pawn', 'white-queen', 'white-rook',
            'chessboard'
        ]
    }
    
    with open(output_path / 'data.yaml', 'w') as f:
        yaml.dump(data_yaml, f, default_flow_style=False)
    
    print(f"\n✅ Dataset fusionné créé : {output_path}")
    print(f"   Total : {total_copied} fichiers copiés")
    
    # Statistiques
    train_count = len(list((output_path / 'images' / 'train').glob('*')))
    val_count = len(list((output_path / 'images' / 'val').glob('*')))
    test_count = len(list((output_path / 'images' / 'test').glob('*')))
    
    print(f"\n📊 Répartition finale :")
    print(f"   Train : {train_count} images")
    print(f"   Val   : {val_count} images")
    print(f"   Test  : {test_count} images")
    print(f"   TOTAL : {train_count + val_count + test_count} images")
    
    return output_path / 'data.yaml'


def finetune_model(base_model, data_yaml, epochs, lr0, project_name):
    """
    Fine-tune un modèle existant
    
    Args:
        base_model: Chemin vers le modèle de base
        data_yaml: Chemin vers data.yaml
        epochs: Nombre d'epochs
        lr0: Learning rate initial
        project_name: Nom du projet/modèle
    """
    print("\n" + "="*70)
    print("🚀 FINE-TUNING DU MODÈLE")
    print("="*70)
    
    print(f"\nModèle de base : {base_model}")
    print(f"Dataset        : {data_yaml}")
    print(f"Epochs         : {epochs}")
    print(f"Learning rate  : {lr0}")
    print(f"Nom du projet  : {project_name}")
    
    # Charger le modèle
    print("\n📥 Chargement du modèle de base...")
    model = YOLO(base_model)
    
    # Configuration d'entraînement
    print("\n🏋️  Début du fine-tuning...\n")
    
    results = model.train(
        data=str(data_yaml),
        epochs=epochs,
        imgsz=640,
        batch=8,
        lr0=lr0,
        lrf=0.01,
        momentum=0.937,
        weight_decay=0.0005,
        warmup_epochs=3,
        warmup_momentum=0.8,
        warmup_bias_lr=0.1,
        box=7.5,
        cls=0.5,
        dfl=1.5,
        project='models',
        name=project_name,
        exist_ok=True,
        pretrained=True,
        optimizer='SGD',
        verbose=True,
        seed=0,
        deterministic=True,
        single_cls=False,
        rect=False,
        cos_lr=False,
        close_mosaic=10,
        resume=False,
        amp=True,
        fraction=1.0,
        profile=False,
        freeze=None,
        multi_scale=False,
        overlap_mask=True,
        mask_ratio=4,
        dropout=0.0,
        val=True,
        save=True,
        save_period=-1,
        cache=False,
        device='cpu',
        workers=4,
        plots=True,
        label_smoothing=0.0,
        patience=50,
        augment=True,
        hsv_h=0.015,
        hsv_s=0.7,
        hsv_v=0.4,
        degrees=0.0,
        translate=0.1,
        scale=0.5,
        shear=0.0,
        perspective=0.0,
        flipud=0.0,
        fliplr=0.5,
        mosaic=1.0,
        mixup=0.0,
        copy_paste=0.0
    )
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Fine-tuning Senchess Gear-Haki")
    
    # Chemins datasets
    parser.add_argument('--gear-data', type=str, 
                       default='data/processed',
                       help='Chemin dataset Gear')
    parser.add_argument('--haki-data', type=str,
                       default='data/chess_decoder_1000',
                       help='Chemin dataset Haki')
    parser.add_argument('--output-data', type=str,
                       default='data/gear_haki_merged',
                       help='Chemin dataset fusionné')
    
    # Modèle de base
    parser.add_argument('--base-model', type=str,
                       default='models/senchess_haki_v1.0/weights/best.pt',
                       help='Modèle de base pour fine-tuning (haki par défaut)')
    
    # Hyperparamètres
    parser.add_argument('--epochs', type=int, default=50,
                       help='Nombre d\'epochs (défaut: 50)')
    parser.add_argument('--lr0', type=float, default=0.001,
                       help='Learning rate initial (défaut: 0.001)')
    
    # Nom du projet
    parser.add_argument('--name', type=str,
                       default='senchess_gear_haki_finetune',
                       help='Nom du modèle')
    
    # Options
    parser.add_argument('--skip-merge', action='store_true',
                       help='Skip dataset merge (utilise dataset existant)')
    
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("🎯 SENCHESS GEAR-HAKI FINE-TUNING")
    print("="*70)
    print(f"\nDate : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Stratégie : Fine-tune depuis {Path(args.base_model).stem}")
    print(f"Objectif  : Modèle universel 2D + 3D")
    
    # Étape 1 : Fusion des datasets (si nécessaire)
    if not args.skip_merge:
        data_yaml = merge_datasets(
            args.gear_data,
            args.haki_data,
            args.output_data
        )
    else:
        data_yaml = Path(args.output_data) / 'data.yaml'
        print(f"\n⏭️  Fusion skippée, utilisation de : {data_yaml}")
    
    # Étape 2 : Fine-tuning
    results = finetune_model(
        args.base_model,
        data_yaml,
        args.epochs,
        args.lr0,
        args.name
    )
    
    # Résultats finaux
    print("\n" + "="*70)
    print("✅ FINE-TUNING TERMINÉ")
    print("="*70)
    
    model_path = Path('models') / args.name / 'weights' / 'best.pt'
    print(f"\n📦 Modèle sauvegardé : {model_path}")
    print(f"📊 Résultats : models/{args.name}/results.csv")
    print(f"📈 Courbes : models/{args.name}/results.png")
    
    print("\n💡 Pour évaluer le modèle :")
    print(f"   python src/evaluate.py --model {model_path}")
    print(f"\n💡 Pour prédire :")
    print(f"   python src/predict.py --model {model_path} --source imgTest/")
    
    print("\n🎉 Fine-tuning Gear-Haki complété !")


if __name__ == '__main__':
    main()
