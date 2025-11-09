# 🎯 COMMANDES RAPIDES - SENCHESS API

## 📤 Upload des modèles vers Hugging Face

```bash
# Installation
pip install huggingface_hub

# Upload (suivez les instructions interactives)
python upload_models_to_huggingface.py

# Ou avec token direct
python upload_models_to_huggingface.py --token hf_votre_token

# Avec nom de repo personnalisé
python upload_models_to_huggingface.py --repo mon-projet --username VotreUsername
```

## 🧪 Test en local

```bash
# Terminal 1 : Lancer l'API
cd api
pip install -r requirements.txt
export USE_HUGGINGFACE=false  # Utiliser fichiers locaux
python index.py

# Terminal 2 : Tester avec script Python
python api/test_api.py

# Ou avec script bash
./test_api.sh

# Ou avec curl
curl http://localhost:5000/health
curl -X POST http://localhost:5000/predict \
  -F "image=@imgTest/capture.jpg" \
  -F "model=ensemble"
```

## 🚀 Déploiement Vercel

```bash
# Installation Vercel CLI (si nécessaire)
npm install -g vercel

# Login
vercel login

# Déployer en preview
vercel

# Déployer en production
vercel --prod

# Voir les logs
vercel logs

# Variables d'environnement
vercel env add HUGGINGFACE_REPO_ID production
# Entrez: VotreUsername/senchess-models
```

## 🔧 Configuration

```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer les variables
nano .env  # ou votre éditeur préféré

# Variables importantes :
# - HUGGINGFACE_REPO_ID=VotreUsername/senchess-models
# - MODEL_TYPE=ensemble  (ou 'gear' ou 'haki')
# - USE_HUGGINGFACE=true
```

## 📊 Monitoring

```bash
# Logs en temps réel (Vercel)
vercel logs --follow

# Status de l'API
curl https://votre-app.vercel.app/health

# Test de prédiction
curl -X POST https://votre-app.vercel.app/predict \
  -F "image=@imgTest/capture.jpg" \
  -F "conf=0.25" \
  -F "model=ensemble"
```

## 🐛 Dépannage

```bash
# Vérifier les packages Python
pip list | grep -E "ultralytics|flask|huggingface"

# Tester le téléchargement HF manuellement
python -c "
from huggingface_hub import hf_hub_download
path = hf_hub_download(
    repo_id='VotreUsername/senchess-models',
    filename='gear_v1.1.pt'
)
print(f'Téléchargé: {path}')
"

# Vérifier les modèles locaux
ls -lh models/senchess_gear_v1.1/weights/best.pt
ls -lh models/senchess_haki_v1.0/weights/best.pt

# Tester YOLO localement
python -c "
from ultralytics import YOLO
model = YOLO('models/senchess_gear_v1.1/weights/best.pt')
print('Modèle chargé avec succès')
print(f'Classes: {model.names}')
"
```

## 🔄 Mise à jour

```bash
# Mettre à jour les modèles sur HF
python upload_models_to_huggingface.py

# Redéployer sur Vercel
vercel --prod

# Ou forcer un nouveau déploiement
vercel --force --prod
```

## 🧹 Nettoyage

```bash
# Supprimer les caches locaux
rm -rf /tmp/models
rm -rf ~/.cache/huggingface

# Supprimer le déploiement Vercel
vercel remove votre-projet-name
```

## 📝 Git

```bash
# Ne pas commiter les modèles (déjà dans .gitignore)
git status

# Commiter les changements de l'API
git add api/ vercel.json .vercelignore
git commit -m "feat: API Vercel avec support Hugging Face"
git push

# Vérifier .gitignore
cat .gitignore | grep -E "\.pt|models/"
```

## 🌐 URLs utiles

- Dashboard Vercel : https://vercel.com/dashboard
- Hugging Face : https://huggingface.co/
- Tokens HF : https://huggingface.co/settings/tokens
- Votre repo HF : https://huggingface.co/VotreUsername/senchess-models
- Votre API : https://votre-app.vercel.app

## 💡 Astuces

```bash
# Tester avec différents seuils de confiance
for conf in 0.15 0.25 0.35; do
  echo "Test avec conf=$conf"
  curl -X POST http://localhost:5000/predict \
    -F "image=@imgTest/capture.jpg" \
    -F "conf=$conf" | jq '.detectedPieces'
done

# Tester les 3 modes
for model in gear haki ensemble; do
  echo "Test avec model=$model"
  curl -X POST http://localhost:5000/predict \
    -F "image=@imgTest/capture.jpg" \
    -F "model=$model" | jq '.model_used, .detectedPieces'
done

# Benchmark de vitesse
time curl -X POST http://localhost:5000/predict \
  -F "image=@imgTest/capture.jpg" \
  -F "model=ensemble" > /dev/null
```
