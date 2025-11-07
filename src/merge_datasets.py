"""
Script pour fusionner le dataset Roboflow adapté avec le dataset actuel.
"""
import shutil
from pathlib import Path

def merge_datasets(dataset1_path, dataset2_path, output_path):
    """
    Fusionne deux datasets YOLO.
    
    Args:
        dataset1_path: Premier dataset (dataset actuel)
        dataset2_path: Deuxième dataset (Roboflow adapté)
        output_path: Chemin de sortie pour le dataset fusionné
    """
    dataset1 = Path(dataset1_path)
    dataset2 = Path(dataset2_path)
    output = Path(output_path)
    
    # Créer la structure de sortie
    for split in ['train', 'valid', 'test']:
        (output / split / 'images').mkdir(parents=True, exist_ok=True)
        (output / split / 'labels').mkdir(parents=True, exist_ok=True)
    
    stats = {'train': 0, 'valid': 0, 'test': 0}
    
    for split in ['train', 'valid', 'test']:
        print(f"\n📂 Fusion du split: {split}")
        
        # Copier depuis dataset1
        src_img1 = dataset1 / split / 'images'
        src_lbl1 = dataset1 / split / 'labels'
        
        if src_img1.exists():
            for img in src_img1.glob('*'):
                shutil.copy2(img, output / split / 'images' / img.name)
                stats[split] += 1
            
            for lbl in src_lbl1.glob('*.txt'):
                shutil.copy2(lbl, output / split / 'labels' / lbl.name)
            
            print(f"  ✓ Dataset 1: {len(list(src_img1.glob('*')))} images")
        
        # Copier depuis dataset2 (avec préfixe pour éviter les conflits)
        src_img2 = dataset2 / split / 'images'
        src_lbl2 = dataset2 / split / 'labels'
        
        if src_img2.exists():
            for img in src_img2.glob('*'):
                new_name = f"roboflow_{img.name}"
                shutil.copy2(img, output / split / 'images' / new_name)
                stats[split] += 1
            
            for lbl in src_lbl2.glob('*.txt'):
                new_name = f"roboflow_{lbl.name}"
                shutil.copy2(lbl, output / split / 'labels' / new_name)
            
            print(f"  ✓ Dataset 2: {len(list(src_img2.glob('*')))} images")
    
    # Créer le data.yaml
    yaml_content = f"""# Dataset fusionné pour fine-tuning
path: {output.absolute()}
train: train/images
val: valid/images
test: test/images

# Classes
nc: 13
names: ['bishop', 'black-bishop', 'black-king', 'black-knight', 'black-pawn', 
        'black-queen', 'black-rook', 'white-bishop', 'white-king', 'white-knight', 
        'white-pawn', 'white-queen', 'white-rook']
"""
    
    with open(output / 'data.yaml', 'w') as f:
        f.write(yaml_content)
    
    print(f"\n{'='*60}")
    print("✅ Fusion terminée!")
    print(f"{'='*60}")
    print(f"Train: {stats['train']} images")
    print(f"Valid: {stats['valid']} images")
    print(f"Test: {stats['test']} images")
    print(f"Total: {sum(stats.values())} images")
    print(f"\nDataset fusionné sauvegardé dans: {output}")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description="Fusionne deux datasets YOLO")
    parser.add_argument('--dataset1', type=str, 
                        default='data/processed',
                        help="Premier dataset (actuel)")
    parser.add_argument('--dataset2', type=str, 
                        default='data/roboflow_adapted',
                        help="Deuxième dataset (Roboflow)")
    parser.add_argument('--output', type=str, 
                        default='data/merged_dataset',
                        help="Dataset de sortie fusionné")
    
    args = parser.parse_args()
    
    print("🔀 Fusion des datasets")
    print(f"Dataset 1: {args.dataset1}")
    print(f"Dataset 2: {args.dataset2}")
    print(f"Output: {args.output}")
    
    merge_datasets(args.dataset1, args.dataset2, args.output)
