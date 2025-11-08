"""
Script pour visualiser les résultats des détections
"""
import cv2
import matplotlib.pyplot as plt
from pathlib import Path

def show_results():
    """Affiche les résultats des détections Haki, Gear et Ultimate côte à côte"""
    
    predictions_dir = Path("predictions")
    images = ["capture1", "capture2", "capture3", "cqpture"]
    
    for img_name in images:
        haki_path = predictions_dir / f"haki_{img_name}2" / f"{img_name}.jpg"
        gear_path = predictions_dir / f"gear_{img_name}2" / f"{img_name}.jpg"
        ultimate_path = predictions_dir / f"ultimate_{img_name}" / f"{img_name}.jpg"
        
        if not haki_path.exists() and not gear_path.exists() and not ultimate_path.exists():
            print(f"⚠️  Résultats non trouvés pour {img_name}")
            continue
        
        # Créer une figure avec 3 sous-graphiques
        fig, axes = plt.subplots(1, 3, figsize=(24, 8))
        fig.suptitle(f'Comparaison Haki vs Gear vs Ultimate - {img_name}', fontsize=16, fontweight='bold')
        
        # Afficher Haki
        if haki_path.exists():
            img_haki = cv2.imread(str(haki_path))
            img_haki = cv2.cvtColor(img_haki, cv2.COLOR_BGR2RGB)
            axes[0].imshow(img_haki)
            axes[0].set_title('🔴 Modèle HAKI (Screenshots/Diagrammes)', fontsize=14, fontweight='bold')
            axes[0].axis('off')
        else:
            axes[0].text(0.5, 0.5, 'Pas de résultat', ha='center', va='center')
            axes[0].set_title('🔴 Modèle HAKI', fontsize=14)
            axes[0].axis('off')
        
        # Afficher Gear
        if gear_path.exists():
            img_gear = cv2.imread(str(gear_path))
            img_gear = cv2.cvtColor(img_gear, cv2.COLOR_BGR2RGB)
            axes[1].imshow(img_gear)
            axes[1].set_title('⚫ Modèle GEAR (Photos physiques)', fontsize=14, fontweight='bold')
            axes[1].axis('off')
        else:
            axes[1].text(0.5, 0.5, 'Pas de résultat', ha='center', va='center')
            axes[1].set_title('⚫ Modèle GEAR', fontsize=14)
            axes[1].axis('off')
        
        # Afficher Ultimate
        if ultimate_path.exists():
            img_ultimate = cv2.imread(str(ultimate_path))
            img_ultimate = cv2.cvtColor(img_ultimate, cv2.COLOR_BGR2RGB)
            axes[2].imshow(img_ultimate)
            axes[2].set_title('🌟 Modèle ULTIMATE (Universel)', fontsize=14, fontweight='bold')
            axes[2].axis('off')
        else:
            axes[2].text(0.5, 0.5, 'Pas de résultat', ha='center', va='center')
            axes[2].set_title('🌟 Modèle ULTIMATE', fontsize=14)
            axes[2].axis('off')
        
        plt.tight_layout()
        plt.show()
        
        # Pause pour voir l'image
        print(f"\n✅ Affichage de {img_name}")
        print("   Fermez la fenêtre pour passer à l'image suivante...\n")

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🖼️  VISUALISATION DES RÉSULTATS")
    print("="*70 + "\n")
    show_results()
    print("\n✅ Toutes les images ont été affichées !\n")
