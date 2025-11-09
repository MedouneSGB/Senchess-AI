# 🎯 API Senchess - Détection de Pièces d'Échecs

API REST Flask pour détecter les pièces d'échecs avec YOLO et convertir en notation FEN.

## 🚀 Démarrage Rapide

### Local (développement)

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer l'API
python index.py

# L'API sera disponible sur http://localhost:5000
```

### Test

```bash
# Script Python
python test_api.py

# Ou avec curl
curl http://localhost:5000/health
```

## 📡 Endpoints

### `GET /`
Page d'accueil avec la liste des endpoints

### `GET /health`
Vérifier l'état de l'API et des modèles chargés

**Réponse:**
```json
{
  "status": "healthy",
  "model_type": "ensemble",
  "models_loaded": {
    "gear": true,
    "haki": true
  },
  "use_huggingface": true,
  "repo_id": "VotreUsername/senchess-models"
}
```

### `POST /predict`
Analyser une image d'échiquier

**Paramètres:**
- `image` (file) : Image à analyser
- `image_base64` (string) : Image encodée en base64
- `conf` (float, optionnel) : Seuil de confiance (défaut: 0.25)
- `model` (string, optionnel) : 'gear', 'haki' ou 'ensemble' (défaut: valeur de MODEL_TYPE)

**Réponse:**
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
  "model_used": "ensemble",
  "imageSize": {
    "width": 800,
    "height": 800
  },
  "warnings": []
}
```

## 🎮 Modes de Détection

| Mode | Description | Usage |
|------|-------------|-------|
| **ensemble** ⭐️ | Combine Gear + Haki | Meilleure précision - RECOMMANDÉ |
| **gear** | Modèle Gear v1.1 | Détection rapide de toutes les pièces |
| **haki** | Modèle Haki v1.0 | Pièces stratégiques (K, Q, R, B) |

## ⚙️ Configuration

Variables d'environnement :

```bash
# Repository Hugging Face contenant les modèles
HUGGINGFACE_REPO_ID=VotreUsername/senchess-models

# Type de modèle : 'gear', 'haki' ou 'ensemble'
MODEL_TYPE=ensemble

# Utiliser Hugging Face ou fichiers locaux
USE_HUGGINGFACE=true

# Token HF (optionnel, pour repos privés)
# HF_TOKEN=hf_your_token
```

## 📦 Structure

```
api/
├── index.py              # API Flask principale
├── requirements.txt      # Dépendances Python
├── test_api.py          # Script de test
├── client-example.ts    # Code client TypeScript
└── README.md            # Cette documentation
```

## 🔧 Fonctionnalités

- ✅ Détection multi-modèles (Gear, Haki, Ensemble)
- ✅ Conversion automatique en FEN
- ✅ Support images : upload, base64
- ✅ Téléchargement automatique depuis Hugging Face
- ✅ Calcul de confiance et avertissements
- ✅ CORS activé pour intégration web
- ✅ Gestion d'erreurs robuste

## 📱 Intégration Client

### JavaScript/TypeScript

Copiez `client-example.ts` dans votre projet :

```typescript
import { analyzeChessBoardImage } from './chessImageRecognition';

// Avec un fichier
const file = event.target.files[0];
const result = await analyzeChessBoardFile(file);

// Avec une URL
const result = await analyzeChessBoardImage(imageUrl);

console.log('FEN:', result.fen);
console.log('Pièces:', result.detectedPieces);
```

### Python

```python
import requests

# Upload d'image
with open('chess.jpg', 'rb') as f:
    response = requests.post(
        'https://votre-app.vercel.app/predict',
        files={'image': f},
        data={'conf': 0.25, 'model': 'ensemble'}
    )

result = response.json()
print(f"FEN: {result['fen']}")
```

### cURL

```bash
curl -X POST https://votre-app.vercel.app/predict \
  -F "image=@chess.jpg" \
  -F "conf=0.25" \
  -F "model=ensemble"
```

## 🐛 Dépannage

### "Model not loaded"
- Vérifiez `HUGGINGFACE_REPO_ID`
- Vérifiez que les modèles sont bien uploadés sur HF
- Pour repos privés, ajoutez `HF_TOKEN`

### Timeout sur Vercel
- Utilisez un seul modèle (`MODEL_TYPE=gear`)
- Passez à Vercel Pro (timeout 60s au lieu de 10s)
- Optimisez la taille des images envoyées

### "No module named 'huggingface_hub'"
- Vérifiez `requirements.txt`
- Redéployez sur Vercel

## � Documentation Complète

- `../QUICK_START.md` - Guide de déploiement express
- `../HUGGINGFACE_GUIDE.md` - Upload des modèles
- `../DEPLOYMENT.md` - Guide complet
- `../COMMANDS.md` - Toutes les commandes utiles

## 🎉 C'est prêt !

L'API est prête à être déployée sur Vercel et utilisée dans votre application web.
