import os
import argparse
from ultralytics import YOLO
import cv2
import json

def predict_chess_pieces(model_path, image_path, conf_threshold=0.25, save_output=True):
    """
    Utilise le modèle entraîné pour détecter les pièces d'échecs sur une nouvelle image.
    
    Args:
        model_path: Chemin vers le fichier du modèle entraîné (.pt)
        image_path: Chemin vers l'image à analyser
        conf_threshold: Seuil de confiance minimum pour les détections (0-1)
        save_output: Si True, sauvegarde l'image annotée
    
    Returns:
        dict: Résultats de la détection avec les coordonnées et classes de chaque pièce
    """
    # Charger le modèle entraîné
    print(f"Chargement du modèle depuis : {model_path}")
    model = YOLO(model_path)
    
    # Effectuer la prédiction
    print(f"Analyse de l'image : {image_path}")
    results = model.predict(
        source=image_path,
        conf=conf_threshold,
        save=save_output,
        project='predictions',
        name='chess_detection'
    )
    
    # Extraire les informations de détection
    detections = []
    for result in results:
        boxes = result.boxes
        for i, box in enumerate(boxes):
            # Coordonnées de la boîte englobante
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            
            # Classe et confiance
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            class_name = result.names[class_id]
            
            detection = {
                'id': i + 1,
                'class': class_name,
                'confidence': round(confidence, 3),
                'bounding_box': {
                    'x1': round(x1, 2),
                    'y1': round(y1, 2),
                    'x2': round(x2, 2),
                    'y2': round(y2, 2)
                },
                'center': {
                    'x': round((x1 + x2) / 2, 2),
                    'y': round((y1 + y2) / 2, 2)
                }
            }
            detections.append(detection)
    
    # Affichage des résultats
    print(f"\n{'='*60}")
    print(f"Résultats de la détection")
    print(f"{'='*60}")
    print(f"Nombre de pièces détectées : {len(detections)}\n")
    
    for det in detections:
        print(f"Pièce #{det['id']}: {det['class']}")
        print(f"  Confiance: {det['confidence']*100:.1f}%")
        print(f"  Position (centre): ({det['center']['x']}, {det['center']['y']})")
        print()
    
    # Sauvegarder les résultats en JSON
    if save_output:
        output_json_path = os.path.join('predictions', 'chess_detection', 'detections.json')
        os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
        with open(output_json_path, 'w') as f:
            json.dump(detections, f, indent=2)
        print(f"Résultats sauvegardés dans : {output_json_path}")
    
    return detections


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script de prédiction pour la détection de pièces d'échecs.")
    
    parser.add_argument('--model-path', type=str, 
                        default='models/chess_detector4/weights/best.pt',
                        help="Chemin vers le modèle entraîné (.pt).")
    parser.add_argument('--image-path', type=str, required=True,
                        help="Chemin vers l'image à analyser.")
    parser.add_argument('--conf', type=float, default=0.25,
                        help="Seuil de confiance minimum (0-1).")
    parser.add_argument('--no-save', action='store_true',
                        help="Ne pas sauvegarder l'image annotée.")
    
    args = parser.parse_args()
    
    # Vérifier que le modèle existe
    if not os.path.exists(args.model_path):
        print(f"Erreur : Le modèle '{args.model_path}' n'a pas été trouvé.")
        print("Assurez-vous d'avoir entraîné le modèle avec 'python src/train.py' avant de faire des prédictions.")
        exit(1)
    
    # Vérifier que l'image existe
    if not os.path.exists(args.image_path):
        print(f"Erreur : L'image '{args.image_path}' n'a pas été trouvée.")
        exit(1)
    
    # Lancer la prédiction
    detections = predict_chess_pieces(
        model_path=args.model_path,
        image_path=args.image_path,
        conf_threshold=args.conf,
        save_output=not args.no_save
    )
