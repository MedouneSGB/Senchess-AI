"""
Exemples d'utilisation rapide des modèles Senchess AI

Ce fichier contient des exemples pratiques pour utiliser les modèles
Senchess Haki et Senchess Gear dans vos projets.
"""

import sys
from pathlib import Path

# Ajouter le répertoire parent au path pour importer model_manager
sys.path.append(str(Path(__file__).parent.parent))

from src.model_manager import SenchessModelManager


# ============================================
# Exemple 1 : Détection Basique
# ============================================

def exemple_detection_simple():
    """Détection simple sur une image"""
    print("\n" + "="*60)
    print("EXEMPLE 1 : Détection simple")
    print("="*60 + "\n")
    
    # Initialiser le gestionnaire
    manager = SenchessModelManager()
    
    # Charger le modèle Gear (photos physiques)
    model = manager.load_model('gear')
    
    # Détecter les pièces
    image_path = "imgTest/capture2.jpg"
    results = manager.predict(model, image_path, save=True)
    
    print(f"✅ Détection terminée !")
    print(f"   {len(results[0].boxes)} pièces détectées")
    print(f"   Résultats sauvegardés dans predictions/")


# ============================================
# Exemple 2 : Comparaison des Modèles
# ============================================

def exemple_comparaison_modeles():
    """Comparer les 2 modèles sur la même image"""
    print("\n" + "="*60)
    print("EXEMPLE 2 : Comparaison des modèles")
    print("="*60 + "\n")
    
    manager = SenchessModelManager()
    
    # Comparer les 2 modèles
    image_path = "imgTest/capture2.jpg"
    comparison = manager.compare(image_path)
    
    print("\n📊 Résultats de la comparaison :")
    for model_name, stats in comparison.items():
        print(f"\n{model_name}:")
        print(f"  Détections      : {stats['detections']}")
        print(f"  Conf. moyenne   : {stats['avg_confidence']:.2%}")
        print(f"  Temps inférence : {stats['inference_time']:.3f}s")


# ============================================
# Exemple 3 : Traitement par Lot
# ============================================

def exemple_batch_processing():
    """Traiter plusieurs images d'un coup"""
    print("\n" + "="*60)
    print("EXEMPLE 3 : Traitement par lot")
    print("="*60 + "\n")
    
    from pathlib import Path
    
    manager = SenchessModelManager()
    model = manager.load_model('gear')
    
    # Trouver toutes les images de test
    test_dir = Path("imgTest")
    images = list(test_dir.glob("*.jpg")) + list(test_dir.glob("*.png"))
    
    print(f"📁 {len(images)} images trouvées\n")
    
    # Traiter chaque image
    for i, img_path in enumerate(images, 1):
        results = manager.predict(model, str(img_path), save=False)
        detections = len(results[0].boxes)
        print(f"  [{i}/{len(images)}] {img_path.name}: {detections} pièces")
    
    print(f"\n✅ Traitement terminé !")


# ============================================
# Exemple 4 : Détection avec Confiance Personnalisée
# ============================================

def exemple_confiance_personnalisee():
    """Ajuster le seuil de confiance"""
    print("\n" + "="*60)
    print("EXEMPLE 4 : Seuil de confiance personnalisé")
    print("="*60 + "\n")
    
    manager = SenchessModelManager()
    model = manager.load_model('haki')
    
    image_path = "imgTest/capture2.jpg"
    
    # Tester différents seuils
    thresholds = [0.1, 0.25, 0.5, 0.75]
    
    print("🎯 Test de différents seuils de confiance :\n")
    for threshold in thresholds:
        results = manager.predict(model, image_path, conf=threshold, save=False)
        detections = len(results[0].boxes)
        print(f"  Seuil {threshold:.2f} : {detections} détections")


# ============================================
# Exemple 5 : Recommandation Automatique
# ============================================

def exemple_recommandation():
    """Obtenir une recommandation de modèle"""
    print("\n" + "="*60)
    print("EXEMPLE 5 : Recommandation automatique")
    print("="*60 + "\n")
    
    manager = SenchessModelManager()
    
    # Scénarios différents
    scenarios = [
        "photo smartphone d'un échiquier",
        "diagramme d'échecs généré",
        "capture d'écran d'une partie en ligne"
    ]
    
    for scenario in scenarios:
        recommendation = manager.recommend(scenario)
        print(f"📝 '{scenario}'")
        print(f"   → Modèle recommandé : {recommendation['recommended_model']}")
        print(f"   → Raison : {recommendation['reason']}\n")


# ============================================
# Exemple 6 : Utilisation Directe YOLO
# ============================================

def exemple_yolo_direct():
    """Utiliser YOLO directement sans model_manager"""
    print("\n" + "="*60)
    print("EXEMPLE 6 : Utilisation directe YOLO")
    print("="*60 + "\n")
    
    from ultralytics import YOLO
    
    # Charger un modèle
    model = YOLO("models/senchess_gear_v1.0/weights/best.pt")
    
    # Prédiction
    results = model.predict(
        source="imgTest/capture2.jpg",
        conf=0.25,
        save=True,
        project="predictions",
        name="yolo_direct"
    )
    
    # Afficher les résultats
    print("✅ Détection YOLO directe :")
    for r in results:
        boxes = r.boxes
        print(f"   {len(boxes)} pièces détectées")
        for box in boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            name = r.names[cls]
            print(f"   - {name}: {conf:.2%}")


# ============================================
# Exemple 7 : Extraction de Données FEN
# ============================================

def exemple_extraction_fen():
    """Extraire la position pour notation FEN (basique)"""
    print("\n" + "="*60)
    print("EXEMPLE 7 : Extraction position (prototype FEN)")
    print("="*60 + "\n")
    
    manager = SenchessModelManager()
    model = manager.load_model('gear')
    
    # Détecter les pièces
    image_path = "imgTest/capture2.jpg"
    results = manager.predict(model, image_path, save=False)
    
    # Extraire les informations
    pieces = []
    for box in results[0].boxes:
        cls = int(box.cls[0])
        name = results[0].names[cls]
        conf = float(box.conf[0])
        x, y = box.xywh[0][:2]  # Centre de la bounding box
        
        pieces.append({
            'piece': name,
            'confidence': conf,
            'position': (float(x), float(y))
        })
    
    # Trier par position (gauche à droite, haut en bas)
    pieces.sort(key=lambda p: (p['position'][1], p['position'][0]))
    
    print(f"🎯 {len(pieces)} pièces détectées :\n")
    for i, piece in enumerate(pieces, 1):
        x, y = piece['position']
        print(f"  {i}. {piece['piece']:<20} à ({x:>6.1f}, {y:>6.1f}) - {piece['confidence']:.1%}")
    
    print("\n💡 Note : Pour une vraie notation FEN, il faudrait :")
    print("   - Calibrer les coordonnées pixel → cases échiquier")
    print("   - Mapper les détections → grille 8x8")
    print("   - Convertir en notation algébrique")


# ============================================
# MENU PRINCIPAL
# ============================================

def main():
    """Menu principal pour choisir un exemple"""
    print("\n" + "="*60)
    print("🔥 EXEMPLES SENCHESS AI")
    print("="*60)
    
    exemples = [
        ("Détection simple", exemple_detection_simple),
        ("Comparaison des modèles", exemple_comparaison_modeles),
        ("Traitement par lot", exemple_batch_processing),
        ("Confiance personnalisée", exemple_confiance_personnalisee),
        ("Recommandation automatique", exemple_recommandation),
        ("Utilisation directe YOLO", exemple_yolo_direct),
        ("Extraction position (FEN)", exemple_extraction_fen),
    ]
    
    print("\nChoisissez un exemple :")
    for i, (nom, _) in enumerate(exemples, 1):
        print(f"  {i}. {nom}")
    print(f"  0. Exécuter tous les exemples")
    print(f"  q. Quitter")
    
    try:
        choix = input("\nVotre choix : ").strip()
        
        if choix.lower() == 'q':
            print("Au revoir ! 👋")
            return
        
        if choix == '0':
            # Exécuter tous les exemples
            for nom, fonction in exemples:
                try:
                    fonction()
                except Exception as e:
                    print(f"❌ Erreur dans '{nom}': {e}")
                print()
        else:
            idx = int(choix) - 1
            if 0 <= idx < len(exemples):
                exemples[idx][1]()
            else:
                print("❌ Choix invalide")
    
    except (ValueError, KeyboardInterrupt):
        print("\n\nAu revoir ! 👋")


if __name__ == '__main__':
    main()
