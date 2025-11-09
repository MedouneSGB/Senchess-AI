# 🎯 DÉPLOIEMENT SENCHESS - GUIDE EXPRESS

## 📦 Ce qui a été configuré

✅ API Flask complète (`api/index.py`)
✅ Support de 3 modes : Gear, Haki, Ensemble
✅ Conversion automatique en FEN
✅ Configuration Vercel (`vercel.json`)
✅ Script d'upload vers Hugging Face

## 🚀 Déploiement en 5 étapes

### 1️⃣ Installer huggingface_hub
```bash
pip install huggingface_hub
```

### 2️⃣ Uploader vos modèles sur Hugging Face
```bash
cd "/Users/macbookair/Desktop/Senchess AI"
python upload_models_to_huggingface.py
```
- Suivez les instructions
- Copiez le `HUGGINGFACE_REPO_ID` affiché

### 3️⃣ Configurer Vercel
Éditez `vercel.json` et remplacez :
```json
"HUGGINGFACE_REPO_ID": "VotreUsername/senchess-models"
```

### 4️⃣ Déployer
```bash
npm i -g vercel    # Si pas déjà installé
vercel login
vercel --prod
```

### 5️⃣ Utiliser dans votre site
Copiez le code de `api/client-example.ts` dans votre projet :
```typescript
import { analyzeChessBoardImage } from './chessImageRecognition';

const result = await analyzeChessBoardImage(imageUrl);
console.log('FEN:', result.fen);
console.log('Pièces:', result.detectedPieces);
```

## 🎮 Modes disponibles

| Mode | Description | Quand l'utiliser |
|------|-------------|------------------|
| **ensemble** ⭐️ | Combine Gear + Haki | **RECOMMANDÉ** - Meilleure précision |
| **gear** | Détection globale | Toutes les pièces, rapide |
| **haki** | Pièces stratégiques | King, Queen, Rook, Bishop |

Choisir le mode :
```typescript
// Dans votre requête
formData.append('model', 'ensemble');
```

## 📝 Variables d'environnement

Dans le dashboard Vercel (Settings → Environment Variables) :

```bash
HUGGINGFACE_REPO_ID=VotreUsername/senchess-models
MODEL_TYPE=ensemble
USE_HUGGINGFACE=true
```

## 🧪 Tester localement

```bash
# Terminal 1 : Lancer l'API
cd api
pip install -r requirements.txt
python index.py

# Terminal 2 : Tester
python test_api.py
```

## 📊 Format de réponse

```json
{
  "success": true,
  "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
  "pieces": [...],
  "confidence": 0.89,
  "detectedPieces": 32,
  "model_used": "ensemble"
}
```

## ⚠️ Important

- ✅ Les modèles sont hébergés sur Hugging Face (gratuit)
- ✅ Vercel télécharge automatiquement au démarrage
- ✅ Pas besoin de git commit les fichiers `.pt`
- ⚠️ Premier démarrage peut prendre 30-60s (téléchargement)
- ⚠️ Vercel gratuit : 10s timeout (passe au Pro si nécessaire)

## 📚 Documentation complète

- `HUGGINGFACE_GUIDE.md` - Guide détaillé upload HF
- `DEPLOYMENT.md` - Guide complet déploiement
- `api/README.md` - Configuration API
- `api/client-example.ts` - Code client complet

## 🆘 Aide rapide

**Problème** : "Model not loaded"
→ Vérifiez `HUGGINGFACE_REPO_ID` dans Vercel

**Problème** : Timeout
→ Utilisez un seul modèle (`MODEL_TYPE=gear`)
→ Ou passez à Vercel Pro (60s timeout)

**Problème** : "Repository not found"
→ Vérifiez que l'upload HF s'est bien passé
→ Le repo doit être public ou fournir `HF_TOKEN`

## 🎉 C'est prêt !

Votre URL API sera :
```
https://votre-app.vercel.app/predict
```

Testez avec :
```bash
curl https://votre-app.vercel.app/health
```
