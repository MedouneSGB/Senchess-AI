"""
Exemples d'utilisation de l'API Senchess AI
Testez facilement les différents modèles et fonctionnalités
"""

import requests
import json
from pathlib import Path

# URL de l'API déployée
API_URL = "https://senchess-api-929629832495.us-central1.run.app"

def test_health():
    """Test du endpoint /health"""
    print("=" * 60)
    print("TEST 1: Health Check")
    print("=" * 60)
    
    response = requests.get(f"{API_URL}/health")
    result = response.json()
    
    print(f"Status: {result['status']}")
    print(f"Modèle configuré: {result['model_type']}")
    print(f"Modèles chargés:")
    for model, loaded in result['models_loaded'].items():
        status = "✅" if loaded else "❌"
        print(f"  {status} {model}")
    print()


def test_prediction(image_path, model="ensemble"):
    """Test du endpoint /predict avec une image"""
    print("=" * 60)
    print(f"TEST 2: Prédiction avec modèle '{model}'")
    print("=" * 60)
    
    # Vérifier que l'image existe
    if not Path(image_path).exists():
        print(f"❌ Erreur: L'image {image_path} n'existe pas")
        return
    
    # Envoyer la requête
    with open(image_path, "rb") as f:
        files = {"image": f}
        data = {"model": model}
        
        print(f"📤 Envoi de l'image: {image_path}")
        response = requests.post(f"{API_URL}/predict", files=files, data=data)
    
    # Traiter la réponse
    if response.status_code == 200:
        result = response.json()
        
        if result['success']:
            print(f"\n✅ Prédiction réussie!")
            print(f"\n📋 Résultats:")
            print(f"  FEN: {result['fen']}")
            print(f"  Modèle utilisé: {result['model_used']}")
            print(f"  Pièces détectées: {result['detectedPieces']}")
            print(f"  Confiance moyenne: {result['confidence']:.1%}")
            print(f"  Taille image: {result['imageSize']['width']}x{result['imageSize']['height']}")
            
            print(f"\n🎯 Détail des pièces:")
            for piece in sorted(result['pieces'], key=lambda x: x['confidence'], reverse=True):
                print(f"  • {piece['class']:15} - Confiance: {piece['confidence']:.1%}")
            
            if result['warnings']:
                print(f"\n⚠️  Avertissements:")
                for warning in result['warnings']:
                    print(f"  • {warning}")
        else:
            print(f"❌ Erreur: {result.get('error', 'Erreur inconnue')}")
    else:
        print(f"❌ Erreur HTTP {response.status_code}")
        print(response.text)
    
    print()


def compare_models(image_path):
    """Compare les performances des trois modèles"""
    print("=" * 60)
    print("TEST 3: Comparaison des Modèles")
    print("=" * 60)
    
    models = ["gear", "haki", "ensemble"]
    results = {}
    
    for model in models:
        print(f"\n🔄 Test avec modèle: {model}")
        
        with open(image_path, "rb") as f:
            files = {"image": f}
            data = {"model": model}
            response = requests.post(f"{API_URL}/predict", files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                results[model] = {
                    'pieces': result['detectedPieces'],
                    'confidence': result['confidence'],
                    'fen': result['fen']
                }
                print(f"  ✅ {result['detectedPieces']} pièces détectées - Confiance: {result['confidence']:.1%}")
            else:
                print(f"  ❌ Erreur: {result.get('error')}")
        else:
            print(f"  ❌ Erreur HTTP {response.status_code}")
    
    # Résumé comparatif
    print(f"\n📊 Résumé Comparatif:")
    print(f"{'Modèle':<12} {'Pièces':<8} {'Confiance':<12} {'FEN Identique'}")
    print("-" * 60)
    
    base_fen = results.get('gear', {}).get('fen', '')
    for model, data in results.items():
        fen_match = "✅" if data['fen'] == base_fen else "⚠️ "
        print(f"{model:<12} {data['pieces']:<8} {data['confidence']:<11.1%} {fen_match}")
    
    print()


def test_error_handling():
    """Test de la gestion des erreurs"""
    print("=" * 60)
    print("TEST 4: Gestion des Erreurs")
    print("=" * 60)
    
    # Test sans image
    print("\n1. Test sans image:")
    response = requests.post(f"{API_URL}/predict")
    print(f"   Status: {response.status_code}")
    if response.status_code != 200:
        print(f"   ✅ Erreur correctement gérée")
    
    # Test avec modèle invalide
    print("\n2. Test avec modèle invalide:")
    files = {"image": open("imgTest/capture2.jpg", "rb")}
    data = {"model": "invalid_model"}
    response = requests.post(f"{API_URL}/predict", files=files, data=data)
    result = response.json()
    print(f"   Status: {response.status_code}")
    error_msg = result.get('error', 'Pas d\'erreur')
    print(f"   Message: {error_msg}")
    
    print()


def save_results(image_path, output_path="api_test_results.json"):
    """Sauvegarde les résultats dans un fichier JSON"""
    print("=" * 60)
    print("TEST 5: Sauvegarde des Résultats")
    print("=" * 60)
    
    with open(image_path, "rb") as f:
        files = {"image": f}
        response = requests.post(f"{API_URL}/predict", files=files)
    
    if response.status_code == 200:
        result = response.json()
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Résultats sauvegardés dans: {output_path}")
        print(f"📊 Taille du fichier: {Path(output_path).stat().st_size} octets")
    else:
        print(f"❌ Erreur lors de la récupération des résultats")
    
    print()


def main():
    """Exécute tous les tests"""
    print("\n" + "🎯" * 30)
    print("  TESTS DE L'API SENCHESS AI")
    print("🎯" * 30 + "\n")
    
    # Chemin vers l'image de test
    image_path = "imgTest/capture2.jpg"
    
    try:
        # Test 1: Health check
        test_health()
        
        # Test 2: Prédiction avec ensemble
        test_prediction(image_path, model="ensemble")
        
        # Test 3: Comparaison des modèles
        compare_models(image_path)
        
        # Test 4: Gestion des erreurs
        test_error_handling()
        
        # Test 5: Sauvegarde des résultats
        save_results(image_path)
        
        print("=" * 60)
        print("✅ TOUS LES TESTS TERMINÉS")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
