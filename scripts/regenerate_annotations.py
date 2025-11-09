"""
Régénère les prédictions Haki et Ultimate avec annotations courtes (wK, bQ, etc.)
"""

from pathlib import Path
from ultralytics import YOLO
import cv2

def get_short_name(class_name):
    """Convertit le nom de classe en notation courte (wK, bQ, etc.)"""
    mapping = {
        'white-king': 'wK',
        'white-queen': 'wQ',
        'white-rook': 'wR',
        'white-bishop': 'wB',
        'white-knight': 'wN',
        'white-pawn': 'wP',
        'black-king': 'bK',
        'black-queen': 'bQ',
        'black-rook': 'bR',
        'black-bishop': 'bB',
        'black-knight': 'bN',
        'black-pawn': 'bP',
        'king': 'K',
        'queen': 'Q',
        'rook': 'R',
        'bishop': 'B',
        'knight': 'N',
        'pawn': 'P'
    }
    return mapping.get(class_name.lower(), class_name)

def regenerate_predictions():
    """Régénère les prédictions avec annotations courtes"""
    
    print("\n" + "="*70)
    print("🔄 RÉGÉNÉRATION DES ANNOTATIONS (wK, bQ, wR, etc.)")
    print("="*70 + "\n")
    
    # Charger les modèles
    print("📦 Chargement des modèles...")
    haki_path = Path("models/senchess_haki_v1.0/weights/best.pt")
    ultimate_path = Path("models/senchess_ultimate_v1.0_quick/weights/best.pt")
    
    model_haki = YOLO(str(haki_path))
    model_ultimate = YOLO(str(ultimate_path))
    print("✅ Modèles chargés\n")
    
    # Images à traiter
    test_dir = Path("examples/imgTest")
    images = list(test_dir.glob("*.png"))
    
    for img_path in sorted(images):
        print(f"🎯 {img_path.name}")
        
        # HAKI
        results_haki = model_haki.predict(source=str(img_path), conf=0.25, save=False, verbose=False)[0]
        img_haki = cv2.imread(str(img_path))
        
        for box in results_haki.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            class_name = results_haki.names[cls_id]
            
            # Annotation
            short_name = get_short_name(class_name)
            label = f"{short_name} {conf:.2f}"
            
            # Rectangle bleu
            cv2.rectangle(img_haki, (x1, y1), (x2, y2), (255, 0, 0), 2)
            
            # Label
            (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(img_haki, (x1, y1 - 22), (x1 + w, y1), (255, 0, 0), -1)
            cv2.putText(img_haki, label, (x1, y1 - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Sauvegarder Haki (format .jpg pour correspondre à compare_all_models.py)
        save_dir_haki = Path(f"predictions/haki_{img_path.stem}2")
        save_dir_haki.mkdir(parents=True, exist_ok=True)
        save_path_haki = save_dir_haki / f"{img_path.stem}.jpg"
        cv2.imwrite(str(save_path_haki), img_haki)
        print(f"   ✅ Haki: {len(results_haki.boxes)} pièces → {save_path_haki}")
        
        # ULTIMATE
        results_ultimate = model_ultimate.predict(source=str(img_path), conf=0.25, save=False, verbose=False)[0]
        img_ultimate = cv2.imread(str(img_path))
        
        for box in results_ultimate.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            class_name = results_ultimate.names[cls_id]
            
            # Annotation
            short_name = get_short_name(class_name)
            label = f"{short_name} {conf:.2f}"
            
            # Rectangle vert
            cv2.rectangle(img_ultimate, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Label
            (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(img_ultimate, (x1, y1 - 22), (x1 + w, y1), (0, 255, 0), -1)
            cv2.putText(img_ultimate, label, (x1, y1 - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Sauvegarder Ultimate (format .jpg pour correspondre à compare_all_models.py)
        save_dir_ultimate = Path(f"predictions/ultimate_{img_path.stem}")
        save_dir_ultimate.mkdir(parents=True, exist_ok=True)
        save_path_ultimate = save_dir_ultimate / f"{img_path.stem}.jpg"
        cv2.imwrite(str(save_path_ultimate), img_ultimate)
        print(f"   ✅ Ultimate: {len(results_ultimate.boxes)} pièces → {save_path_ultimate}\n")
    
    print("="*70)
    print("✅ RÉGÉNÉRATION TERMINÉE")
    print("   📁 Haki: predictions/haki_*2/")
    print("   📁 Ultimate: predictions/ultimate_*/")
    print("="*70 + "\n")

if __name__ == '__main__':
    regenerate_predictions()
