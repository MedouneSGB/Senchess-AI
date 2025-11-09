# Senchess AI - Modèle de Détection de Pièces d'Échecs

Ce projet contient le code et les ressources pour entraîner un modèle de vision par ordinateur capable de détecter la position des pièces sur un échiquier à partir d'une image. Ce modèle est conçu pour être intégré à **Senchess.com**, une plateforme d'échecs en ligne avec des fonctionnalités d'IA avancées.

## 🎯 Modèles Disponibles

Nous avons entraîné **2 modèles de production** spécialisés :

| Modèle | mAP50 | Spécialité | Meilleur pour |
|--------|-------|------------|---------------|
| **🥇 Senchess Haki v1.0** | 99.5% | Diagrammes 2D générés | Images Chess Decoder, graphiques stylisés |
| **🥈 Senchess Gear v1.0** | 98.5% | Photos physiques 3D | Photos smartphone d'échiquiers réels |

## � API REST Déployable

**Nouveau !** Une API Flask complète pour déployer vos modèles sur Vercel et les utiliser dans vos applications web.

### Démarrage rapide

```bash
# 1. Uploader vos modèles sur Hugging Face
pip install huggingface_hub
python upload_models_to_huggingface.py

# 2. Déployer sur Vercel
npm i -g vercel
vercel --prod
```

### Utilisation

```typescript
// Dans votre application web
import { analyzeChessBoardImage } from './chessImageRecognition';

const result = await analyzeChessBoardImage(imageUrl);
console.log('FEN:', result.fen);  // Position en notation FEN
console.log('Pièces:', result.detectedPieces);  // Nombre de pièces détectées
```

**📚 Documentation complète :**
- [`QUICK_START.md`](QUICK_START.md) - Guide de déploiement express (5 étapes)
- [`HUGGINGFACE_GUIDE.md`](HUGGINGFACE_GUIDE.md) - Upload des modèles sur Hugging Face
- [`DEPLOYMENT.md`](DEPLOYMENT.md) - Guide de déploiement complet
- [`COMMANDS.md`](COMMANDS.md) - Toutes les commandes utiles
- [`api/README.md`](api/README.md) - Documentation de l'API

## �📋 Table des Matières

- [Modèles Disponibles](#-modèles-disponibles)
- [API REST Déployable](#-api-rest-déployable)
- [Structure du Projet](#structure-du-projet)
- [Technologies Utilisées](#technologies-utilisées)
- [Installation](#installation)
- [Utilisation Rapide](#utilisation-rapide)
- [Utilisation Avancée](#utilisation-avancée)
  - [1. Gestionnaire de Modèles](#1-gestionnaire-de-modèles)
  - [2. Entraînement](#2-entraînement)
  - [3. Prédiction](#3-prédiction)
  - [4. Évaluation](#4-évaluation)
- [Dataset](#dataset)
- [Résultats](#résultats)
- [Exemples](#exemples)

## 📁 Structure du Projet

```
Senchess AI/
├── data/                           # Données d'entraînement (1693 images total)
│   ├── processed/                  # Dataset Gear (693 images - photos 3D)
│   │   ├── train/                  # Ensemble d'entraînement (485 images)
│   │   ├── valid/                  # Ensemble de validation (58 images)
│   │   └── test/                   # Ensemble de test (150 images)
│   ├── chess_decoder_1000/         # Dataset Haki (1000 images - diagrammes 2D)
│   │   ├── images/
│   │   │   ├── train/              # 700 images
│   │   │   ├── val/                # 200 images
│   │   │   └── test/               # 100 images
│   │   └── labels/
│   └── chess_dataset.yaml          # Configuration dataset Gear
├── src/                            # Code source
│   ├── train.py                    # Script d'entraînement du modèle
│   ├── predict.py                  # Script d'inférence simple
│   ├── model_manager.py            # 🆕 Gestionnaire de modèles professionnel
│   ├── evaluate.py                 # 🆕 Évaluation et comparaison
│   ├── adapt_roboflow_dataset.py   # Détection automatique des couleurs
│   ├── merge_datasets.py           # Fusion de datasets YOLO
│   └── prepare_data.py             # Préparation des données
├── models/                         # Modèles entraînés
│   ├── senchess_haki_v1.0/         # 🥇 Meilleur modèle (99.5% mAP50)
│   │   └── weights/
│   │       └── best.pt             # 6.0MB - Diagrammes 2D
│   ├── senchess_gear_v1.0/         # 🥈 Second modèle (98.5% mAP50)
│   │   └── weights/
│   │       └── best.pt             # 6.0MB - Photos physiques
│   └── MODEL_CONFIG.yaml           # Configuration complète des modèles
├── predictions/                    # Résultats des prédictions
├── imgTest/                        # Images de test
├── requirements.txt                # Dépendances Python
├── .gitignore                      # Fichiers à ignorer
└── README.md                       # Ce fichier
```

## 🛠️ Technologies Utilisées

- **YOLOv8** (Ultralytics) - Architecture de détection d'objets state-of-the-art
- **PyTorch** - Framework de deep learning
- **OpenCV** - Traitement d'images
- **Python 3.9+** - Langage de programmation

## 💻 Installation

### Prérequis

- Python 3.9 à 3.11 (Python 3.13 n'est pas encore compatible avec PyTorch)
- pip

### Étapes d'installation

1. **Clonez le projet** (si applicable) :
   ```bash
   git clone <url-du-repo>
   cd "Senchess AI"
   ```

2. **Créez un environnement virtuel** :
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Sur macOS/Linux
   # .venv\Scripts\activate   # Sur Windows
   ```

3. **Installez les dépendances** :
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## 🚀 Utilisation Rapide

### Utiliser les Modèles Pré-Entraînés

```python
from src.model_manager import SenchessModelManager

# Initialiser le gestionnaire
manager = SenchessModelManager()

# Lister les modèles disponibles
manager.list_models()

# Charger et utiliser Haki (meilleur pour diagrammes 2D)
haki = manager.load_model('haki')
results = manager.predict('haki', 'votre_image.png')

# Charger et utiliser Gear (meilleur pour photos physiques)
gear = manager.load_model('gear')
results = manager.predict('gear', 'photo_echiquier.jpg')

# Comparer les 2 modèles sur la même image
comparison = manager.compare_models('test_image.jpg')
```

### En Ligne de Commande

```bash
# Lister les modèles disponibles
python src/model_manager.py --list

# Prédiction avec Haki
python src/model_manager.py --model haki --image imgTest/capture3.png

# Prédiction avec Gear
python src/model_manager.py --model gear --image imgTest/capture2.jpg

# Comparer les 2 modèles
python src/model_manager.py --compare --image imgTest/capture2.jpg
```

## 🔧 Utilisation Avancée

### 1. Gestionnaire de Modèles

Le `SenchessModelManager` offre une API complète :

```python
from src.model_manager import SenchessModelManager

manager = SenchessModelManager()

# Obtenir les informations d'un modèle
info = manager.get_model_info('haki')
print(f"mAP50: {info['metrics']['mAP50']}%")

# Recommandation automatique selon le cas d'usage
best_model = manager.recommend_model('user_photos')  # Retourne 'gear'
best_model = manager.recommend_model('generated_images')  # Retourne 'haki'
```

### 2. Entraînement

Entraînez un nouveau modèle YOLOv8 sur votre dataset :

```bash
# Entraînement de base (10 époques)
python src/train.py

# Entraînement standard (50 époques)
python src/train.py --epochs 50 --project models --name mon_nouveau_modele

# Entraînement approfondi (100 époques)
python src/train.py --epochs 100 --batch-size 8

# Fine-tuning d'un modèle existant
python src/train.py --model models/senchess_gear_v1.0/weights/best.pt --epochs 20
```

**Paramètres disponibles** :
- `--epochs` : Nombre d'époques (par défaut : 10)
- `--batch-size` : Taille du batch (par défaut : 8)
- `--img-size` : Taille des images (par défaut : 640)
- `--model` : Modèle de base (`yolov8n.pt` ou chemin vers .pt existant)
- `--project` : Dossier de sortie (par défaut : `models`)
- `--name` : Nom du modèle (par défaut : auto-généré)

Le modèle entraîné sera sauvegardé dans `models/<name>/weights/best.pt`.

### 3. Prédiction

Utilisez les modèles entraînés pour détecter les pièces :

```bash
# Prédiction simple avec le modèle par défaut
python src/predict.py --image-path imgTest/capture2.jpg

# Avec seuil de confiance personnalisé
python src/predict.py --image-path imgTest/capture2.jpg --conf 0.5

# Sans sauvegarder l'image annotée
python src/predict.py --image-path imgTest/capture2.jpg --no-save

# Utiliser un modèle spécifique
python src/predict.py --image-path imgTest/capture3.png --model models/senchess_haki_v1.0/weights/best.pt
```

Les résultats incluent :
- Une image annotée avec les boîtes englobantes (dans `predictions/`)
- Un fichier JSON avec les coordonnées et classes de chaque pièce détectée

### 4. Évaluation

Évaluez et comparez les performances des modèles :

```bash
# Évaluer un modèle sur l'ensemble de test
python src/evaluate.py --model haki

# Comparer les 2 modèles
python src/evaluate.py --compare

# Évaluation détaillée avec métriques par classe
python src/evaluate.py --model haki --detailed
```

## 📊 Dataset

Le projet utilise **2 datasets complémentaires** :

### Dataset 1 : Senchess Gear (693 images)
- **Type** : Photos d'échiquiers physiques 3D
- **Source** : Images personnelles
- **Répartition** : 485 train / 58 valid / 150 test
- **13 classes** avec distinction noir/blanc :
  - Pièces noires : black-bishop, black-king, black-knight, black-pawn, black-queen, black-rook
  - Pièces blanches : white-bishop, white-king, white-knight, white-pawn, white-queen, white-rook
  - Pièce générique : bishop (fou)

### Dataset 2 : Senchess Haki (1000 images)
- **Type** : Diagrammes d'échecs 2D générés par Chess Decoder
- **Source** : Chess Decoder dataset
- **Répartition** : 700 train / 200 val / 100 test
- **Mêmes 13 classes** avec distinction noir/blanc
- **Styles variés** : ocean, marble, wood, classic, sunset, forest, neon, gold-silver

Les annotations sont au format YOLO (fichiers `.txt` avec coordonnées normalisées).

## 📈 Résultats

### Performances des Modèles

| Modèle | Dataset | Images | mAP50 | mAP50-95 | Precision | Recall | Durée |
|--------|---------|--------|-------|----------|-----------|--------|-------|
| **Senchess Haki v1.0** | Chess Decoder (1000) | 1000 | **99.5%** | 85.3% | 98.2% | 97.8% | 2.24h |
| **Senchess Gear v1.0** | Photos (693) | 693 | **98.5%** | 71.2% | 95.8% | 94.3% | 11.7h |

### Spécialisations

- **Senchess Haki v1.0** 🥇
  - ✅ Excellent sur diagrammes 2D générés
  - ✅ Reconnaissance de styles variés (ocean, marble, wood, etc.)
  - ✅ Précision quasi-parfaite sur images Chess Decoder
  - ⚠️ Moins performant sur photos physiques réelles

- **Senchess Gear v1.0** 🥈
  - ✅ Excellent sur photos d'échiquiers physiques
  - ✅ Robuste aux variations d'éclairage
  - ✅ Performances optimales sur images smartphone
  - ⚠️ Moins performant sur diagrammes générés

### Recommandations d'Usage

```python
# Pour photos d'échiquiers réels (smartphone, appareil photo)
manager.predict('gear', 'photo_echiquier.jpg')

# Pour diagrammes générés (Chess Decoder, captures d'écran)
manager.predict('haki', 'diagramme.png')

# Pour usage hybride, comparez les 2
manager.compare_models('image_inconnue.jpg')
```

## 🖼️ Exemples

### Exemple 1 : Photo d'échiquier physique (Gear)

```python
from src.model_manager import SenchessModelManager

manager = SenchessModelManager()
results = manager.predict('gear', 'imgTest/capture2.jpg')
```

**Résultat** : 32 pièces détectées avec confiance moyenne de 94.3%

### Exemple 2 : Diagramme Chess Decoder (Haki)

```python
results = manager.predict('haki', 'imgTest/capture3.png')
```

**Résultat** : 32 pièces détectées avec confiance moyenne de 98.7%

### Exemple 3 : Comparaison des modèles

```python
comparison = manager.compare_models('imgTest/capture2.jpg')
print(f"Gear: {comparison['gear']['detections']} détections")
print(f"Haki: {comparison['haki']['detections']} détections")
```

## 🎯 Prochaines Étapes

- [ ] Créer Senchess Ultimate (fusion 1693 images pour modèle universel)
- [ ] Intégration avec l'API REST de Senchess.com
- [ ] Support de la détection en temps réel (vidéo)
- [ ] Tests unitaires et CI/CD
- [ ] Export du modèle pour déploiement mobile (ONNX, TFLite)
- [ ] Dashboard de monitoring en production

## 📝 Notes Techniques

### CPU vs GPU
- **Entraînement sur CPU** : Possible mais lent (1-2h par 10 époques sur 1000 images)
- **GPU recommandé** : NVIDIA avec CUDA pour accélération 10-20x
- **Alternative** : Google Colab avec GPU gratuit

### Taille des Modèles
- **YOLOv8n** (nano) : 6MB, 3M paramètres, le plus rapide
- **YOLOv8s** (small) : 22MB, 11M paramètres, meilleur compromis
- **YOLOv8m** (medium) : 52MB, 26M paramètres, haute précision

### Amélioration des Performances
- **Plus de données** : Variété d'échiquiers, angles, éclairages
- **Data augmentation** : Rotation, flip, changement luminosité
- **Fine-tuning** : Partir d'un modèle pré-entraîné
- **Ensemble** : Combiner plusieurs modèles

## 🤝 Contribution

Pour contribuer au projet :
1. Fork le repository
2. Créez une branche (`git checkout -b feature/amelioration`)
3. Commitez vos changements (`git commit -m 'Ajout fonctionnalité'`)
4. Push vers la branche (`git push origin feature/amelioration`)
5. Ouvrez une Pull Request

## � Documentation Complète

Pour plus de détails sur le projet :
- **[docs/SUMMARY.md](docs/SUMMARY.md)** - Résumé exécutif du projet
- **[docs/IMPROVEMENTS.md](docs/IMPROVEMENTS.md)** - Rapport des améliorations Court Terme
- **[docs/CHANGELOG.md](docs/CHANGELOG.md)** - Historique des versions
- **[docs/PROJECT_STATUS.txt](docs/PROJECT_STATUS.txt)** - Statut visuel du projet
- **[models/MODEL_CONFIG.yaml](models/MODEL_CONFIG.yaml)** - Configuration détaillée des modèles

## �📜 License

Ce projet est sous licence [MIT](LICENSE).

## 📧 Contact

Pour toute question concernant ce projet, veuillez contacter l'équipe Senchess.com.

---

**Modèles Actuels** : Senchess Haki v1.0 (99.5%) | Senchess Gear v1.0 (98.5%)

**Happy Chess Learning!** ♟️🤖🎯
