"""
Script pour adapter le dataset Roboflow en ajoutant la détection de couleur des pièces.
Analyse les images pour déterminer si les pièces sont noires ou blanches.
"""
import os
import shutil
import cv2
import numpy as np
from pathlib import Path

# Mapping des classes Roboflow vers notre format
CLASS_MAPPING = {
    'Kingrotation': 'king',
    'Knightrotation': 'knight', 
    'Pawnrotation': 'pawn',
    'Queenrotation': 'queen',
    'bishoprotation': 'bishop',
    'rookrotation': 'rook'
}

# Classes finales avec couleurs
FINAL_CLASSES = [
    'bishop', 'black-bishop', 'black-king', 'black-knight', 'black-pawn', 
    'black-queen', 'black-rook', 'white-bishop', 'white-king', 'white-knight', 
    'white-pawn', 'white-queen', 'white-rook'
]

def detect_piece_color(image, bbox):
    """
    Détecte si une pièce est noire ou blanche en analysant la luminosité moyenne.
    
    Args:
        image: Image numpy array (BGR)
        bbox: [x_center, y_center, width, height] en format YOLO normalisé
    
    Returns:
        'black' ou 'white'
    """
    h, w = image.shape[:2]
    
    # Convertir bbox YOLO en pixels
    x_center = int(bbox[0] * w)
    y_center = int(bbox[1] * h)
    box_w = int(bbox[2] * w)
    box_h = int(bbox[3] * h)
    
    # Extraire la région de la pièce
    x1 = max(0, x_center - box_w // 2)
    y1 = max(0, y_center - box_h // 2)
    x2 = min(w, x_center + box_w // 2)
    y2 = min(h, y_center + box_h // 2)
    
    piece_region = image[y1:y2, x1:x2]
    
    if piece_region.size == 0:
        return 'white'  # Défaut
    
    # Convertir en grayscale et calculer la luminosité moyenne
    gray = cv2.cvtColor(piece_region, cv2.COLOR_BGR2GRAY)
    mean_brightness = np.mean(gray)
    
    # Seuil : si luminosité < 127, c'est noir, sinon blanc
    return 'black' if mean_brightness < 127 else 'white'

def process_label_file(image_path, label_path, output_label_path):
    """
    Traite un fichier de labels YOLO et ajoute la détection de couleur.
    
    Args:
        image_path: Chemin vers l'image
        label_path: Chemin vers le fichier label original
        output_label_path: Chemin de sortie pour le nouveau label
    """
    # Charger l'image
    image = cv2.imread(str(image_path))
    if image is None:
        print(f"Erreur: impossible de charger {image_path}")
        return
    
    # Lire le fichier label
    with open(label_path, 'r') as f:
        lines = f.readlines()
    
    new_lines = []
    roboflow_classes = ['Kingrotation', 'Knightrotation', 'Pawnrotation', 
                        'Queenrotation', 'bishoprotation', 'rookrotation']
    
    for line in lines:
        parts = line.strip().split()
        if len(parts) < 5:
            continue
            
        class_id = int(parts[0])
        bbox = [float(x) for x in parts[1:5]]
        
        # Obtenir le nom de la classe
        piece_type = roboflow_classes[class_id]
        piece_name = CLASS_MAPPING.get(piece_type, piece_type.lower())
        
        # Détecter la couleur
        color = detect_piece_color(image, bbox)
        
        # Créer le nouveau nom de classe
        new_class_name = f"{color}-{piece_name}"
        
        # Trouver l'index dans FINAL_CLASSES
        if new_class_name in FINAL_CLASSES:
            new_class_id = FINAL_CLASSES.index(new_class_name)
        else:
            print(f"Attention: classe {new_class_name} non trouvée, skip")
            continue
        
        # Créer la nouvelle ligne
        new_line = f"{new_class_id} {' '.join(parts[1:])}\n"
        new_lines.append(new_line)
    
    # Écrire le nouveau fichier label
    with open(output_label_path, 'w') as f:
        f.writelines(new_lines)
    
    print(f"✓ Traité: {label_path.name} -> {len(new_lines)} pièces détectées")

def process_dataset(roboflow_path, output_path):
    """
    Traite tout le dataset Roboflow et crée un nouveau dataset avec couleurs.
    
    Args:
        roboflow_path: Chemin vers le dataset Roboflow
        output_path: Chemin de sortie pour le dataset adapté
    """
    roboflow_path = Path(roboflow_path)
    output_path = Path(output_path)
    
    # Créer la structure de sortie
    for split in ['train', 'valid', 'test']:
        (output_path / split / 'images').mkdir(parents=True, exist_ok=True)
        (output_path / split / 'labels').mkdir(parents=True, exist_ok=True)
    
    total_images = 0
    total_pieces = 0
    
    # Traiter chaque split
    for split in ['train', 'valid', 'test']:
        print(f"\n{'='*60}")
        print(f"Traitement du split: {split}")
        print(f"{'='*60}")
        
        images_dir = roboflow_path / split / 'images'
        labels_dir = roboflow_path / split / 'labels'
        
        if not images_dir.exists():
            print(f"⚠️  Dossier {images_dir} non trouvé, skip")
            continue
        
        # Lister toutes les images
        image_files = list(images_dir.glob('*.jpg')) + list(images_dir.glob('*.png'))
        
        for img_path in image_files:
            label_path = labels_dir / (img_path.stem + '.txt')
            
            if not label_path.exists():
                print(f"⚠️  Label manquant pour {img_path.name}, skip")
                continue
            
            # Copier l'image
            output_img_path = output_path / split / 'images' / img_path.name
            shutil.copy2(img_path, output_img_path)
            
            # Traiter les labels
            output_label_path = output_path / split / 'labels' / (img_path.stem + '.txt')
            process_label_file(img_path, label_path, output_label_path)
            
            total_images += 1
            
            # Compter les pièces
            with open(output_label_path, 'r') as f:
                total_pieces += len(f.readlines())
    
    print(f"\n{'='*60}")
    print(f"✅ Traitement terminé!")
    print(f"{'='*60}")
    print(f"Total images traitées: {total_images}")
    print(f"Total pièces détectées: {total_pieces}")
    print(f"Dataset sauvegardé dans: {output_path}")
    
    # Créer le fichier data.yaml
    create_data_yaml(output_path)

def create_data_yaml(output_path):
    """Crée le fichier data.yaml pour le nouveau dataset."""
    yaml_content = f"""# Dataset adapté depuis Roboflow avec détection de couleur
path: {output_path.absolute()}
train: train/images
val: valid/images
test: test/images

# Classes
nc: 13
names: {FINAL_CLASSES}
"""
    
    yaml_path = output_path / 'data.yaml'
    with open(yaml_path, 'w') as f:
        f.write(yaml_content)
    
    print(f"\n✓ Fichier de configuration créé: {yaml_path}")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description="Adapte le dataset Roboflow avec détection de couleur")
    parser.add_argument('--input', type=str, 
                        default='data/roboflow_dataset',
                        help="Chemin vers le dataset Roboflow")
    parser.add_argument('--output', type=str, 
                        default='data/roboflow_adapted',
                        help="Chemin de sortie pour le dataset adapté")
    
    args = parser.parse_args()
    
    print("🎯 Adaptation du dataset Roboflow")
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    
    process_dataset(args.input, args.output)
