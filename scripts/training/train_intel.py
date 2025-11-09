"""
Script d'entraînement optimisé pour GPU Intel Iris Xe
Utilise les optimisations CPU Intel (plus stable que XPU pour l'instant)
"""

import os
from pathlib import Path
from ultralytics import YOLO
from datetime import datetime
import yaml
import torch

def train_with_intel_optimization():
    """Entraîne le modèle avec optimisations Intel"""
    
    print("\n" + "="*70)
    print("🚀 ENTRAÎNEMENT OPTIMISÉ POUR INTEL IRIS XE")
    print("="*70 + "\n")
    
    # Vérifier le dataset
    dataset_path = Path("data/chess_dataset_1000")
    data_yaml = dataset_path / "data.yaml"
    
    if not data_yaml.exists():
        print("❌ Le fichier data.yaml n'existe pas !")
        return
    
    # Activer les optimisations Intel
    print("⚡ Activation des optimisations Intel MKL...")
    os.environ['OMP_NUM_THREADS'] = '8'  # Utiliser tous les threads
    os.environ['MKL_NUM_THREADS'] = '8'
    torch.set_num_threads(8)
    
    # Vérifier PyTorch
    print(f"📦 PyTorch version : {torch.__version__}")
    print(f"🖥️  Device : CPU (optimisé Intel)")
    print(f"🧵 Threads : {torch.get_num_threads()}")
    
    # Vérifier si IPEX est disponible
    try:
        import intel_extension_for_pytorch as ipex
        print(f"✅ Intel Extension : {ipex.__version__}")
        has_ipex = True
    except ImportError:
        print("ℹ️  Intel Extension non installé (optionnel)")
        has_ipex = False
    
    print()
    
    # Configuration optimisée pour Intel
    config = {
        'model': 'yolov8n.pt',
        'data': str(data_yaml),
        'epochs': 100,
        'batch': 8,  # Batch optimal pour CPU Intel
        'imgsz': 640,
        'patience': 50,
        'project': 'models',
        'name': 'senchess_intel_v1.0',
        'device': 'cpu',
        'workers': 8,  # Utiliser tous les workers
        'optimizer': 'Adam',  # Adam est souvent plus rapide sur CPU
        'lr0': 0.001,
        'lrf': 0.01,
        'momentum': 0.9,
        'weight_decay': 0.0005,
        'warmup_epochs': 3.0,
        'amp': False,  # Désactiver AMP sur CPU
        'val': True,
        'save': True,
        'save_period': 10,
        'plots': True,
        'verbose': True
    }
    
    print("📋 Configuration de l'entraînement :")
    print(f"   Dataset         : chess_dataset_1000 (13 classes)")
    print(f"   Modèle          : {config['model']}")
    print(f"   Époques         : {config['epochs']}")
    print(f"   Batch size      : {config['batch']}")
    print(f"   Workers         : {config['workers']}")
    print(f"   Optimizer       : {config['optimizer']}")
    print()
    
    print("⏱️  Temps estimé : 4-6 heures avec optimisations Intel")
    print()
    
    response = input("Commencer l'entraînement ? (o/n): ")
    
    if response.lower() != 'o':
        print("❌ Annulé")
        return
    
    # Charger et optimiser le modèle
    print("\n🔄 Chargement du modèle...")
    model = YOLO(config['model'])
    
    # Appliquer IPEX si disponible
    if has_ipex:
        print("⚡ Application des optimisations IPEX...")
        try:
            import intel_extension_for_pytorch as ipex
            model = ipex.optimize(model, dtype=torch.float32)
        except Exception as e:
            print(f"⚠️  IPEX non appliqué : {e}")
    
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
            amp=config['amp'],
            val=config['val'],
            save=config['save'],
            save_period=config['save_period'],
            plots=config['plots'],
            verbose=config['verbose']
        )
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        print("\n" + "="*70)
        print("✅ ENTRAÎNEMENT TERMINÉ !")
        print("="*70)
        print(f"\n⏱️  Durée : {duration}")
        print(f"📁 Modèle : models/{config['name']}/weights/best.pt")
        
        # Sauvegarder les infos
        model_dir = Path('models') / config['name']
        info_file = model_dir / 'training_info.yaml'
        
        info = {
            'model_name': 'Senchess Intel v1.0',
            'version': '1.0',
            'hardware': 'Intel Iris Xe Graphics (CPU optimized)',
            'dataset': 'chess_dataset_1000',
            'num_classes': 13,
            'training_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'duration': str(duration),
            'config': config
        }
        
        with open(info_file, 'w', encoding='utf-8') as f:
            yaml.dump(info, f, default_flow_style=False, allow_unicode=True)
        
        print(f"💾 Infos sauvegardées : {info_file}")
        print("\n🎯 Testez le modèle avec : python test_models.py")
        print()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrompu")
    except Exception as e:
        print(f"\n\n❌ Erreur : {e}")
        import traceback
        traceback.print_exc()


def quick_train():
    """Test rapide (10 epochs)"""
    
    print("\n" + "="*70)
    print("⚡ ENTRAÎNEMENT RAPIDE (10 EPOCHS)")
    print("="*70 + "\n")
    
    dataset_path = Path("data/chess_dataset_1000")
    data_yaml = dataset_path / "data.yaml"
    
    if not data_yaml.exists():
        print("❌ data.yaml introuvable")
        return
    
    # Optimisations Intel
    os.environ['OMP_NUM_THREADS'] = '8'
    os.environ['MKL_NUM_THREADS'] = '8'
    torch.set_num_threads(8)
    
    model = YOLO('yolov8n.pt')
    
    print("🏋️  Entraînement rapide...\n")
    
    try:
        results = model.train(
            data=str(data_yaml),
            epochs=10,
            batch=8,
            imgsz=640,
            project='models',
            name='senchess_intel_v1.0_quick',
            device='cpu',
            workers=8,
            amp=False,
            verbose=True
        )
        
        print("\n✅ Terminé !")
        print("📁 Modèle : models/senchess_intel_v1.0_quick/weights/best.pt")
    
    except Exception as e:
        print(f"\n❌ Erreur : {e}")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description="Entraîner avec optimisations Intel")
    parser.add_argument('--quick', action='store_true', help="Test rapide (10 epochs)")
    
    args = parser.parse_args()
    
    if args.quick:
        quick_train()
    else:
        train_with_intel_optimization()
