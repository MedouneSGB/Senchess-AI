"""
Comparaison visuelle des 3 modèles sur une même interface
Haki | Ultimate | Ensemble
"""

import cv2
import matplotlib.pyplot as plt
from pathlib import Path

def compare_three_models():
    """Affiche Haki, Ultimate et Ensemble côte à côte"""
    
    print("\n" + "="*70)
    print("🎯 COMPARAISON 3 MODÈLES : HAKI | ULTIMATE | ENSEMBLE")
    print("="*70 + "\n")
    
    images = ["capture1", "capture2", "capture3", "cqpture"]
    
    for img_name in images:
        haki_path = Path(f"predictions/haki_{img_name}2/{img_name}.jpg")
        ultimate_path = Path(f"predictions/ultimate_{img_name}/{img_name}.jpg")
        ensemble_path = Path(f"predictions/ensemble/{img_name}.png")
        
        # Vérifier que les 3 existent
        if not all([haki_path.exists(), ultimate_path.exists(), ensemble_path.exists()]):
            print(f"⚠️  Fichiers manquants pour {img_name}")
            continue
        
        # Charger les 3 images
        img_haki = cv2.imread(str(haki_path))
        img_haki = cv2.cvtColor(img_haki, cv2.COLOR_BGR2RGB)
        
        img_ultimate = cv2.imread(str(ultimate_path))
        img_ultimate = cv2.cvtColor(img_ultimate, cv2.COLOR_BGR2RGB)
        
        img_ensemble = cv2.imread(str(ensemble_path))
        img_ensemble = cv2.cvtColor(img_ensemble, cv2.COLOR_BGR2RGB)
        
        # Créer une figure avec 3 colonnes
        fig, axes = plt.subplots(1, 3, figsize=(24, 8))
        fig.suptitle(f'COMPARAISON COMPLETE - {img_name}', fontsize=20, fontweight='bold')
        
        # Haki
        axes[0].imshow(img_haki)
        axes[0].set_title('HAKI\nSpecialiste Diagrammes\n(wKing wQueen wRook wBishop)', 
                         fontsize=14, fontweight='bold', color='red')
        axes[0].axis('off')
        
        # Ultimate
        axes[1].imshow(img_ultimate)
        axes[1].set_title('ULTIMATE\nChampion Universel\n(Maximum detections)', 
                         fontsize=14, fontweight='bold', color='green')
        axes[1].axis('off')
        
        # Ensemble
        axes[2].imshow(img_ensemble)
        axes[2].set_title('ENSEMBLE\nFusion Intelligente\n(Rouge=Haki Vert=Ultimate)', 
                         fontsize=14, fontweight='bold', color='blue')
        axes[2].axis('off')
        
        plt.tight_layout()
        plt.show()
        
        print(f"✅ {img_name} - Fermez pour continuer...\n")
    
    print("\n✅ Comparaison terminée !\n")

if __name__ == '__main__':
    compare_three_models()
