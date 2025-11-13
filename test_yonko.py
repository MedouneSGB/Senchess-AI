"""
Script de test rapide pour le modèle Yonko
"""
from ultralytics import YOLO
import cv2
from pathlib import Path

def test_yonko():
    """Test du modèle Yonko avec une image"""
    
    print("🌊 Test du modèle Yonko v1.0\n")
    
    # Charger le modèle
    model_path = 'models/senchess_yonko_v1.0/weights/best.pt'
    
    if not Path(model_path).exists():
        print(f"❌ Modèle non trouvé: {model_path}")
        return
    
    print(f"📥 Chargement du modèle depuis: {model_path}")
    model = YOLO(model_path)
    print("✅ Modèle chargé\n")
    
    # Chercher une image de test
    test_images = list(Path('examples/imgTest').glob('*.jpg')) + \
                  list(Path('examples/imgTest').glob('*.png'))
    
    if not test_images:
        print("⚠️ Aucune image de test trouvée dans examples/imgTest/")
        return
    
    test_image = test_images[0]
    print(f"🖼️ Image de test: {test_image}\n")
    
    # Prédiction
    print("🔍 Analyse en cours...")
    results = model.predict(
        source=str(test_image),
        conf=0.25,
        save=True,
        verbose=True
    )
    
    # Afficher les résultats
    print("\n📊 Résultats de détection:\n")
    
    for result in results:
        boxes = result.boxes
        print(f"✅ {len(boxes)} pièces détectées")
        
        # Calculer la confiance moyenne
        confidences = [float(box.conf[0]) for box in boxes]
        avg_conf = sum(confidences) / len(confidences) if confidences else 0
        print(f"📈 Confiance moyenne: {avg_conf:.2%}\n")
        
        # Liste des pièces
        print("Détail des pièces:")
        for i, box in enumerate(boxes, 1):
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            class_name = result.names[class_id]
            print(f"  {i}. {class_name}: {confidence:.2%}")
    
    print(f"\n💾 Image annotée sauvegardée dans: runs/detect/predict/")

if __name__ == "__main__":
    test_yonko()
