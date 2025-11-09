# ✅ CHECKLIST - Déploiement Senchess API

## 📋 Avant de Commencer

- [ ] Compte Hugging Face créé (https://huggingface.co/)
- [ ] Compte Vercel créé (https://vercel.com/)
- [ ] Node.js installé (pour Vercel CLI)
- [ ] Python 3.9+ installé
- [ ] Git configuré

## 🚀 Étape 1 : Upload des Modèles (15 min)

- [ ] Installer huggingface_hub
  ```bash
  pip install huggingface_hub
  ```

- [ ] Créer un token sur Hugging Face
  - URL : https://huggingface.co/settings/tokens
  - Type : Write access
  - Nom : senchess-upload

- [ ] Uploader les modèles
  ```bash
  python upload_models_to_huggingface.py
  ```

- [ ] Vérifier que les modèles sont uploadés
  - [ ] Visiter : https://huggingface.co/VotreUsername/senchess-models
  - [ ] Voir : gear_v1.1.pt
  - [ ] Voir : haki_v1.0.pt

- [ ] Noter votre HUGGINGFACE_REPO_ID : __________________________

## 🧪 Étape 2 : Test Local (10 min)

- [ ] Installer les dépendances
  ```bash
  cd api
  pip install -r requirements.txt
  ```

- [ ] Créer fichier .env
  ```bash
  cp ../.env.example .env
  ```

- [ ] Éditer .env
  - [ ] USE_HUGGINGFACE=false (pour test local)
  - [ ] HUGGINGFACE_REPO_ID=VotreUsername/senchess-models

- [ ] Lancer l'API
  ```bash
  python index.py
  ```

- [ ] Dans un autre terminal, tester
  ```bash
  python test_api.py
  # ou
  ./test_api.sh
  ```

- [ ] Vérifier les résultats
  - [ ] Health check OK
  - [ ] Prédiction réussie
  - [ ] FEN généré

## 📦 Étape 3 : Configuration Vercel (5 min)

- [ ] Éditer vercel.json
  ```json
  {
    "env": {
      "HUGGINGFACE_REPO_ID": "VotreUsername/senchess-models",
      "MODEL_TYPE": "ensemble",
      "USE_HUGGINGFACE": "true"
    }
  }
  ```

- [ ] Vérifier que les fichiers sont prêts
  - [ ] api/index.py existe
  - [ ] api/requirements.txt existe
  - [ ] vercel.json configuré
  - [ ] .vercelignore présent

## 🌐 Étape 4 : Déploiement Vercel (10 min)

- [ ] Installer Vercel CLI
  ```bash
  npm install -g vercel
  ```

- [ ] Se connecter
  ```bash
  vercel login
  ```

- [ ] Déployer en preview (test)
  ```bash
  vercel
  ```

- [ ] Tester l'URL de preview
  - [ ] Ouvrir l'URL donnée par Vercel
  - [ ] Tester : https://votre-app-xxx.vercel.app/health
  - [ ] Vérifier que les modèles se chargent

- [ ] Si OK, déployer en production
  ```bash
  vercel --prod
  ```

- [ ] Noter votre URL de production : __________________________

## 🎯 Étape 5 : Test Production (5 min)

- [ ] Tester le health check
  ```bash
  curl https://votre-app.vercel.app/health
  ```

- [ ] Tester une prédiction
  ```bash
  curl -X POST https://votre-app.vercel.app/predict \
    -F "image=@imgTest/capture.jpg" \
    -F "model=ensemble"
  ```

- [ ] Vérifier la réponse
  - [ ] FEN présent
  - [ ] Pièces détectées
  - [ ] Confiance > 0.7

## 💻 Étape 6 : Intégration Site Web (15 min)

- [ ] Copier le code client
  - [ ] Copier api/client-example.ts dans votre projet
  - [ ] Renommer en chessImageRecognition.ts

- [ ] Configurer les variables d'environnement
  ```bash
  # Dans votre projet web (.env)
  VITE_SENCHESS_API_URL=https://votre-app.vercel.app
  ```

- [ ] Importer et utiliser
  ```typescript
  import { analyzeChessBoardImage } from './services/chessImageRecognition';
  
  const result = await analyzeChessBoardImage(imageUrl);
  console.log('FEN:', result.fen);
  ```

- [ ] Tester dans votre application
  - [ ] Upload une image
  - [ ] Voir le FEN s'afficher
  - [ ] Vérifier les pièces détectées

## ✅ Vérification Finale

- [ ] ✅ Modèles uploadés sur Hugging Face
- [ ] ✅ API déployée sur Vercel
- [ ] ✅ Tests passent en production
- [ ] ✅ Intégration dans le site web
- [ ] ✅ FEN généré correctement

## 📊 Métriques à Surveiller

Premier mois :
- [ ] Nombre de requêtes/jour : ________
- [ ] Temps de réponse moyen : ________s
- [ ] Taux de succès : ________%
- [ ] Confiance moyenne : ________

## 🐛 En Cas de Problème

### "Model not loaded"
- [ ] Vérifier HUGGINGFACE_REPO_ID dans Vercel Dashboard
- [ ] Vérifier que les modèles sont publics sur HF
- [ ] Voir les logs : `vercel logs`

### Timeout
- [ ] Passer à MODEL_TYPE=gear (plus rapide)
- [ ] Passer à Vercel Pro (60s timeout)
- [ ] Optimiser taille des images

### "Repository not found"
- [ ] Vérifier le nom du repo sur HF
- [ ] Vérifier que le repo est public
- [ ] Sinon, ajouter HF_TOKEN dans Vercel

## 📚 Ressources

- [ ] Documentation lue : QUICK_START.md
- [ ] Guide HF consulté : HUGGINGFACE_GUIDE.md
- [ ] Commandes disponibles : COMMANDS.md
- [ ] Architecture comprise : ARCHITECTURE.md

## 🎉 Félicitations !

Votre API Senchess est maintenant déployée et fonctionnelle !

**URL API** : ________________________________

**Date déploiement** : ____/____/2025

**Prochaines étapes** :
1. Monitorer les performances
2. Collecter feedback utilisateurs
3. Optimiser si nécessaire
4. Fine-tuner les modèles avec nouvelles données

---

**Besoin d'aide ?**
- GitHub Issues : https://github.com/MedouneSGB/Senchess-AI/issues
- Documentation : Voir fichiers .md du projet
