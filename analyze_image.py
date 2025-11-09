"""
Analyse d'une nouvelle image avec les 3 modèles
"""

from pathlib import Path
from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import numpy as np

def get_short_name(class_name):
    """Convertit le nom de classe en notation courte (wK, bQ, etc.)"""
    mapping = {
        'white-king': 'wK', 'white-queen': 'wQ', 'white-rook': 'wR',
        'white-bishop': 'wB', 'white-knight': 'wN', 'white-pawn': 'wP',
        'black-king': 'bK', 'black-queen': 'bQ', 'black-rook': 'bR',
        'black-bishop': 'bB', 'black-knight': 'bN', 'black-pawn': 'bP',
        'king': 'K', 'queen': 'Q', 'rook': 'R',
        'bishop': 'B', 'knight': 'N', 'pawn': 'P'
    }
    return mapping.get(class_name.lower(), class_name)

def format_label(short_name, confidence):
    """Format label sans espace: wK0.95"""
    return f"{short_name}{confidence:.2f}"

def analyze_with_three_models(image_path, conf=0.25):
    """Analyse une image avec Haki, Gear et Ultimate"""
    
    print("\n" + "="*70)
    print("🎯 ANALYSE AVEC 3 MODÈLES")
    print("="*70 + "\n")
    
    # Charger les modèles
    print("📦 Chargement des modèles...")
    haki_path = Path("models/senchess_haki_v1.0/weights/best.pt")
    gear_path = Path("models/senchess_gear_v1.0/weights/best.pt")
    ultimate_path = Path("models/senchess_ultimate_v1.0_quick/weights/best.pt")
    
    model_haki = YOLO(str(haki_path))
    model_gear = YOLO(str(gear_path))
    model_ultimate = YOLO(str(ultimate_path))
    print("✅ Modèles chargés\n")
    
    # Lire l'image originale
    img_original = cv2.imread(image_path)
    if img_original is None:
        print(f"❌ Impossible de lire l'image: {image_path}")
        return
    
    # Ajouter une marge en haut (30 pixels) pour les annotations
    margin_top = 30
    h, w = img_original.shape[:2]
    img_with_margin = cv2.copyMakeBorder(img_original, margin_top, 0, 0, 0, 
                                         cv2.BORDER_CONSTANT, value=(255, 255, 255))
    img_original = img_with_margin
    
    # HAKI
    print("🔴 Analyse HAKI...")
    results_haki = model_haki.predict(source=image_path, conf=conf, save=False, verbose=False)[0]
    img_haki = img_original.copy()
    
    for box in results_haki.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
        # Décaler les coordonnées pour la marge
        y1 += margin_top
        y2 += margin_top
        
        cls_id = int(box.cls[0])
        confidence = float(box.conf[0])
        class_name = results_haki.names[cls_id]
        
        short_name = get_short_name(class_name)
        label = format_label(short_name, confidence)
        
        cv2.rectangle(img_haki, (x1, y1), (x2, y2), (255, 0, 0), 2)
        (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(img_haki, (x1, y1 - 22), (x1 + w, y1), (255, 0, 0), -1)
        cv2.putText(img_haki, label, (x1, y1 - 5), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    print(f"   ✅ {len(results_haki.boxes)} pièces détectées")
    
    # GEAR
    print("⚙️  Analyse GEAR...")
    results_gear = model_gear.predict(source=image_path, conf=conf, save=False, verbose=False)[0]
    img_gear = img_original.copy()
    
    for box in results_gear.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
        # Décaler les coordonnées pour la marge
        y1 += margin_top
        y2 += margin_top
        
        cls_id = int(box.cls[0])
        confidence = float(box.conf[0])
        class_name = results_gear.names[cls_id]
        
        short_name = get_short_name(class_name)
        label = format_label(short_name, confidence)
        
        cv2.rectangle(img_gear, (x1, y1), (x2, y2), (0, 165, 255), 2)  # Orange
        (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(img_gear, (x1, y1 - 22), (x1 + w, y1), (0, 165, 255), -1)
        cv2.putText(img_gear, label, (x1, y1 - 5), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    print(f"   ✅ {len(results_gear.boxes)} pièces détectées")
    
    # ULTIMATE
    print("🌟 Analyse ULTIMATE...")
    results_ultimate = model_ultimate.predict(source=image_path, conf=conf, save=False, verbose=False)[0]
    img_ultimate = img_original.copy()
    
    for box in results_ultimate.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
        # Décaler les coordonnées pour la marge
        y1 += margin_top
        y2 += margin_top
        
        cls_id = int(box.cls[0])
        confidence = float(box.conf[0])
        class_name = results_ultimate.names[cls_id]
        
        short_name = get_short_name(class_name)
        label = format_label(short_name, confidence)
        
        cv2.rectangle(img_ultimate, (x1, y1), (x2, y2), (0, 255, 0), 2)
        (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(img_ultimate, (x1, y1 - 22), (x1 + w, y1), (0, 255, 0), -1)
        cv2.putText(img_ultimate, label, (x1, y1 - 5), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    print(f"   ✅ {len(results_ultimate.boxes)} pièces détectées")
    
    # Afficher les 3 résultats
    fig, axes = plt.subplots(1, 3, figsize=(24, 8))
    fig.patch.set_facecolor('black')  # Fond noir
    fig.suptitle('COMPARAISON 3 MODELES : HAKI | GEAR | ULTIMATE', fontsize=20, fontweight='bold', color='white')
    
    axes[0].imshow(cv2.cvtColor(img_haki, cv2.COLOR_BGR2RGB))
    axes[0].set_title(f'HAKI\n{len(results_haki.boxes)} pieces\n(Diagrammes 2D)', 
                     fontsize=14, fontweight='bold', color='cyan')
    axes[0].axis('off')
    axes[0].set_facecolor('black')
    
    axes[1].imshow(cv2.cvtColor(img_gear, cv2.COLOR_BGR2RGB))
    axes[1].set_title(f'GEAR\n{len(results_gear.boxes)} pieces\n(Photos 3D)', 
                     fontsize=14, fontweight='bold', color='orange')
    axes[1].axis('off')
    axes[1].set_facecolor('black')
    
    axes[2].imshow(cv2.cvtColor(img_ultimate, cv2.COLOR_BGR2RGB))
    axes[2].set_title(f'ULTIMATE\n{len(results_ultimate.boxes)} pieces\n(Universel)', 
                     fontsize=14, fontweight='bold', color='lime')
    axes[2].axis('off')
    axes[2].set_facecolor('black')
    
    plt.tight_layout()
    plt.show()
    
    print("\n✅ Analyse terminée !")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        analyze_with_three_models(sys.argv[1])
    else:
        print("Usage: python analyze_image.py <chemin_image>")
