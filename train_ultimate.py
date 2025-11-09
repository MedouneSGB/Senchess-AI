"""
Script d'entraînement pour Senchess Ultimate v1.0
Modèle universel combinant Haki + Gear
"""

import os
from pathlib import Path
from ultralytics import YOLO
from datetime import datetime
import yaml
import torch

def train_ultimate_model():
    """Entraîne le modèle Senchess Ultimate v1.0"""
    
    print("\n" + "="*70)
    print("🚀 ENTRAÎNEMENT DE SENCHESS ULTIMATE V1.0")
    print("="*70 + "\n")
    
    # Vérifier que le dataset existe
    dataset_path = Path("data/chess_ultimate_1693")
    if not dataset_path.exists():
        print("❌ Le dataset ultimate n'existe pas encore !")
        print("   Exécutez d'abord : python create_ultimate_dataset.py")
        return
    
    # Détecter le device (GPU ou CPU)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    gpu_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "N/A"
    
    print(f"🖥️  Device détecté : {device.upper()}")
    if device == 'cuda':
        print(f"   GPU : {gpu_name}")
        print(f"   CUDA Version : {torch.version.cuda}")
    else:
        print("   ⚠️  Aucun GPU détecté, utilisation du CPU")
    print()
    
    # Configuration de l'entraînement
    config = {
        'model': 'yolov8n.pt',  # Modèle de base
        'data': str(dataset_path / 'data.yaml'),
        'epochs': 50,  # Plus d'époques pour un meilleur apprentissage
        'batch': 16 if device == 'cuda' else 8,  # Batch plus grand avec GPU
        'imgsz': 640,
        'patience': 100,
        'project': 'models',
        'name': 'senchess_ultimate_v1.0',
        'device': device,  # Utilisation automatique du GPU si disponible
        'workers': 8,
        'optimizer': 'auto',
        'lr0': 0.01,
        'lrf': 0.01,
        'momentum': 0.937,
        'weight_decay': 0.0005,
        'warmup_epochs': 3.0,
        'cos_lr': False,
        'close_mosaic': 10,
        'val': True,
        'save': True,
        'plots': True,
        'verbose': True
    }
    
    print("📋 Configuration de l'entraînement :")
    print(f"   Modèle de base  : {config['model']}")
    print(f"   Dataset         : {dataset_path.name}")
    print(f"   Époques         : {config['epochs']}")
    print(f"   Batch size      : {config['batch']}")
    print(f"   Image size      : {config['imgsz']}")
    print(f"   Device          : {config['device']}")
    print(f"   Nom du projet   : {config['name']}")
    print()
    
    # Demander confirmation
    estimated_time = "8-15 heures (CPU) / 30-90 minutes (GPU)" if device == 'cpu' else "30-90 minutes avec GPU"
    print(f"⏱️  Temps estimé d'entraînement : {estimated_time}")
    print()
    response = input("Voulez-vous commencer l'entraînement ? (o/n): ")
    
    if response.lower() != 'o':
        print("❌ Entraînement annulé")
        return
    
    # Charger le modèle de base
    print("\n🔄 Chargement du modèle YOLOv8n...")
    model = YOLO(config['model'])
    
    # Lancer l'entraînement
    print("\n🏋️  Début de l'entraînement...\n")
    start_time = datetime.now()
    
    try:
        results = model.train(
            data=config['data'],
            epochs=config['epochs'],
            batch=config['batch'],
            imgsz=config['imgsz'],
            patience=config['patience'],
            project=config['project'],
            name=config['name'],
            device=config['device'],
            workers=config['workers'],
            optimizer=config['optimizer'],
            lr0=config['lr0'],
            lrf=config['lrf'],
            momentum=config['momentum'],
            weight_decay=config['weight_decay'],
            warmup_epochs=config['warmup_epochs'],
            cos_lr=config['cos_lr'],
            close_mosaic=config['close_mosaic'],
            val=config['val'],
            save=config['save'],
            plots=config['plots'],
            verbose=config['verbose']
        )
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        print("\n" + "="*70)
        print("✅ ENTRAÎNEMENT TERMINÉ AVEC SUCCÈS !")
        print("="*70)
        print(f"\n⏱️  Durée totale : {duration}")
        print(f"📁 Modèle sauvegardé dans : models/{config['name']}/weights/best.pt")
        print(f"📊 Résultats dans : models/{config['name']}/")
        
        # Sauvegarder les infos d'entraînement
        save_training_info(config, duration, results)
        
        print("\n🎯 Prochaines étapes :")
        print("   1. Évaluer le modèle : python src/evaluate.py --model models/senchess_ultimate_v1.0/weights/best.pt")
        print("   2. Tester le modèle : python test_models.py")
        print("   3. Mettre à jour MODEL_CONFIG.yaml avec les nouvelles métriques")
        print()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Entraînement interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n\n❌ Erreur pendant l'entraînement : {e}")


def save_training_info(config, duration, results):
    """Sauvegarde les informations d'entraînement"""
    
    model_dir = Path('models') / config['name']
    info_file = model_dir / 'training_info.yaml'
    
    info = {
        'model_name': 'Senchess Ultimate v1.0',
        'version': '1.0',
        'base_model': config['model'],
        'dataset': 'chess_ultimate_1693',
        'training_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'duration': str(duration),
        'config': config,
        'description': 'Modèle universel combinant Haki (1000 images) + Gear (693 images)'
    }
    
    with open(info_file, 'w', encoding='utf-8') as f:
        yaml.dump(info, f, default_flow_style=False, allow_unicode=True)
    
    print(f"\n💾 Informations d'entraînement sauvegardées : {info_file}")


def quick_train():
    """Version rapide pour tester (10 epochs seulement)"""
    
    print("\n" + "="*70)
    print("⚡ ENTRAÎNEMENT RAPIDE DE SENCHESS ULTIMATE V1.0 (TEST)")
    print("="*70 + "\n")
    
    dataset_path = Path("data/chess_ultimate_1693")
    if not dataset_path.exists():
        print("❌ Le dataset ultimate n'existe pas encore !")
        print("   Exécutez d'abord : python create_ultimate_dataset.py")
        return
    
    # Détecter le device (GPU ou CPU)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"🖥️  Device : {device.upper()}")
    if device == 'cuda':
        print(f"   GPU : {torch.cuda.get_device_name(0)}")
    print()
    
    model = YOLO('yolov8n.pt')
    
    print("🏋️  Entraînement rapide (10 epochs)...\n")
    
    results = model.train(
        data=str(dataset_path / 'data.yaml'),
        epochs=10,
        batch=16 if device == 'cuda' else 8,
        imgsz=640,
        project='models',
        name='senchess_ultimate_v1.0_quick',
        device=device,
        workers=8,
        verbose=True
    )
    
    print("\n✅ Entraînement rapide terminé !")
    print(f"📁 Modèle : models/senchess_ultimate_v1.0_quick/weights/best.pt")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description="Entraîner Senchess Ultimate v1.0")
    parser.add_argument('--quick', action='store_true', help="Entraînement rapide (10 epochs)")
    
    args = parser.parse_args()
    
    if args.quick:
        quick_train()
    else:
        train_ultimate_model()
