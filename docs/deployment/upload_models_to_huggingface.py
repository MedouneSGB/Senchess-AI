"""
Script pour uploader les modèles Haki et Gear sur Hugging Face Hub
Permet de déployer les modèles pour les utiliser avec Vercel
"""

from huggingface_hub import HfApi, create_repo, login
from pathlib import Path
import os

def upload_models_to_huggingface(
    hf_token=None,
    repo_name="senchess-models",
    username=None
):
    """
    Upload les modèles Haki et Gear vers Hugging Face
    
    Args:
        hf_token: Token Hugging Face (ou None pour utiliser le login interactif)
        repo_name: Nom du repository sur HF
        username: Votre username HF
    """
    
    print("🚀 Upload des modèles Senchess vers Hugging Face Hub\n")
    
    # 1. Login à Hugging Face
    print("1️⃣ Connexion à Hugging Face...")
    if hf_token:
        login(token=hf_token)
        print("✅ Connecté avec token\n")
    else:
        print("Veuillez vous connecter à Hugging Face")
        print("Créez un token sur : https://huggingface.co/settings/tokens")
        login()
    
    # 2. Récupérer le username si nécessaire
    api = HfApi()
    if not username:
        user_info = api.whoami()
        username = user_info['name']
    
    repo_id = f"{username}/{repo_name}"
    print(f"📦 Repository: {repo_id}\n")
    
    # 3. Créer le repository (ou vérifier qu'il existe)
    print("2️⃣ Création/vérification du repository...")
    try:
        create_repo(
            repo_id=repo_id,
            repo_type="model",
            exist_ok=True,
            private=False  # Changez en True si vous voulez un repo privé
        )
        print(f"✅ Repository créé/vérifié: https://huggingface.co/{repo_id}\n")
    except Exception as e:
        print(f"⚠️ Erreur création repo: {e}\n")
    
    # 4. Uploader les modèles
    models = [
        {
            'path': 'models/senchess_gear_v1.1/weights/best.pt',
            'name': 'gear_v1.1.pt',
            'description': 'Modèle Gear v1.1 - Détection générale'
        },
        {
            'path': 'models/senchess_haki_v1.0/weights/best.pt',
            'name': 'haki_v1.0.pt',
            'description': 'Modèle Haki v1.0 - Pièces stratégiques'
        }
    ]
    
    print("3️⃣ Upload des modèles...")
    
    uploaded_files = []
    
    for model in models:
        model_path = Path(model['path'])
        
        if not model_path.exists():
            print(f"⚠️ Modèle non trouvé: {model_path}")
            continue
        
        # Obtenir la taille du fichier
        size_mb = model_path.stat().st_size / (1024 * 1024)
        
        print(f"\n📤 Upload de {model['name']} ({size_mb:.1f} MB)...")
        print(f"   Description: {model['description']}")
        
        try:
            # Upload le fichier
            url = api.upload_file(
                path_or_fileobj=str(model_path),
                path_in_repo=model['name'],
                repo_id=repo_id,
                repo_type="model",
            )
            print(f"✅ Uploadé: {model['name']}")
            uploaded_files.append(model['name'])
        except Exception as e:
            print(f"❌ Erreur upload {model['name']}: {e}")
    
    # 5. Créer un README
    print("\n4️⃣ Création du README...")
    
    readme_content = f"""---
language: en
tags:
  - computer-vision
  - object-detection
  - yolo
  - chess
  - ultralytics
license: mit
---

# Senchess AI - Chess Piece Detection Models

Modèles YOLO pour la détection de pièces d'échecs.

## Modèles disponibles

### 🎯 Gear v1.1 (`gear_v1.1.pt`)
- **Usage**: Détection générale de toutes les pièces
- **Classes**: Toutes les pièces d'échecs (pions, tours, cavaliers, fous, dames, rois)
- **Recommandé pour**: Détection complète d'un échiquier

### 🔍 Haki v1.0 (`haki_v1.0.pt`)
- **Usage**: Détection optimisée des pièces stratégiques
- **Classes**: Roi, Dame, Tour, Fou (meilleure précision)
- **Recommandé pour**: Identification précise des pièces importantes

## Utilisation

```python
from huggingface_hub import hf_hub_download
from ultralytics import YOLO

# Télécharger et charger le modèle Gear
model_path = hf_hub_download(
    repo_id="{repo_id}",
    filename="gear_v1.1.pt",
    cache_dir="/tmp"
)
model = YOLO(model_path)

# Prédiction
results = model.predict("chess_board.jpg", conf=0.25)
```

## API Vercel

Ces modèles sont utilisés dans l'API Senchess déployée sur Vercel.

Repository: https://github.com/MedouneSGB/Senchess-AI

## Modèles uploadés

{chr(10).join(f"- ✅ {file}" for file in uploaded_files)}

## License

MIT License - Libre d'utilisation
"""
    
    try:
        # Upload le README
        api.upload_file(
            path_or_fileobj=readme_content.encode(),
            path_in_repo="README.md",
            repo_id=repo_id,
            repo_type="model",
        )
        print("✅ README créé\n")
    except Exception as e:
        print(f"⚠️ Erreur création README: {e}\n")
    
    # 6. Résumé
    print("=" * 60)
    print("✅ UPLOAD TERMINÉ !")
    print("=" * 60)
    print(f"\n🌐 Votre repository: https://huggingface.co/{repo_id}")
    print(f"\n📝 Configuration pour l'API (à ajouter dans .env):")
    print(f"HUGGINGFACE_REPO_ID={repo_id}")
    print(f"\n💡 Les modèles sont maintenant disponibles pour Vercel!")
    
    return repo_id

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Upload les modèles Senchess vers Hugging Face')
    parser.add_argument('--token', type=str, help='Token Hugging Face (optionnel)')
    parser.add_argument('--repo', type=str, default='senchess-models', help='Nom du repository')
    parser.add_argument('--username', type=str, help='Username Hugging Face (optionnel)')
    
    args = parser.parse_args()
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║         UPLOAD MODÈLES SENCHESS → HUGGING FACE            ║
╚═══════════════════════════════════════════════════════════╝
    
Avant de commencer, assurez-vous de :
1. Avoir un compte Hugging Face (gratuit)
2. Avoir créé un token: https://huggingface.co/settings/tokens
   - Permissions nécessaires: "Write access to contents of all repos"
    
""")
    
    input("Appuyez sur ENTRÉE pour continuer...")
    
    try:
        repo_id = upload_models_to_huggingface(
            hf_token=args.token,
            repo_name=args.repo,
            username=args.username
        )
        
        print(f"\n🎉 Succès ! Repository: {repo_id}")
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        print("\n💡 Assurez-vous d'avoir installé huggingface_hub:")
        print("   pip install huggingface_hub")
