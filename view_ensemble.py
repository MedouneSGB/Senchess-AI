"""
Visualisation des résultats du modèle Ensemble
Rouge = Haki (pièces stratégiques)
Vert = Ultimate (autres pièces)
"""

import cv2
import matplotlib.pyplot as plt
from pathlib import Path

def show_ensemble_results():
    """Affiche les résultats du modèle ensemble"""
    
    ensemble_dir = Path("predictions/ensemble")
    
    if not ensemble_dir.exists():
        print("❌ Dossier predictions/ensemble non trouvé")
        return
    
    images = list(ensemble_dir.glob("*.png"))
    
    if not images:
        print("❌ Aucune image trouvée dans predictions/ensemble")
        return
    
    print("\n" + "="*70)
    print("🏆 MODÈLE ENSEMBLE : ULTIMATE + HAKI")
    print("="*70)
    print("\n🔴 Rouge = Haki (King, Queen, Rook, Bishop)")
    print("🟢 Vert = Ultimate (Knights, Pawns)")
    print("="*70 + "\n")
    
    for img_path in sorted(images):
        img = cv2.imread(str(img_path))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        plt.figure(figsize=(16, 12))
        plt.imshow(img)
        plt.title(f'🏆 Ensemble: {img_path.name}\n🔴 Haki (stratégiques) + 🟢 Ultimate (autres)', 
                 fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.show()
        
        print(f"✅ {img_path.name}")
        print("   Fermez la fenêtre pour passer à l'image suivante...\n")
    
    print("✅ Toutes les images ensemble ont été affichées !\n")

if __name__ == '__main__':
    show_ensemble_results()
