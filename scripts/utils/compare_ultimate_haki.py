"""
Comparaison détaillée Ultimate vs Haki
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from src.model_manager import SenchessModelManager
from ultralytics import YOLO

def compare_ultimate_haki():
    """Compare en détail Ultimate et Haki"""
    
    print("\n" + "="*80)
    print("⚔️  DUEL : ULTIMATE vs HAKI")
    print("="*80 + "\n")
    
    # Charger les modèles
    manager = SenchessModelManager()
    
    print("⏳ Chargement des modèles...\n")
    model_haki = manager.load_model('haki')
    model_ultimate = YOLO("models/senchess_ultimate_v1.0_quick/weights/best.pt")
    print()
    
    # Images de test
    test_dir = Path("examples/imgTest")
    images = sorted(list(test_dir.glob("*.png")) + list(test_dir.glob("*.jpg")))
    
    print(f"📁 {len(images)} images à tester\n")
    print("="*80)
    
    # Statistiques globales
    stats = {
        'haki': {'total_detections': 0, 'total_confidence': 0, 'count': 0, 'wins': 0},
        'ultimate': {'total_detections': 0, 'total_confidence': 0, 'count': 0, 'wins': 0}
    }
    
    # Tester chaque image
    for i, img_path in enumerate(images, 1):
        print(f"\n🖼️  IMAGE {i}: {img_path.name}")
        print("-"*80)
        
        # Test Haki
        results_haki = model_haki.predict(source=str(img_path), conf=0.25, save=False, verbose=False)
        detections_haki = len(results_haki[0].boxes)
        if detections_haki > 0:
            confidences_haki = [float(box.conf[0]) for box in results_haki[0].boxes]
            avg_conf_haki = sum(confidences_haki) / len(confidences_haki)
        else:
            avg_conf_haki = 0
        
        # Test Ultimate
        results_ultimate = model_ultimate.predict(source=str(img_path), conf=0.25, save=False, verbose=False)
        detections_ultimate = len(results_ultimate[0].boxes)
        if detections_ultimate > 0:
            confidences_ultimate = [float(box.conf[0]) for box in results_ultimate[0].boxes]
            avg_conf_ultimate = sum(confidences_ultimate) / len(confidences_ultimate)
        else:
            avg_conf_ultimate = 0
        
        # Affichage
        print(f"\n🔴 HAKI:")
        print(f"   Détections      : {detections_haki} pièces")
        print(f"   Conf. moyenne   : {avg_conf_haki:.2%}")
        
        print(f"\n🌟 ULTIMATE:")
        print(f"   Détections      : {detections_ultimate} pièces")
        print(f"   Conf. moyenne   : {avg_conf_ultimate:.2%}")
        
        # Déterminer le gagnant
        if avg_conf_ultimate > avg_conf_haki and detections_ultimate >= detections_haki:
            winner = "ULTIMATE"
            stats['ultimate']['wins'] += 1
            print(f"\n   🏆 Gagnant: ULTIMATE (meilleure confiance et plus de détections)")
        elif avg_conf_haki > avg_conf_ultimate and detections_haki >= detections_ultimate:
            winner = "HAKI"
            stats['haki']['wins'] += 1
            print(f"\n   🏆 Gagnant: HAKI (meilleure confiance et plus de détections)")
        elif detections_ultimate > detections_haki:
            winner = "ULTIMATE"
            stats['ultimate']['wins'] += 1
            print(f"\n   🏆 Gagnant: ULTIMATE (plus de détections)")
        elif detections_haki > detections_ultimate:
            winner = "HAKI"
            stats['haki']['wins'] += 1
            print(f"\n   🏆 Gagnant: HAKI (plus de détections)")
        elif avg_conf_ultimate > avg_conf_haki:
            winner = "ULTIMATE"
            stats['ultimate']['wins'] += 1
            print(f"\n   🏆 Gagnant: ULTIMATE (meilleure confiance)")
        elif avg_conf_haki > avg_conf_ultimate:
            winner = "HAKI"
            stats['haki']['wins'] += 1
            print(f"\n   🏆 Gagnant: HAKI (meilleure confiance)")
        else:
            winner = "ÉGALITÉ"
            print(f"\n   🤝 ÉGALITÉ")
        
        # Mise à jour des stats
        stats['haki']['total_detections'] += detections_haki
        stats['haki']['total_confidence'] += avg_conf_haki
        stats['haki']['count'] += 1
        
        stats['ultimate']['total_detections'] += detections_ultimate
        stats['ultimate']['total_confidence'] += avg_conf_ultimate
        stats['ultimate']['count'] += 1
    
    # Résultats finaux
    print("\n" + "="*80)
    print("📊 RÉSULTATS FINAUX")
    print("="*80 + "\n")
    
    avg_det_haki = stats['haki']['total_detections'] / stats['haki']['count']
    avg_conf_haki = stats['haki']['total_confidence'] / stats['haki']['count']
    
    avg_det_ultimate = stats['ultimate']['total_detections'] / stats['ultimate']['count']
    avg_conf_ultimate = stats['ultimate']['total_confidence'] / stats['ultimate']['count']
    
    print("🔴 HAKI:")
    print(f"   Victoires             : {stats['haki']['wins']}/{len(images)}")
    print(f"   Détections moyennes   : {avg_det_haki:.1f} pièces/image")
    print(f"   Confiance moyenne     : {avg_conf_haki:.2%}")
    
    print("\n🌟 ULTIMATE:")
    print(f"   Victoires             : {stats['ultimate']['wins']}/{len(images)}")
    print(f"   Détections moyennes   : {avg_det_ultimate:.1f} pièces/image")
    print(f"   Confiance moyenne     : {avg_conf_ultimate:.2%}")
    
    print("\n" + "="*80)
    if stats['ultimate']['wins'] > stats['haki']['wins']:
        print("🏆 CHAMPION : ULTIMATE !")
        print(f"   Supériorité : +{stats['ultimate']['wins'] - stats['haki']['wins']} victoires")
        print(f"   Confiance : +{(avg_conf_ultimate - avg_conf_haki)*100:.2f} points")
        print(f"   Détections : +{(avg_det_ultimate - avg_det_haki):.1f} pièces/image en moyenne")
    elif stats['haki']['wins'] > stats['ultimate']['wins']:
        print("🏆 CHAMPION : HAKI !")
        print(f"   Supériorité : +{stats['haki']['wins'] - stats['ultimate']['wins']} victoires")
        print(f"   Confiance : +{(avg_conf_haki - avg_conf_ultimate)*100:.2f} points")
        print(f"   Détections : +{(avg_det_haki - avg_det_ultimate):.1f} pièces/image en moyenne")
    else:
        print("🤝 ÉGALITÉ PARFAITE !")
    print("="*80 + "\n")


if __name__ == '__main__':
    compare_ultimate_haki()
