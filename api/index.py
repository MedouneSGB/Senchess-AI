"""
API Flask pour la détection de pièces d'échecs avec YOLO
Déployable sur Vercel
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import io
import base64
import numpy as np
from PIL import Image
import cv2
from ultralytics import YOLO
from pathlib import Path
import tempfile

app = Flask(__name__)
CORS(app)  # Permettre les requêtes cross-origin

# Configuration des modèles
HUGGINGFACE_REPO = os.environ.get('HUGGINGFACE_REPO_ID', 'MedouneSGB/senchess-models')
MODEL_TYPE = os.environ.get('MODEL_TYPE', 'gear')  # 'gear', 'haki', ou 'ensemble'
USE_HUGGINGFACE = os.environ.get('USE_HUGGINGFACE', 'true').lower() == 'true'

# Variables globales pour les modèles
model_gear = None
model_haki = None

def download_model_from_huggingface(model_name):
    """Télécharge un modèle depuis Hugging Face Hub"""
    try:
        from huggingface_hub import hf_hub_download
        
        print(f"📥 Téléchargement de {model_name} depuis Hugging Face...")
        
        model_path = hf_hub_download(
            repo_id=HUGGINGFACE_REPO,
            filename=model_name,
            cache_dir="/tmp/models"
        )
        
        print(f"✅ Modèle téléchargé: {model_path}")
        return model_path
        
    except ImportError:
        print("❌ huggingface_hub non installé")
        return None
    except Exception as e:
        print(f"❌ Erreur téléchargement: {e}")
        return None

def load_model():
    """Charge le(s) modèle(s) YOLO"""
    global model_gear, model_haki
    
    try:
        if USE_HUGGINGFACE:
            # Charger depuis Hugging Face
            print(f"🔄 Chargement des modèles depuis Hugging Face ({HUGGINGFACE_REPO})...")
            
            if MODEL_TYPE in ['gear', 'ensemble']:
                gear_path = download_model_from_huggingface('gear_v1.1.pt')
                if gear_path:
                    model_gear = YOLO(gear_path)
                    print("✅ Modèle Gear chargé")
            
            if MODEL_TYPE in ['haki', 'ensemble']:
                haki_path = download_model_from_huggingface('haki_v1.0.pt')
                if haki_path:
                    model_haki = YOLO(haki_path)
                    print("✅ Modèle Haki chargé")
        
        else:
            # Charger depuis fichiers locaux (pour développement local)
            print("🔄 Chargement des modèles depuis fichiers locaux...")
            
            gear_local = 'models/senchess_gear_v1.1/weights/best.pt'
            haki_local = 'models/senchess_haki_v1.0/weights/best.pt'
            
            if MODEL_TYPE in ['gear', 'ensemble'] and os.path.exists(gear_local):
                model_gear = YOLO(gear_local)
                print(f"✅ Modèle Gear chargé depuis: {gear_local}")
            
            if MODEL_TYPE in ['haki', 'ensemble'] and os.path.exists(haki_local):
                model_haki = YOLO(haki_local)
                print(f"✅ Modèle Haki chargé depuis: {haki_local}")
        
        # Vérifier qu'au moins un modèle est chargé
        if model_gear is None and model_haki is None:
            print("⚠️ Aucun modèle chargé - utilisation d'un modèle par défaut")
            model_gear = YOLO('yolov8n.pt')
            print("⚠️ Modèle par défaut chargé (yolov8n)")
            
    except Exception as e:
        print(f"❌ Erreur lors du chargement du modèle: {e}")
        model_gear = None
        model_haki = None

def pieces_to_fen(detections, image_width, image_height):
    """
    Convertit les détections de pièces en notation FEN
    
    Args:
        detections: Liste des détections avec position et classe
        image_width: Largeur de l'image
        image_height: Hauteur de l'image
    
    Returns:
        str: Notation FEN de la position
    """
    # Créer une grille 8x8 vide
    board = [['' for _ in range(8)] for _ in range(8)]
    
    # Mapping des noms de pièces vers notation FEN
    piece_mapping = {
        'white-king': 'K', 'white-queen': 'Q', 'white-rook': 'R',
        'white-bishop': 'B', 'white-knight': 'N', 'white-pawn': 'P',
        'black-king': 'k', 'black-queen': 'q', 'black-rook': 'r',
        'black-bishop': 'b', 'black-knight': 'n', 'black-pawn': 'p',
        # Variantes possibles
        'king': 'K', 'queen': 'Q', 'rook': 'R',
        'bishop': 'B', 'knight': 'N', 'pawn': 'P',
        'black king': 'k', 'black queen': 'q', 'black rook': 'r',
        'black bishop': 'b', 'black knight': 'n', 'black pawn': 'p',
    }
    
    # Calculer la taille d'une case
    cell_width = image_width / 8
    cell_height = image_height / 8
    
    # Placer chaque pièce détectée sur la grille
    for det in detections:
        piece_name = det['class'].lower()
        
        # Obtenir le symbole FEN
        fen_symbol = piece_mapping.get(piece_name, '')
        if not fen_symbol:
            continue
        
        # Calculer la position centrale de la pièce
        center_x = (det['bbox']['x1'] + det['bbox']['x2']) / 2
        center_y = (det['bbox']['y1'] + det['bbox']['y2']) / 2
        
        # Convertir en coordonnées d'échiquier (0-7)
        col = int(center_x / cell_width)
        row = int(center_y / cell_height)
        
        # S'assurer que les coordonnées sont valides
        col = max(0, min(7, col))
        row = max(0, min(7, row))
        
        # Placer la pièce (noter que row 0 = haut de l'image = rang 8 aux échecs)
        board[row][col] = fen_symbol
    
    # Construire la chaîne FEN
    fen_rows = []
    for row in board:
        fen_row = ''
        empty_count = 0
        
        for cell in row:
            if cell == '':
                empty_count += 1
            else:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0
                fen_row += cell
        
        if empty_count > 0:
            fen_row += str(empty_count)
        
        fen_rows.append(fen_row)
    
    # Joindre avec '/' et ajouter les métadonnées FEN par défaut
    fen = '/'.join(fen_rows)
    fen += ' w KQkq - 0 1'  # Métadonnées: blancs jouent, tous les roques possibles, etc.
    
    return fen

@app.route('/', methods=['GET'])
def home():
    """Page d'accueil de l'API"""
    return jsonify({
        'name': 'Senchess AI API',
        'version': '1.0.0',
        'description': 'API de détection de pièces d\'échecs avec YOLO',
        'endpoints': {
            '/': 'Cette page',
            '/health': 'Vérifier l\'état de l\'API',
            '/predict': 'POST - Analyser une image d\'échiquier'
        }
    })

@app.route('/health', methods=['GET'])
def health():
    """Vérifier l'état de l'API et du modèle"""
    models_loaded = {
        'gear': model_gear is not None,
        'haki': model_haki is not None
    }
    
    any_loaded = model_gear is not None or model_haki is not None
    
    return jsonify({
        'status': 'healthy' if any_loaded else 'model_not_loaded',
        'model_type': MODEL_TYPE,
        'models_loaded': models_loaded,
        'use_huggingface': USE_HUGGINGFACE,
        'repo_id': HUGGINGFACE_REPO if USE_HUGGINGFACE else 'local'
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint principal pour la détection de pièces d'échecs
    
    Accepte:
    - image: fichier image (multipart/form-data)
    - image_url: URL d'une image
    - image_base64: image encodée en base64
    - conf: seuil de confiance (optionnel, défaut 0.25)
    - model: 'gear', 'haki' ou 'ensemble' (optionnel, utilise MODEL_TYPE par défaut)
    
    Retourne:
    - fen: notation FEN de la position
    - pieces: liste des pièces détectées
    - confidence: confiance moyenne
    - detectedPieces: nombre de pièces détectées
    """
    # Vérifier qu'au moins un modèle est chargé
    if model_gear is None and model_haki is None:
        return jsonify({
            'error': 'Modèle non chargé',
            'message': 'Aucun modèle YOLO n\'a pu être chargé'
        }), 500
    
    try:
        # Paramètres
        conf_threshold = float(request.form.get('conf', 0.25))
        requested_model = request.form.get('model', MODEL_TYPE)
        
        # Récupérer l'image depuis différentes sources
        image = None
        
        # 1. Fichier uploadé
        if 'image' in request.files:
            file = request.files['image']
            image_bytes = file.read()
            image = Image.open(io.BytesIO(image_bytes))
        
        # 2. Image base64
        elif 'image_base64' in request.form:
            image_base64 = request.form['image_base64']
            # Enlever le préfixe data:image/...;base64, si présent
            if ',' in image_base64:
                image_base64 = image_base64.split(',')[1]
            image_bytes = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_bytes))
        
        # 3. URL d'image (à implémenter si nécessaire)
        elif 'image_url' in request.form:
            return jsonify({
                'error': 'Non implémenté',
                'message': 'Le téléchargement depuis URL n\'est pas encore supporté'
            }), 501
        
        else:
            return jsonify({
                'error': 'Aucune image fournie',
                'message': 'Veuillez fournir une image via "image", "image_base64" ou "image_url"'
            }), 400
        
        # Convertir PIL Image en format compatible OpenCV
        image_np = np.array(image)
        if len(image_np.shape) == 2:  # Grayscale
            image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2RGB)
        elif image_np.shape[2] == 4:  # RGBA
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2RGB)
        
        image_height, image_width = image_np.shape[:2]
        
        # Sauvegarder temporairement l'image
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            tmp_path = tmp_file.name
            cv2.imwrite(tmp_path, cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR))
        
        # Choisir le modèle à utiliser
        detections = []
        
        if requested_model == 'ensemble' and model_gear and model_haki:
            # Mode ensemble : utiliser les deux modèles
            detections = predict_ensemble(tmp_path, conf_threshold)
        elif requested_model == 'haki' and model_haki:
            # Utiliser Haki
            detections = predict_with_model(model_haki, tmp_path, conf_threshold)
        elif model_gear:
            # Utiliser Gear (par défaut)
            detections = predict_with_model(model_gear, tmp_path, conf_threshold)
        elif model_haki:
            # Fallback sur Haki si Gear n'est pas disponible
            detections = predict_with_model(model_haki, tmp_path, conf_threshold)
        
        # Nettoyer le fichier temporaire
        os.unlink(tmp_path)
        
        # Calculer la confiance moyenne
        confidences = [d['confidence'] for d in detections]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        # Convertir en FEN
        fen = pieces_to_fen(detections, image_width, image_height)
        
        # Préparer la réponse
        response = {
            'success': True,
            'fen': fen,
            'pieces': detections,
            'confidence': round(avg_confidence, 3),
            'detectedPieces': len(detections),
            'description': f'Position détectée avec {len(detections)} pièces',
            'model_used': requested_model,
            'imageSize': {
                'width': image_width,
                'height': image_height
            },
            'warnings': []
        }
        
        # Ajouter des avertissements si nécessaire
        if avg_confidence < 0.8:
            response['warnings'].append('Confiance faible - vérifiez la qualité de l\'image')
        
        if len(detections) < 2:
            response['warnings'].append('Peu de pièces détectées - vérifiez que l\'échiquier est visible')
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'error': 'Erreur lors de la prédiction',
            'message': str(e)
        }), 500

def predict_with_model(model, image_path, conf_threshold):
    """Effectue une prédiction avec un modèle unique"""
    results = model.predict(
        source=image_path,
        conf=conf_threshold,
        save=False,
        verbose=False
    )
    
    detections = []
    for result in results:
        boxes = result.boxes
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            class_name = result.names[class_id]
            
            detections.append({
                'id': len(detections) + 1,
                'class': class_name,
                'confidence': round(confidence, 3),
                'bbox': {
                    'x1': round(x1, 2),
                    'y1': round(y1, 2),
                    'x2': round(x2, 2),
                    'y2': round(y2, 2),
                    'width': round(x2 - x1, 2),
                    'height': round(y2 - y1, 2)
                }
            })
    
    return detections

def predict_ensemble(image_path, conf_threshold):
    """
    Prédiction ensemble combinant Gear et Haki
    - Gear pour toutes les pièces
    - Haki pour les pièces stratégiques (King, Queen, Rook, Bishop) avec priorité
    """
    strategic_pieces = [
        'king', 'queen', 'rook', 'bishop',
        'black-king', 'black-queen', 'black-rook', 'black-bishop',
        'white-king', 'white-queen', 'white-rook', 'white-bishop'
    ]
    
    # 1. Prédictions Gear (toutes les pièces)
    gear_detections = predict_with_model(model_gear, image_path, conf_threshold)
    
    # 2. Prédictions Haki (pièces stratégiques)
    haki_detections = predict_with_model(model_haki, image_path, conf_threshold)
    
    # 3. Combiner intelligemment
    final_detections = []
    used_positions = []
    
    def boxes_overlap(box1, box2, threshold=0.5):
        """Vérifie si deux boîtes se chevauchent"""
        x1_min, y1_min = box1['x1'], box1['y1']
        x1_max, y1_max = box1['x2'], box1['y2']
        x2_min, y2_min = box2['x1'], box2['y1']
        x2_max, y2_max = box2['x2'], box2['y2']
        
        # Calculer l'intersection
        x_overlap = max(0, min(x1_max, x2_max) - max(x1_min, x2_min))
        y_overlap = max(0, min(y1_max, y2_max) - max(y1_min, y2_min))
        intersection = x_overlap * y_overlap
        
        # Calculer les aires
        area1 = (x1_max - x1_min) * (y1_max - y1_min)
        area2 = (x2_max - x2_min) * (y2_max - y2_min)
        union = area1 + area2 - intersection
        
        return intersection / union > threshold if union > 0 else False
    
    # Prioriser les détections Haki pour les pièces stratégiques
    for haki_det in haki_detections:
        if haki_det['class'].lower() in strategic_pieces:
            final_detections.append(haki_det)
            used_positions.append(haki_det['bbox'])
    
    # Ajouter les détections Gear non chevauchantes
    for gear_det in gear_detections:
        overlaps = False
        for used_pos in used_positions:
            if boxes_overlap(gear_det['bbox'], used_pos):
                overlaps = True
                break
        
        if not overlaps:
            final_detections.append(gear_det)
    
    # Réassigner les IDs
    for i, det in enumerate(final_detections):
        det['id'] = i + 1
    
    return final_detections

# Charger le modèle au démarrage
load_model()

# Pour Vercel, exporter l'app
# Vercel utilisera cette variable pour gérer les requêtes
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
