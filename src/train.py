import os
import argparse
from ultralytics import YOLO
import torch

def train_model(data_yaml, epochs, batch_size, img_size, model_name='yolov8n.pt', project='models', name='chess_detector'):
    """
    Lance l'entraînement d'un modèle YOLOv8 pour la détection de pièces d'échecs.
    """
    # Vérifier la disponibilité d'un GPU
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Utilisation du device : {device}")

    # Charger un modèle pré-entraîné ou un modèle existant pour fine-tuning
    # yolov8n.pt est le plus petit et rapide. Pour plus de précision,
    # on peut utiliser yolov8s.pt, yolov8m.pt, yolov8l.pt ou yolov8x.pt.
    print(f"Chargement du modèle : {model_name}")
    model = YOLO(model_name)
    model.to(device)

    # Entraîner le modèle
    # Les résultats (modèles, graphiques, etc.) seront sauvegardés dans le dossier project/name
    print("Lancement de l'entraînement...")
    results = model.train(
        data=data_yaml,
        epochs=epochs,
        batch=batch_size,
        imgsz=img_size,
        project=project,  # Dossier racine pour sauvegarder les entraînements
        name=name         # Nom du sous-dossier pour cet entraînement spécifique
    )

    print("\nEntraînement terminé.")
    # Le meilleur modèle est automatiquement sauvegardé sous project/name/weights/best.pt
    print(f"Le meilleur modèle est sauvegardé ici : {results.save_dir}/weights/best.pt")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script d'entraînement du modèle de détection de pièces d'échecs.")
    
    parser.add_argument('--data-yaml', type=str, default='data/chess_dataset.yaml', help="Chemin vers le fichier de configuration du dataset (.yaml).")
    parser.add_argument('--epochs', type=int, default=50, help="Nombre d'époques pour l'entraînement.")
    parser.add_argument('--batch-size', type=int, default=16, help="Taille du batch. Réduire si vous manquez de mémoire GPU.")
    parser.add_argument('--img-size', type=int, default=640, help="Taille des images pour l'entraînement (carré).")
    parser.add_argument('--model', type=str, default='yolov8n.pt', help="Modèle de base à utiliser (ex: yolov8n.pt, yolov8s.pt) ou chemin vers un modèle pour fine-tuning.")
    parser.add_argument('--project', type=str, default='models', help="Dossier racine pour sauvegarder l'entraînement.")
    parser.add_argument('--name', type=str, default='chess_detector', help="Nom du sous-dossier pour cet entraînement.")

    args = parser.parse_args()

    # Vérifier si le fichier de données existe
    if not os.path.exists(args.data_yaml):
        print(f"Erreur : Le fichier de configuration '{args.data_yaml}' n'a pas été trouvé.")
        print("Veuillez vous assurer que le fichier existe et que le chemin est correct.")
    else:
        train_model(
            data_yaml=args.data_yaml,
            epochs=args.epochs,
            batch_size=args.batch_size,
            img_size=args.img_size,
            model_name=args.model,
            project=args.project,
            name=args.name
        )
