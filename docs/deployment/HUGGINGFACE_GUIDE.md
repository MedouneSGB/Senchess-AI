# 🚀 Guide Rapide : Upload des Modèles vers Hugging Face

Ce guide explique comment uploader vos modèles Haki et Gear sur Hugging Face pour les utiliser avec Vercel.

## 📋 Étapes

### 1. Créer un compte Hugging Face (gratuit)
- Allez sur https://huggingface.co/
- Créez un compte si vous n'en avez pas

### 2. Créer un token d'accès
- Allez sur https://huggingface.co/settings/tokens
- Cliquez sur "New token"
- Nom : `senchess-upload`
- Type : `Write` (accès en écriture)
- Copiez le token généré

### 3. Installer huggingface_hub
```bash
pip install huggingface_hub
```

### 4. Uploader les modèles
```bash
# Depuis le répertoire racine de votre projet
cd "/Users/macbookair/Desktop/Senchess AI"

# Lancer le script d'upload
python upload_models_to_huggingface.py
```

Le script va :
1. Vous demander de vous connecter (avec votre token)
2. Créer un repository `votre-username/senchess-models`
3. Uploader `gear_v1.1.pt` et `haki_v1.0.pt`
4. Créer un README automatiquement

### 5. Configurer Vercel
Une fois l'upload terminé, le script affichera :
```
HUGGINGFACE_REPO_ID=VotreUsername/senchess-models
```

Ajoutez cette variable dans :
- **Vercel Dashboard** : Settings → Environment Variables
- Ou dans `vercel.json` (déjà configuré)

### 6. Déployer sur Vercel
```bash
vercel --prod
```

## 🎯 Options du script

```bash
# Upload avec token directement (évite le login interactif)
python upload_models_to_huggingface.py --token hf_votre_token_ici

# Changer le nom du repository
python upload_models_to_huggingface.py --repo mon-projet-echecs

# Spécifier votre username
python upload_models_to_huggingface.py --username VotreUsername
```

## ✅ Vérification

Après l'upload, visitez :
```
https://huggingface.co/VotreUsername/senchess-models
```

Vous devriez voir :
- ✅ gear_v1.1.pt (votre modèle Gear)
- ✅ haki_v1.0.pt (votre modèle Haki)
- ✅ README.md (documentation)

## 🔧 Configuration de l'API

L'API supporte maintenant 3 modes :

### Mode Gear (détection globale)
```bash
# Variable d'environnement
MODEL_TYPE=gear
```

### Mode Haki (pièces stratégiques)
```bash
MODEL_TYPE=haki
```

### Mode Ensemble (meilleur des deux) ⭐️ Recommandé
```bash
MODEL_TYPE=ensemble
```

## 📞 Utilisation depuis votre site

```typescript
// Utiliser le mode ensemble
const formData = new FormData();
formData.append('image', imageBlob);
formData.append('model', 'ensemble'); // ou 'gear' ou 'haki'

const response = await fetch('https://votre-app.vercel.app/predict', {
  method: 'POST',
  body: formData
});
```

## ❓ Problèmes courants

### Erreur : "Token invalide"
- Vérifiez que le token a les permissions `Write`
- Recréez un nouveau token si nécessaire

### Erreur : "Repository exists"
- Normal ! Le script gère automatiquement les repos existants
- Les fichiers seront écrasés avec les nouvelles versions

### Upload lent
- Normal pour des fichiers YOLO (50-100MB)
- Peut prendre 5-10 minutes selon votre connexion

## 🔒 Sécurité

### Repository privé
Si vous voulez un repository privé (invisible publiquement) :

Modifiez `upload_models_to_huggingface.py` ligne ~70 :
```python
private=True  # Au lieu de False
```

Puis ajoutez un token Hugging Face dans Vercel :
```bash
# Dashboard Vercel → Environment Variables
HF_TOKEN=hf_votre_token_ici
```

## 📊 Après le déploiement

Testez votre API :
```bash
# Health check
curl https://votre-app.vercel.app/health

# Test de prédiction
curl -X POST https://votre-app.vercel.app/predict \
  -F "image=@imgTest/capture.jpg" \
  -F "model=ensemble"
```

## 🎉 C'est tout !

Vos modèles sont maintenant hébergés sur Hugging Face et votre API peut les télécharger automatiquement au démarrage sur Vercel.
