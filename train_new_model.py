"""
Script d'entraînement pour Senchess GPU v1.0
Utilise le dataset chess_dataset_1000 avec support GPU
"""

import os
from pathlib import Path
from ultralytics import YOLO
from datetime import datetime
import yaml
import torch

def train_new_model():
    """Entraîne un nouveau modèle avec support GPU"""
    
    print("\n" + "="*70)
    print("🚀 ENTRAÎNEMENT DE SENCHESS GPU V1.0")
    print("="*70 + "\n")
    
    # Vérifier que le dataset existe
    dataset_path = Path("data/chess_dataset_1000")
    data_yaml = dataset_path / "data.yaml"
    
    if not data_yaml.exists():
        print("❌ Le fichier data.yaml n'existe pas !")
        print(f"   Chemin attendu : {data_yaml}")
        return
    
    # Détecter le device (GPU ou CPU)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    gpu_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "N/A"
    
    print(f"🖥️  Device détecté : {device.upper()}")
    if device == 'cuda':
        print(f"   GPU : {gpu_name}")
        print(f"   CUDA Version : {torch.version.cuda}")
        # Afficher la mémoire GPU disponible
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        print(f"   Mémoire GPU : {gpu_memory:.2f} GB")
    else:
        print("   ⚠️  Aucun GPU détecté, utilisation du CPU")
        print("   💡 Pour utiliser le GPU, exécutez : python install_gpu.py")
    print()
    
    # Configuration de l'entraînement
    config = {
        'model': 'yolov8n.pt',  # Modèle de base (nano - rapide)
        'data': str(data_yaml),
        'epochs': 100,  # Nombre d'époques
        'batch': 16 if device == 'cuda' else 8,  # Batch plus grand avec GPU
        'imgsz': 640,  # Taille des images
        'patience': 50,  # Early stopping
        'project': 'models',
        'name': 'senchess_gpu_v1.0',
        'device': device,  # Utilisation automatique du GPU si disponible
        'workers': 8,
        'optimizer': 'auto',
        'lr0': 0.01,  # Learning rate initial
        'lrf': 0.01,  # Learning rate final
        'momentum': 0.937,
        'weight_decay': 0.0005,
        'warmup_epochs': 3.0,
        'cos_lr': False,
        'close_mosaic': 10,
        'val': True,
        'save': True,
        'save_period': 10,  # Sauvegarder tous les 10 epochs
        'plots': True,
        'verbose': True
    }
    
    print("📋 Configuration de l'entraînement :")
    print(f"   Dataset         : chess_dataset_1000 (13 classes)")
    print(f"   Modèle de base  : {config['model']}")
    print(f"   Époques         : {config['epochs']}")
    print(f"   Batch size      : {config['batch']}")
    print(f"   Image size      : {config['imgsz']}")
    print(f"   Device          : {config['device']}")
    print(f"   Patience        : {config['patience']} (early stopping)")
    print(f"   Nom du modèle   : {config['name']}")
    print()
    
    # Estimation du temps
    if device == 'cuda':
        estimated_time = "45-90 minutes avec GPU"
    else:
        estimated_time = "6-10 heures avec CPU"
    
    print(f"⏱️  Temps estimé : {estimated_time}")
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
            save_period=config['save_period'],
            plots=config['plots'],
            verbose=config['verbose']
        )
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        print("\n" + "="*70)
        print("✅ ENTRAÎNEMENT TERMINÉ AVEC SUCCÈS !")
        print("="*70)
        print(f"\n⏱️  Durée totale : {duration}")
        print(f"📁 Modèle sauvegardé : models/{config['name']}/weights/best.pt")
        print(f"📊 Résultats : models/{config['name']}/")
        
        # Sauvegarder les infos d'entraînement
        save_training_info(config, duration, results)
        
        print("\n🎯 Prochaines étapes :")
        print("   1. Tester le modèle : python test_models.py")
        print("   2. Faire des prédictions : python src/predict.py")
        print()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Entraînement interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n\n❌ Erreur pendant l'entraînement : {e}")
        import traceback
        traceback.print_exc()


def save_training_info(config, duration, results):
    """Sauvegarde les informations d'entraînement"""
    
    model_dir = Path('models') / config['name']
    info_file = model_dir / 'training_info.yaml'
    
    info = {
        'model_name': 'Senchess GPU v1.0',
        'version': '1.0',
        'base_model': config['model'],
        'dataset': 'chess_dataset_1000',
        'num_classes': 13,
        'training_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'duration': str(duration),
        'device': config['device'],
        'config': config,
        'description': 'Modèle entraîné avec le dataset chess_dataset_1000 (13 classes) avec support GPU'
    }
    
    with open(info_file, 'w', encoding='utf-8') as f:
        yaml.dump(info, f, default_flow_style=False, allow_unicode=True)
    
    print(f"\n💾 Informations sauvegardées : {info_file}")


def quick_train():
    """Version rapide pour tester (10 epochs seulement)"""
    
    print("\n" + "="*70)
    print("⚡ ENTRAÎNEMENT RAPIDE (TEST) - 10 EPOCHS")
    print("="*70 + "\n")
    
    dataset_path = Path("data/chess_dataset_1000")
    data_yaml = dataset_path / "data.yaml"
    
    if not data_yaml.exists():
        print("❌ Le fichier data.yaml n'existe pas !")
        return
    
    # Détecter le device (GPU ou CPU)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"🖥️  Device : {device.upper()}")
    if device == 'cuda':
        print(f"   GPU : {torch.cuda.get_device_name(0)}")
    print()
    
    model = YOLO('yolov8n.pt')
    
    print("🏋️  Entraînement rapide (10 epochs)...\n")
    
    try:
        results = model.train(
            data=str(data_yaml),
            epochs=10,
            batch=16 if device == 'cuda' else 8,
            imgsz=640,
            project='models',
            name='senchess_gpu_v1.0_quick',
            device=device,
            workers=8,
            verbose=True
        )
        
        print("\n✅ Entraînement rapide terminé !")
        print(f"📁 Modèle : models/senchess_gpu_v1.0_quick/weights/best.pt")
    
    except Exception as e:
        print(f"\n❌ Erreur : {e}")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description="Entraîner Senchess GPU v1.0")
    parser.add_argument('--quick', action='store_true', help="Entraînement rapide (10 epochs)")
    
    args = parser.parse_args()
    
    if args.quick:
        quick_train()
    else:
        train_new_model()
