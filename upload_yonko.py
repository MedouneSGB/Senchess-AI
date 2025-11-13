"""
Script pour uploader le modèle Yonko sur Hugging Face Hub
"""

from huggingface_hub import HfApi, login
from pathlib import Path

def upload_yonko_model(repo_id="MedouneSGB/senchess-models"):
    """Upload le modèle Yonko vers Hugging Face"""
    
    print("🚀 Upload du modèle Yonko vers Hugging Face Hub\n")
    
    # 1. Login à Hugging Face
    print("1️⃣ Connexion à Hugging Face...")
    print("Veuillez vous connecter avec votre token Hugging Face")
    login()
    
    api = HfApi()
    print(f"✅ Connecté\n")
    print(f"📦 Repository: {repo_id}\n")
    
    # 2. Uploader le modèle Yonko
    model_path = Path('models/senchess_yonko_v1.0/weights/best.pt')
    
    if not model_path.exists():
        print(f"❌ Modèle non trouvé: {model_path}")
        return
    
    # Obtenir la taille du fichier
    size_mb = model_path.stat().st_size / (1024 * 1024)
    
    print(f"2️⃣ Upload de yonko_v1.0.pt ({size_mb:.1f} MB)...")
    print(f"   Description: Modèle Yonko v1.0 - Entraîné sur 10000 images avec augmentation")
    
    try:
        # Upload le fichier
        url = api.upload_file(
            path_or_fileobj=str(model_path),
            path_in_repo='yonko_v1.0.pt',
            repo_id=repo_id,
            repo_type="model",
        )
        print(f"✅ Uploadé: yonko_v1.0.pt")
        print(f"📍 URL: {url}")
    except Exception as e:
        print(f"❌ Erreur upload: {e}")
        return
    
    # 3. Mettre à jour le README
    print("\n3️⃣ Mise à jour du README...")
    
    try:
        # Télécharger le README existant
        try:
            readme_content = api.hf_hub_download(
                repo_id=repo_id,
                filename="README.md",
                repo_type="model"
            )
            with open(readme_content, 'r', encoding='utf-8') as f:
                readme_text = f.read()
        except:
            readme_text = ""
        
        # Ajouter la section Yonko si elle n'existe pas
        if "yonko_v1.0.pt" not in readme_text:
            yonko_section = """
### 🌊 Yonko v1.0 (`yonko_v1.0.pt`)
- **Usage**: Modèle entraîné sur un large dataset (10000 images) avec augmentation de données
- **Classes**: Toutes les pièces d'échecs
- **Dataset**: 10000+ images avec augmentation
- **Recommandé pour**: Détection robuste avec grande variété de conditions
"""
            # Insérer après la section Haki
            if "### 🔍 Haki v1.0" in readme_text:
                readme_text = readme_text.replace(
                    "## Utilisation",
                    yonko_section + "\n## Utilisation"
                )
            
            # Ajouter dans la liste des modèles uploadés
            if "## Modèles uploadés" in readme_text:
                readme_text = readme_text.replace(
                    "## License",
                    "- ✅ yonko_v1.0.pt\n\n## License"
                )
            
            # Upload le README mis à jour
            api.upload_file(
                path_or_fileobj=readme_text.encode(),
                path_in_repo="README.md",
                repo_id=repo_id,
                repo_type="model",
            )
            print("✅ README mis à jour\n")
        else:
            print("✅ README déjà à jour\n")
    except Exception as e:
        print(f"⚠️ Erreur mise à jour README: {e}\n")
    
    # 4. Résumé
    print("=" * 60)
    print("✅ UPLOAD TERMINÉ !")
    print("=" * 60)
    print(f"\n🌐 Repository: https://huggingface.co/{repo_id}")
    print(f"\n💡 Le modèle Yonko est maintenant disponible pour l'API!")
    print(f"\n📝 Fichier uploadé: yonko_v1.0.pt")

if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════╗
║         UPLOAD MODÈLE YONKO → HUGGING FACE                ║
╚═══════════════════════════════════════════════════════════╝

Avant de commencer, assurez-vous de :
1. Avoir un compte Hugging Face
2. Avoir créé un token: https://huggingface.co/settings/tokens
   - Permissions: "Write access to contents of all repos"

""")
    
    input("Appuyez sur ENTRÉE pour continuer...")
    
    try:
        upload_yonko_model()
        print(f"\n🎉 Succès !")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        print("\n💡 Assurez-vous d'avoir installé huggingface_hub:")
        print("   pip install huggingface_hub")
