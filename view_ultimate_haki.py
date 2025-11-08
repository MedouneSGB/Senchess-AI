"""
Visualisation comparée Ultimate vs Haki
"""

import cv2
import matplotlib.pyplot as plt
from pathlib import Path

def show_ultimate_vs_haki():
    """Affiche les résultats Ultimate vs Haki côte à côte"""
    
    predictions_dir = Path("predictions")
    images = ["capture1", "capture2", "capture3", "cqpture"]
    
    print("\n" + "="*70)
    print("🖼️  VISUALISATION ULTIMATE vs HAKI")
    print("="*70 + "\n")
    
    for img_name in images:
        haki_path = predictions_dir / f"haki_{img_name}2" / f"{img_name}.jpg"
        ultimate_path = predictions_dir / f"ultimate_{img_name}" / f"{img_name}.jpg"
        
        if not haki_path.exists() and not ultimate_path.exists():
            print(f"⚠️  Résultats non trouvés pour {img_name}")
            continue
        
        # Créer une figure avec 2 sous-graphiques
        fig, axes = plt.subplots(1, 2, figsize=(20, 10))
        fig.suptitle(f'🏆 DUEL : Ultimate vs Haki - {img_name}', fontsize=18, fontweight='bold')
        
        # Afficher Haki
        if haki_path.exists():
            img_haki = cv2.imread(str(haki_path))
            img_haki = cv2.cvtColor(img_haki, cv2.COLOR_BGR2RGB)
            axes[0].imshow(img_haki)
            axes[0].set_title('🔴 HAKI (Spécialisé Diagrammes)', fontsize=16, fontweight='bold', color='red')
            axes[0].axis('off')
        else:
            axes[0].text(0.5, 0.5, 'Pas de résultat', ha='center', va='center', fontsize=14)
            axes[0].set_title('🔴 HAKI', fontsize=16)
            axes[0].axis('off')
        
        # Afficher Ultimate
        if ultimate_path.exists():
            img_ultimate = cv2.imread(str(ultimate_path))
            img_ultimate = cv2.cvtColor(img_ultimate, cv2.COLOR_BGR2RGB)
            axes[1].imshow(img_ultimate)
            axes[1].set_title('🌟 ULTIMATE (Champion Universel)', fontsize=16, fontweight='bold', color='green')
            axes[1].axis('off')
        else:
            axes[1].text(0.5, 0.5, 'Pas de résultat', ha='center', va='center', fontsize=14)
            axes[1].set_title('🌟 ULTIMATE', fontsize=16)
            axes[1].axis('off')
        
        plt.tight_layout()
        plt.show()
        
        print(f"✅ Affichage de {img_name}")
        print("   Fermez la fenêtre pour passer à l'image suivante...\n")

if __name__ == '__main__':
    show_ultimate_vs_haki()
    print("\n✅ Toutes les images ont été affichées !\n")
