import os
import shutil
import random
import argparse

def split_data(input_folder, output_folder, train_ratio=0.8, val_ratio=0.1):
    """
    Répartit les images et les annotations en ensembles d'entraînement, de validation et de test.

    La structure attendue dans input_folder :
    - un sous-dossier 'images'
    - un sous-dossier 'labels'

    La structure créée dans output_folder :
    - images/train, images/val, images/test
    - labels/train, labels/val, labels/test
    """
    # Chemins des dossiers sources
    images_src_dir = os.path.join(input_folder, 'images')
    labels_src_dir = os.path.join(input_folder, 'labels')

    if not os.path.isdir(images_src_dir) or not os.path.isdir(labels_src_dir):
        print(f"Erreur : Les dossiers 'images' et 'labels' doivent exister dans '{input_folder}'")
        print("Veuillez placer vos images dans 'data/raw/images' et vos annotations dans 'data/raw/labels'.")
        return

    # Chemins des dossiers de destination
    sets = ['train', 'val', 'test']
    for s in sets:
        os.makedirs(os.path.join(output_folder, 'images', s), exist_ok=True)
        os.makedirs(os.path.join(output_folder, 'labels', s), exist_ok=True)

    # Liste des fichiers (sans extension)
    image_files = [os.path.splitext(f)[0] for f in os.listdir(images_src_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
    random.shuffle(image_files)

    # Calcul des divisions
    total_files = len(image_files)
    train_end = int(total_files * train_ratio)
    val_end = int(total_files * (train_ratio + val_ratio))

    splits = {
        'train': image_files[:train_end],
        'val': image_files[train_end:val_end],
        'test': image_files[val_end:]
    }

    # Copie des fichiers
    for split_name, file_list in splits.items():
        print(f"Traitement de l'ensemble '{split_name}' ({len(file_list)} fichiers)...")
        for filename in file_list:
            # On cherche le fichier image original avec son extension
            img_ext = '.jpg' # default
            for ext in ['.jpg', '.jpeg', '.png']:
                if os.path.exists(os.path.join(images_src_dir, filename + ext)):
                    img_ext = ext
                    break
            
            # Chemins source
            img_src_path = os.path.join(images_src_dir, filename + img_ext)
            label_src_path = os.path.join(labels_src_dir, filename + '.txt')

            # Chemins destination
            img_dest_path = os.path.join(output_folder, 'images', split_name, filename + img_ext)
            label_dest_path = os.path.join(output_folder, 'labels', split_name, filename + '.txt')

            # Copie
            if os.path.exists(img_src_path):
                shutil.copy(img_src_path, img_dest_path)
            if os.path.exists(label_src_path):
                shutil.copy(label_src_path, label_dest_path)

    print("\nRépartition des données terminée.")
    print(f"  - Entraînement : {len(splits['train'])} images")
    print(f"  - Validation   : {len(splits['val'])} images")
    print(f"  - Test         : {len(splits['test'])} images")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Prépare et répartit les données d'échecs.")
    parser.add_argument('--input-folder', type=str, default='data/raw', help="Dossier contenant les sous-dossiers 'images' et 'labels'.")
    parser.add_argument('--output-folder', type=str, default='data/processed', help="Dossier où sauvegarder les ensembles train/val/test.")
    
    args = parser.parse_args()

    # Création de dossiers de démonstration si le dossier raw est vide
    if not os.path.exists(args.input_folder) or not os.listdir(args.input_folder):
        print("Le dossier 'data/raw' est vide ou n'existe pas. Création d'une structure de démonstration.")
        os.makedirs(os.path.join(args.input_folder, 'images'), exist_ok=True)
        os.makedirs(os.path.join(args.input_folder, 'labels'), exist_ok=True)
        print("\nVeuillez placer vos images dans 'data/raw/images' et vos annotations (fichiers .txt) dans 'data/raw/labels'.")
        print("Assurez-vous que chaque image a un fichier d'annotation avec le même nom (ex: 'partie1.jpg' et 'partie1.txt').")
    else:
        split_data(args.input_folder, args.output_folder)
