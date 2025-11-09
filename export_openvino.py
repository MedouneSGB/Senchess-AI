"""
Script pour exporter un modèle YOLO vers OpenVINO
OpenVINO optimise l'inférence pour les processeurs Intel (CPU + GPU Iris Xe)
"""

import os
from pathlib import Path
from ultralytics import YOLO
import argparse

def export_to_openvino(model_path: str, imgsz: int = 640, half: bool = False):
    """
    Exporte un modèle YOLO vers format OpenVINO
    
    Args:
        model_path: Chemin vers le modèle .pt à exporter
        imgsz: Taille d'image pour l'export (défaut: 640)
        half: Utiliser FP16 au lieu de FP32 (plus rapide, légèrement moins précis)
    """
    print("=" * 70)
    print("🚀 EXPORT YOLO → OpenVINO")
    print("=" * 70)
    print()
    
    # Vérifier que le modèle existe
    if not os.path.exists(model_path):
        print(f"❌ Erreur : Modèle introuvable : {model_path}")
        return False
    
    print(f"📦 Modèle source : {model_path}")
    print(f"📐 Taille d'image : {imgsz}")
    print(f"⚡ Précision : {'FP16 (half)' if half else 'FP32 (full)'}")
    print()
    
    try:
        # Charger le modèle
        print("📂 Chargement du modèle YOLO...")
        model = YOLO(model_path)
        
        # Export vers OpenVINO
        print("🔄 Export vers OpenVINO en cours...")
        print("   (Cela peut prendre 1-2 minutes...)")
        print()
        
        export_path = model.export(
            format='openvino',
            imgsz=imgsz,
            half=half,
            int8=False,  # Quantification INT8 désactivée (peut dégrader la précision)
        )
        
        print()
        print("✅ Export réussi !")
        print(f"📁 Modèle OpenVINO sauvegardé dans : {export_path}")
        print()
        
        # Afficher la structure des fichiers exportés
        export_dir = Path(export_path).parent
        print("📋 Fichiers générés :")
        for file in sorted(export_dir.glob("*")):
            if file.is_file():
                size_mb = file.stat().st_size / (1024 * 1024)
                print(f"   - {file.name} ({size_mb:.2f} MB)")
        
        print()
        print("=" * 70)
        print("🎯 PROCHAINES ÉTAPES")
        print("=" * 70)
        print()
        print("1. Tester l'inférence OpenVINO :")
        print(f"   python predict_openvino.py --model {export_path}")
        print()
        print("2. Comparer performances CPU vs GPU Intel :")
        print(f"   python benchmark_openvino.py --model {export_path}")
        print()
        print("3. Utiliser dans votre application :")
        print(f"   model = YOLO('{export_path}')")
        print("   results = model.predict('image.jpg')")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'export : {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(description="Export YOLO vers OpenVINO")
    parser.add_argument(
        '--model',
        type=str,
        default='models/senchess_intel_v1.0_quick2/weights/best.pt',
        help='Chemin vers le modèle YOLO (.pt)'
    )
    parser.add_argument(
        '--imgsz',
        type=int,
        default=640,
        help='Taille d\'image pour l\'export (défaut: 640)'
    )
    parser.add_argument(
        '--half',
        action='store_true',
        help='Utiliser FP16 (plus rapide, légèrement moins précis)'
    )
    
    args = parser.parse_args()
    
    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║                                                                  ║")
    print("║           🚀 EXPORT YOLO → OpenVINO (Intel)                     ║")
    print("║                                                                  ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print()
    print("OpenVINO optimise l'inférence pour :")
    print("  ✅ CPU Intel (avec optimisations vectorielles)")
    print("  ✅ GPU Intel Iris Xe (accélération matérielle)")
    print("  ✅ VPU Intel (Neural Compute Stick)")
    print()
    print("⚡ Gain de performance typique : 2-5x vs PyTorch CPU")
    print()
    
    success = export_to_openvino(args.model, args.imgsz, args.half)
    
    if success:
        print("✅ Export terminé avec succès !")
    else:
        print("❌ L'export a échoué")
        exit(1)


if __name__ == "__main__":
    main()
