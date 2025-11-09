# 🚀 Déploiement de l'API Senchess sur Vercel

Ce guide vous explique comment déployer votre API de détection d'échecs sur Vercel.

## 📋 Prérequis

1. Un compte [Vercel](https://vercel.com) (gratuit)
2. Le [CLI Vercel](https://vercel.com/cli) installé : `npm i -g vercel`
3. Votre modèle YOLO entraîné (fichier `.pt`)

## ⚠️ Important : Limitation des Modèles

**Problème** : Les fichiers de modèles YOLO (`.pt`) sont trop volumineux pour être déployés directement sur Vercel (limite de 250MB pour le déploiement).

### Solutions possibles :

### Option 1 : Hébergement externe du modèle (Recommandé)

1. **Héberger le modèle sur un service de stockage cloud** :
   - Google Cloud Storage
   - AWS S3
   - Azure Blob Storage
   - Hugging Face Hub

2. **Télécharger le modèle au démarrage** :
   Modifiez `api/index.py` :

```python
import requests
from pathlib import Path

def load_model():
    """Charge le modèle YOLO depuis un URL"""
    global model
    
    model_url = os.environ.get('MODEL_URL')
    local_path = '/tmp/model.pt'
    
    # Télécharger si pas déjà présent
    if not os.path.exists(local_path):
        print(f"📥 Téléchargement du modèle depuis {model_url}...")
        response = requests.get(model_url)
        with open(local_path, 'wb') as f:
            f.write(response.content)
        print("✅ Modèle téléchargé")
    
    model = YOLO(local_path)
```

### Option 2 : Utiliser Hugging Face

Hébergez votre modèle sur Hugging Face :

```bash
# Installer huggingface_hub
pip install huggingface_hub

# Uploader le modèle
from huggingface_hub import HfApi
api = HfApi()
api.upload_file(
    path_or_fileobj="models/senchess_gear_v1.1/weights/best.pt",
    path_in_repo="best.pt",
    repo_id="votre-username/senchess-model",
    repo_type="model"
)
```

Puis dans `api/index.py` :

```python
from huggingface_hub import hf_hub_download

def load_model():
    global model
    model_path = hf_hub_download(
        repo_id="votre-username/senchess-model",
        filename="best.pt",
        cache_dir="/tmp"
    )
    model = YOLO(model_path)
```

### Option 3 : Déploiement sur une plateforme différente

Si vous avez besoin d'héberger des fichiers volumineux :
- **Railway** (support des volumes persistants)
- **Render** (déploiement Docker)
- **Google Cloud Run**
- **AWS Lambda** (avec EFS)

## 🛠️ Déploiement sur Vercel

### Étape 1 : Préparer votre projet

1. Assurez-vous que tous les fichiers sont en place :
```
Senchess AI/
├── api/
│   ├── index.py          # API Flask
│   └── requirements.txt  # Dépendances Python
├── vercel.json          # Configuration Vercel
└── .vercelignore        # Fichiers à ignorer
```

2. Hébergez votre modèle (voir options ci-dessus)

### Étape 2 : Configuration des variables d'environnement

Créez un fichier `.env.local` (ne pas commiter) :

```bash
MODEL_URL=https://votre-url/model.pt
# ou
HF_REPO_ID=votre-username/senchess-model
```

### Étape 3 : Déployer

```bash
# Depuis le répertoire racine du projet
cd "/Users/macbookair/Desktop/Senchess AI"

# Login à Vercel
vercel login

# Déployer en preview
vercel

# Ou déployer en production directement
vercel --prod
```

### Étape 4 : Configurer les variables d'environnement sur Vercel

Depuis le dashboard Vercel :
1. Allez dans votre projet → Settings → Environment Variables
2. Ajoutez :
   - `MODEL_URL` : URL de votre modèle
   - `MODEL_API_KEY` : (optionnel) pour sécuriser l'accès

## 🧪 Tester l'API

### En local :

```bash
# Installer les dépendances
cd api
pip install -r requirements.txt

# Lancer l'API
python index.py

# L'API sera disponible sur http://localhost:5000
```

### Test avec curl :

```bash
# Health check
curl https://votre-app.vercel.app/health

# Prédiction avec une image
curl -X POST https://votre-app.vercel.app/predict \
  -F "image=@path/to/chess.jpg" \
  -F "conf=0.25"
```

### Test avec JavaScript (comme dans votre site) :

```typescript
// src/services/chessImageRecognition.ts

export async function analyzeChessBoardImage(
  imageUrl: string
): Promise<ChessPositionAnalysis> {
  try {
    // 1. Préparer l'image
    const imageBlob = await fetch(imageUrl).then(r => r.blob());
    
    // 2. Créer FormData
    const formData = new FormData();
    formData.append('image', imageBlob);
    formData.append('conf', '0.25');
    
    // 3. Appeler votre API Vercel
    const response = await fetch('https://votre-app.vercel.app/predict', {
      method: 'POST',
      body: formData,
      // headers: {
      //   'Authorization': `Bearer ${import.meta.env.VITE_MODEL_API_KEY}`
      // }
    });
    
    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }
    
    const result = await response.json();
    
    // 4. Le résultat contient déjà le FEN !
    return {
      fen: result.fen,
      description: result.description,
      confidence: result.confidence > 0.9 ? 'high' : 
                  result.confidence > 0.7 ? 'medium' : 'low',
      detectedPieces: result.detectedPieces,
      warnings: result.warnings || []
    };
    
  } catch (error) {
    console.error('Model Recognition Error:', error);
    throw new Error('Échec de reconnaissance du modèle');
  }
}
```

## 📊 Format de réponse de l'API

```json
{
  "success": true,
  "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
  "pieces": [
    {
      "id": 1,
      "class": "white-king",
      "confidence": 0.95,
      "bbox": {
        "x1": 123.45,
        "y1": 234.56,
        "x2": 178.90,
        "y2": 289.12,
        "width": 55.45,
        "height": 54.56
      }
    }
  ],
  "confidence": 0.89,
  "detectedPieces": 32,
  "description": "Position détectée avec 32 pièces",
  "imageSize": {
    "width": 800,
    "height": 800
  },
  "warnings": []
}
```

## 🔒 Sécurité (Optionnel)

Pour protéger votre API, ajoutez une authentification :

```python
# Dans api/index.py
from functools import wraps

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('Authorization', '').replace('Bearer ', '')
        expected_key = os.environ.get('API_KEY')
        
        if not expected_key or api_key != expected_key:
            return jsonify({'error': 'Unauthorized'}), 401
        
        return f(*args, **kwargs)
    return decorated_function

@app.route('/predict', methods=['POST'])
@require_api_key  # Ajouter ce décorateur
def predict():
    # ... reste du code
```

## 📈 Monitoring

Sur Vercel, vous pouvez :
- Voir les logs en temps réel : `vercel logs`
- Monitorer les requêtes dans le dashboard
- Configurer des alertes

## 🐛 Dépannage

### Erreur : "Module not found"
- Vérifiez que `api/requirements.txt` contient toutes les dépendances

### Erreur : "Model not loaded"
- Vérifiez que `MODEL_URL` est correctement configuré
- Testez l'URL du modèle dans un navigateur

### Timeout lors du téléchargement du modèle
- Vercel a une limite de 10s pour les fonctions serverless (gratuit)
- Passez au plan Pro pour 60s, ou utilisez une autre plateforme

### Erreur de mémoire
- Les modèles YOLO sont gourmands en RAM
- Utilisez un modèle plus léger (nano ou small)
- Considérez une plateforme avec plus de RAM

## 🚀 Prochaines étapes

1. **Optimiser le modèle** : Utilisez ONNX ou TensorRT pour des inférences plus rapides
2. **Caching** : Mettre en cache les prédictions fréquentes
3. **Batch processing** : Supporter plusieurs images en une requête
4. **WebSocket** : Pour des mises à jour en temps réel
5. **CDN** : Héberger les résultats d'image annotées

## 📚 Ressources

- [Vercel Python Runtime](https://vercel.com/docs/functions/runtimes/python)
- [Ultralytics YOLO Docs](https://docs.ultralytics.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Hugging Face Hub](https://huggingface.co/docs/hub/index)

## 💡 Alternative : API locale pour développement

Si Vercel est trop complexe pour commencer, testez d'abord localement :

```bash
# Terminal 1 : Lancer l'API
cd api
python index.py

# Terminal 2 : Tester
curl -X POST http://localhost:5000/predict -F "image=@test.jpg"
```

Puis utilisez [ngrok](https://ngrok.com/) pour exposer temporairement :

```bash
ngrok http 5000
# Utilisez l'URL https fournie dans votre site
```
