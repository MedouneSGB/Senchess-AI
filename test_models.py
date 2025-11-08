"""
Script pour tester les modèles Haki, Gear et Ultimate sur les images de test
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from src.model_manager import SenchessModelManager

def test_models_on_images():
    """Teste les trois modèles sur toutes les images du dossier imgTest"""
    
    print("\n" + "="*70)
    print("🔥 TEST DES MODÈLES SENCHESS HAKI, GEAR ET ULTIMATE")
    print("="*70 + "\n")
    
    # Initialiser le gestionnaire
    manager = SenchessModelManager()
    
    # Dossier des images de test
    test_dir = Path("examples/imgTest")
    images = sorted(list(test_dir.glob("*.png")) + list(test_dir.glob("*.jpg")))
    
    if not images:
        print("❌ Aucune image trouvée dans le dossier imgTest")
        return
    
    print(f"📁 {len(images)} images trouvées : {[img.name for img in images]}\n")
    
    # Charger les trois modèles
    print("⏳ Chargement des modèles...\n")
    try:
        model_haki = manager.load_model('haki')
        print("✅ Modèle Haki chargé")
    except Exception as e:
        print(f"❌ Erreur lors du chargement de Haki: {e}")
        model_haki = None
    
    try:
        model_gear = manager.load_model('gear')
        print("✅ Modèle Gear chargé")
    except Exception as e:
        print(f"❌ Erreur lors du chargement de Gear: {e}")
        model_gear = None
    
    # Charger Ultimate
    try:
        from ultralytics import YOLO
        model_ultimate = YOLO("models/senchess_ultimate_v1.0_quick/weights/best.pt")
        print("✅ Modèle Ultimate chargé")
    except Exception as e:
        print(f"❌ Erreur lors du chargement de Ultimate: {e}")
        model_ultimate = None
    
    print("\n" + "="*70)
    print("📊 RÉSULTATS DES TESTS")
    print("="*70 + "\n")
    
    # Tester chaque image avec les deux modèles
    for i, img_path in enumerate(images, 1):
        print(f"\n{'─'*70}")
        print(f"🖼️  Image {i}/{len(images)}: {img_path.name}")
        print(f"{'─'*70}\n")
        
        # Test avec Haki
        if model_haki:
            print("🔴 Modèle HAKI (Screenshots/Diagrammes):")
            try:
                results_haki = model_haki.predict(
                    source=str(img_path), 
                    conf=0.25,
                    save=True,
                    project='predictions',
                    name=f'haki_{img_path.stem}'
                )
                
                detections = len(results_haki[0].boxes)
                print(f"   ✓ {detections} pièces détectées")
                
                # Afficher les détails
                if detections > 0:
                    confidences = [float(box.conf[0]) for box in results_haki[0].boxes]
                    avg_conf = sum(confidences) / len(confidences)
                    print(f"   ✓ Confiance moyenne: {avg_conf:.2%}")
                    
                    # Compter par type de pièce
                    piece_counts = {}
                    for box in results_haki[0].boxes:
                        cls = int(box.cls[0])
                        name = results_haki[0].names[cls]
                        piece_counts[name] = piece_counts.get(name, 0) + 1
                    
                    print("   ✓ Détails:")
                    for piece, count in sorted(piece_counts.items()):
                        print(f"      - {piece}: {count}")
                        
            except Exception as e:
                print(f"   ❌ Erreur: {e}")
        
        print()
        
        # Test avec Gear
        if model_gear:
            print("⚫ Modèle GEAR (Photos physiques):")
            try:
                results_gear = model_gear.predict(
                    source=str(img_path), 
                    conf=0.25,
                    save=True,
                    project='predictions',
                    name=f'gear_{img_path.stem}'
                )
                
                detections = len(results_gear[0].boxes)
                print(f"   ✓ {detections} pièces détectées")
                
                # Afficher les détails
                if detections > 0:
                    confidences = [float(box.conf[0]) for box in results_gear[0].boxes]
                    avg_conf = sum(confidences) / len(confidences)
                    print(f"   ✓ Confiance moyenne: {avg_conf:.2%}")
                    
                    # Compter par type de pièce
                    piece_counts = {}
                    for box in results_gear[0].boxes:
                        cls = int(box.cls[0])
                        name = results_gear[0].names[cls]
                        piece_counts[name] = piece_counts.get(name, 0) + 1
                    
                    print("   ✓ Détails:")
                    for piece, count in sorted(piece_counts.items()):
                        print(f"      - {piece}: {count}")
                        
            except Exception as e:
                print(f"   ❌ Erreur: {e}")
        
        print()
        
        # Test avec Ultimate
        if model_ultimate:
            print("🌟 Modèle ULTIMATE (Universel):")
            try:
                results_ultimate = model_ultimate.predict(
                    source=str(img_path), 
                    conf=0.25,
                    save=True,
                    project='predictions',
                    name=f'ultimate_{img_path.stem}'
                )
                
                detections = len(results_ultimate[0].boxes)
                print(f"   ✓ {detections} pièces détectées")
                
                # Afficher les détails
                if detections > 0:
                    confidences = [float(box.conf[0]) for box in results_ultimate[0].boxes]
                    avg_conf = sum(confidences) / len(confidences)
                    print(f"   ✓ Confiance moyenne: {avg_conf:.2%}")
                    
                    # Compter par type de pièce
                    piece_counts = {}
                    for box in results_ultimate[0].boxes:
                        cls = int(box.cls[0])
                        name = results_ultimate[0].names[cls]
                        piece_counts[name] = piece_counts.get(name, 0) + 1
                    
                    print("   ✓ Détails:")
                    for piece, count in sorted(piece_counts.items()):
                        print(f"      - {piece}: {count}")
                        
            except Exception as e:
                print(f"   ❌ Erreur: {e}")
    
    print("\n" + "="*70)
    print("✅ TESTS TERMINÉS")
    print("="*70)
    print("\n💾 Les résultats annotés sont sauvegardés dans le dossier 'predictions/'\n")


if __name__ == '__main__':
    test_models_on_images()
