"""
Script de test local pour l'API Senchess
Permet de tester l'API avant le déploiement
"""

import requests
import sys
from pathlib import Path

def test_api(base_url="http://localhost:5000"):
    """Teste les différents endpoints de l'API"""
    
    print(f"🧪 Test de l'API Senchess : {base_url}\n")
    
    # 1. Test de la page d'accueil
    print("1️⃣ Test de la page d'accueil...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print(f"✅ Page d'accueil OK")
            print(f"   {response.json()}\n")
        else:
            print(f"❌ Erreur : {response.status_code}\n")
    except Exception as e:
        print(f"❌ Erreur de connexion : {e}\n")
        return
    
    # 2. Test du health check
    print("2️⃣ Test du health check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check OK")
            print(f"   Status: {data['status']}")
            print(f"   Model loaded: {data['model_loaded']}\n")
        else:
            print(f"❌ Erreur : {response.status_code}\n")
    except Exception as e:
        print(f"❌ Erreur : {e}\n")
    
    # 3. Test de prédiction
    print("3️⃣ Test de prédiction...")
    
    # Chercher une image de test
    test_images = [
        Path("imgTest/capture.jpg"),
        Path("imgTest/capture2.jpg"),
        Path("imgTest/capture3.jpg"),
    ]
    
    test_image = None
    for img in test_images:
        if img.exists():
            test_image = img
            break
    
    if not test_image:
        print("⚠️ Aucune image de test trouvée dans imgTest/")
        print("   Veuillez placer une image d'échiquier dans imgTest/capture.jpg\n")
        return
    
    print(f"   Utilisation de : {test_image}")
    
    try:
        with open(test_image, 'rb') as f:
            files = {'image': f}
            data = {'conf': '0.25'}
            
            response = requests.post(
                f"{base_url}/predict",
                files=files,
                data=data
            )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Prédiction réussie")
            print(f"   FEN: {result['fen']}")
            print(f"   Pièces détectées: {result['detectedPieces']}")
            print(f"   Confiance moyenne: {result['confidence']}")
            
            if result['warnings']:
                print(f"   ⚠️ Avertissements: {', '.join(result['warnings'])}")
            
            print(f"\n   Détails des pièces:")
            for piece in result['pieces'][:5]:  # Afficher les 5 premières
                print(f"     - {piece['class']}: {piece['confidence']}")
            
            if len(result['pieces']) > 5:
                print(f"     ... et {len(result['pieces']) - 5} autres")
            
            print("\n✅ Tous les tests sont passés !")
        else:
            print(f"❌ Erreur : {response.status_code}")
            print(f"   {response.json()}")
    
    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    # URL de l'API (local ou Vercel)
    if len(sys.argv) > 1:
        api_url = sys.argv[1]
    else:
        api_url = "http://localhost:5000"
    
    test_api(api_url)
