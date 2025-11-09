# 🏗️ Architecture Senchess AI

## 📊 Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────┐
│                    SENCHESS AI SYSTEM                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────┐      ┌──────────────────┐      ┌──────────────┐
│   Site Web      │      │   API Vercel     │      │  Hugging Face│
│   Senchess.com  │─────▶│   Flask REST     │─────▶│    Models    │
│                 │      │                  │      │              │
│ - Upload image  │◀─────│ - /predict       │      │ - gear.pt    │
│ - Affiche FEN   │      │ - /health        │      │ - haki.pt    │
└─────────────────┘      └──────────────────┘      └──────────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │  YOLO Models    │
                         ├─────────────────┤
                         │ • Gear v1.1     │
                         │ • Haki v1.0     │
                         │ • Ensemble      │
                         └─────────────────┘
```

## 🎯 Flux de Détection

```
1. Image Upload
   ↓
2. API /predict
   ↓
3. YOLO Detection
   ├─ Gear (toutes pièces)
   ├─ Haki (pièces stratégiques)
   └─ Ensemble (combinaison intelligente)
   ↓
4. Conversion FEN
   ↓
5. Retour JSON
   {
     fen: "...",
     pieces: [...],
     confidence: 0.89
   }
```

## 📦 Structure des Fichiers

```
Senchess AI/
│
├── 🚀 API VERCEL
│   ├── api/
│   │   ├── index.py              # Flask API principale
│   │   ├── requirements.txt      # Dépendances
│   │   ├── test_api.py          # Tests
│   │   └── client-example.ts    # Code client
│   │
│   ├── vercel.json              # Config Vercel
│   └── .vercelignore            # Exclusions
│
├── 🤖 MODÈLES LOCAUX
│   ├── models/
│   │   ├── senchess_gear_v1.1/
│   │   │   └── weights/best.pt  # 98.5% mAP50
│   │   └── senchess_haki_v1.0/
│   │       └── weights/best.pt  # 99.5% mAP50
│   │
│   └── upload_models_to_huggingface.py  # Upload script
│
├── 📊 ENTRAÎNEMENT
│   ├── src/
│   │   ├── train.py             # Entraînement
│   │   ├── finetune.py          # Fine-tuning
│   │   ├── predict.py           # Prédictions
│   │   └── evaluate.py          # Évaluation
│   │
│   └── data/
│       └── chess_decoder_1000/  # Dataset
│
├── 📚 DOCUMENTATION
│   ├── QUICK_START.md           # Guide express (⭐️ COMMENCER ICI)
│   ├── HUGGINGFACE_GUIDE.md     # Upload HF
│   ├── DEPLOYMENT.md            # Déploiement complet
│   ├── COMMANDS.md              # Commandes utiles
│   └── ARCHITECTURE.md          # Ce fichier
│
└── 🧪 TESTS
    ├── test_api.sh              # Test bash
    ├── test_models.py           # Test modèles
    └── imgTest/                 # Images test
```

## 🔄 Cycle de Développement

```
┌──────────────────────────────────────────────────────────┐
│                   CYCLE COMPLET                          │
└──────────────────────────────────────────────────────────┘

1. ENTRAÎNEMENT LOCAL
   ├─ Préparer dataset (data/)
   ├─ Entraîner modèle (src/train.py)
   └─ Évaluer (src/evaluate.py)
        ↓
2. UPLOAD MODÈLES
   ├─ Créer compte Hugging Face
   ├─ python upload_models_to_huggingface.py
   └─ Vérifier sur https://huggingface.co/
        ↓
3. DÉVELOPPEMENT API
   ├─ Coder API (api/index.py)
   ├─ Tester local (python api/index.py)
   └─ Vérifier (./test_api.sh)
        ↓
4. DÉPLOIEMENT VERCEL
   ├─ Configurer (vercel.json)
   ├─ vercel --prod
   └─ Tester production
        ↓
5. INTÉGRATION WEB
   ├─ Copier client-example.ts
   ├─ Configurer VITE_SENCHESS_API_URL
   └─ Utiliser analyzeChessBoardImage()
```

## 🎮 Modes de Détection

```
┌─────────────────────────────────────────────────────────┐
│                    STRATÉGIES                            │
└─────────────────────────────────────────────────────────┘

MODE GEAR
├─ Modèle : gear_v1.1.pt
├─ Classes : Toutes (12 classes)
├─ Vitesse : Rapide (~2s)
└─ Usage : Détection complète rapide

MODE HAKI
├─ Modèle : haki_v1.0.pt
├─ Classes : K, Q, R, B (8 classes)
├─ Précision : Très haute (99.5%)
└─ Usage : Pièces importantes uniquement

MODE ENSEMBLE ⭐️ (RECOMMANDÉ)
├─ Modèles : gear + haki
├─ Stratégie : 
│   1. Haki pour K, Q, R, B (haute précision)
│   2. Gear pour les autres pièces
│   3. Fusion intelligente (NMS)
├─ Vitesse : Moyenne (~4s)
└─ Usage : Meilleure précision globale
```

## 🌐 Déploiement

```
┌─────────────────────────────────────────────────────────┐
│               ENVIRONNEMENTS                             │
└─────────────────────────────────────────────────────────┘

DÉVELOPPEMENT LOCAL
├─ USE_HUGGINGFACE=false
├─ Modèles locaux (models/*.pt)
├─ Flask dev server (port 5000)
└─ Tests : python api/test_api.py

PRODUCTION VERCEL
├─ USE_HUGGINGFACE=true
├─ Télécharge depuis HF au démarrage
├─ Serverless functions
└─ URL : https://votre-app.vercel.app
```

## 📡 API Endpoints

```
GET /
├─ Retour : Info API
└─ Usage : Documentation

GET /health
├─ Retour : {status, models_loaded, ...}
└─ Usage : Monitoring

POST /predict
├─ Input : image (file/base64)
│         conf (float, 0-1)
│         model ('gear'|'haki'|'ensemble')
│
├─ Process : 
│   1. Charger image
│   2. Prédiction YOLO
│   3. Conversion FEN
│   4. Calcul confiance
│
└─ Output : {
      fen: "...",
      pieces: [...],
      confidence: 0.89,
      detectedPieces: 32,
      model_used: "ensemble",
      warnings: [...]
    }
```

## 🔐 Variables d'Environnement

```
┌──────────────────────────────────────────────────┐
│            CONFIGURATION                         │
└──────────────────────────────────────────────────┘

HUGGINGFACE_REPO_ID
├─ Format : "username/repo-name"
├─ Exemple : "MedouneSGB/senchess-models"
└─ Requis pour : Télécharger les modèles

MODEL_TYPE
├─ Valeurs : "gear" | "haki" | "ensemble"
├─ Défaut : "ensemble"
└─ Usage : Choisir la stratégie de détection

USE_HUGGINGFACE
├─ Valeurs : "true" | "false"
├─ true → Télécharge depuis HF
└─ false → Utilise fichiers locaux

HF_TOKEN (optionnel)
├─ Format : "hf_xxxxxxxxxxxx"
└─ Requis pour : Repos privés
```

## 📈 Performance

```
┌─────────────────────────────────────────────────┐
│              MÉTRIQUES                          │
└─────────────────────────────────────────────────┘

Gear v1.1
├─ mAP50 : 98.5%
├─ Précision : 97.8%
├─ Recall : 96.9%
└─ Vitesse : ~2s/image

Haki v1.0
├─ mAP50 : 99.5%
├─ Précision : 99.2%
├─ Recall : 99.0%
└─ Vitesse : ~1.5s/image

Ensemble
├─ mAP50 : ~99.0% (estimé)
├─ Détections : Meilleure couverture
├─ Confiance : Plus stable
└─ Vitesse : ~4s/image
```

## 🚦 Workflow Complet

```
Utilisateur                API Vercel              Hugging Face
    │                         │                         │
    │──── Upload Image ──────▶│                         │
    │                         │                         │
    │                         │──── Download Models ───▶│
    │                         │◀─── Models (.pt) ───────│
    │                         │                         │
    │                         │ [Load YOLO Models]     │
    │                         │ [Run Inference]        │
    │                         │ [Convert to FEN]       │
    │                         │                         │
    │◀─── JSON Response ──────│                         │
    │   {fen, pieces, ...}    │                         │
    │                         │                         │
    │──── Display Board ──────│                         │
```

## 🎯 Prochaines Étapes

1. ✅ Upload modèles sur Hugging Face
2. ✅ Configurer Vercel
3. ✅ Déployer API
4. 🔄 Intégrer dans Senchess.com
5. 📊 Collecter métriques production
6. 🚀 Optimiser performances
7. 🔧 Fine-tuning continu

## 📚 Ressources

- Code : https://github.com/MedouneSGB/Senchess-AI
- Modèles : https://huggingface.co/VotreUsername/senchess-models
- API : https://votre-app.vercel.app
- Site : https://senchess.com

---

**Commencez ici : [`QUICK_START.md`](QUICK_START.md)** 🚀
