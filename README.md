# Senchess AI - Modèle de Détection de Pièces d'Échecs

Ce projet contient le code et les ressources pour entraîner un modèle de vision par ordinateur capable de détecter la position des pièces sur un échiquier à partir d'une image. Ce modèle est conçu pour être intégré à **Senchess.com**, une plateforme d'échecs en ligne avec des fonctionnalités d'IA avancées.

## 🎯 Modèles Disponibles

Nous avons entraîné **2 modèles de production** spécialisés :

| Modèle | mAP50 | Spécialité | Meilleur pour |
|--------|-------|------------|---------------|
| **🥇 Senchess Haki v1.0** | 99.5% | Diagrammes 2D générés | Images Chess Decoder, graphiques stylisés |
| **🥈 Senchess Gear v1.0** | 98.5% | Photos physiques 3D | Photos smartphone d'échiquiers réels |

## 📋 Table des Matières

- [Modèles Disponibles](#-modèles-disponibles)
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
│   ├── chess_dataset_1000/         # Dataset 13 classes (1000 images)
│   │   ├── images/train/val/test/  # Images organisées
│   │   └── labels/train/val/test/  # Annotations YOLO
│   ├── chess_decoder_1000/         # Dataset Haki (1000 images - diagrammes 2D)
│   │   ├── images/train/val/test/
│   │   └── labels/train/val/test/
│   └── chess_ultimate_1693/        # Dataset ultimate (combiné)
│       ├── train/images/labels/
│       ├── valid/images/labels/
│       └── test/images/labels/
├── scripts/                        # 🆕 Scripts organisés
│   ├── training/                   # Scripts d'entraînement
│   │   ├── train_intel.py          # ⭐ Production (optimisé CPU Intel)
│   │   ├── train_ultimate.py       # Entraînement ultimate dataset
│   │   ├── train_new_model.py      # Nouveau modèle 13 classes
│   │   └── ensemble_model.py       # Modèle ensemble
│   ├── inference/                  # Scripts d'inférence
│   │   ├── export_openvino.py      # Export vers OpenVINO
│   │   ├── benchmark_openvino_fixed.py  # 🚀 Benchmark GPU (6x speedup!)
│   │   ├── test_models.py          # Tests de validation
│   │   └── analyze_image.py        # Analyse d'images
│   ├── utils/                      # Utilitaires
│   │   ├── check_devices.py        # Vérifier devices OpenVINO
│   │   ├── check_gpu_intel.py      # Détecter GPU Intel
│   │   ├── compare_all_models.py   # Comparer modèles
│   │   └── view_results.py         # Visualiser résultats
│   └── experiments/                # 🧪 Code expérimental
│       ├── experiment_ipex.py      # Tests IPEX (échoué)
│       └── downgrade_pytorch.py    # Gestion versions PyTorch
├── src/                            # Code source original
│   ├── train.py                    # Script d'entraînement du modèle
│   ├── predict.py                  # Script d'inférence simple
│   ├── model_manager.py            # Gestionnaire de modèles professionnel
│   ├── evaluate.py                 # Évaluation et comparaison
│   └── ...                         # Autres utilitaires
├── models/                         # Modèles entraînés
│   ├── senchess_haki_v1.0/         # 🥇 Meilleur modèle (99.5% mAP50)
│   │   └── weights/best.pt         # 6.0MB - Diagrammes 2D
│   ├── senchess_gear_v1.0/         # 🥈 Second modèle (98.5% mAP50)
│   │   └── weights/best.pt         # 6.0MB - Photos physiques
│   ├── senchess_intel_v1.0_quick<N>/  # Modèles Intel CPU
│   │   └── weights/best.pt         # Entraînés avec train_intel.py
│   └── MODEL_CONFIG.yaml           # Configuration complète
├── docs/                           # Documentation
│   ├── OPENVINO_SUCCESS.md         # 🚀 Guide OpenVINO GPU (6x speedup)
│   ├── GPU_INTEL_CONCLUSION.md     # Leçons IPEX vs OpenVINO
│   └── ...                         # Autres docs
├── predictions/                    # Résultats des prédictions
├── requirements.txt                # Dépendances Python
└── README.md                       # Ce fichier
```

## 🛠️ Technologies Utilisées

- **YOLOv8** (Ultralytics) - Architecture de détection d'objets state-of-the-art
- **PyTorch 2.9** - Framework de deep learning
- **OpenVINO 2025.3** - Accélération GPU Intel (6x speedup!)
- **Intel MKL** - Optimisations CPU pour training
- **OpenCV** - Traitement d'images
- **Python 3.13** - Langage de programmation

### 🚀 Optimisations GPU Intel

Ce projet inclut maintenant un support complet pour **Intel Iris Xe Graphics** :

- ✅ **Training optimisé CPU** avec Intel MKL (`scripts/training/train_intel.py`)
- ✅ **Inference GPU accélérée** avec OpenVINO (6x plus rapide!)
- ✅ **Benchmarks complets** PyTorch vs OpenVINO CPU vs GPU
- ❌ **IPEX non recommandé** (setup complexe, drivers manquants)

**Performances Intel Iris Xe:**
- PyTorch CPU: 58ms/image (17 FPS)
- OpenVINO CPU: 26ms/image (39 FPS) - 2.26x speedup
- **OpenVINO GPU: 10ms/image (103 FPS) - 6x speedup!** 🚀

Voir `docs/OPENVINO_SUCCESS.md` pour le guide complet.

## 💻 Installation

### Prérequis

- Python 3.13+ (ou 3.9-3.12)
- pip
- Intel CPU (recommandé pour optimisations MKL)
- Intel Iris Xe ou GPU Intel (optionnel, pour accélération OpenVINO)

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

### 🚀 Nouveaux Scripts Organisés

```bash
# === TRAINING ===
# Entraînement rapide optimisé Intel CPU (10 epochs)
python scripts/training/train_intel.py --quick

# Entraînement complet (100 epochs)
python scripts/training/train_intel.py --full

# === INFERENCE ===
# Export modèle vers OpenVINO
python scripts/inference/export_openvino.py

# Benchmark performances (PyTorch vs OpenVINO CPU/GPU)
python scripts/inference/benchmark_openvino_fixed.py

# Test modèles
python scripts/inference/test_models.py

# === UTILS ===
# Vérifier devices OpenVINO disponibles
python scripts/utils/check_devices.py

# Comparer tous les modèles
python scripts/utils/compare_all_models.py

# Visualiser résultats training
python scripts/utils/view_results.py
```

### En Ligne de Commande (API originale)

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
- [ ] Support de la détection en temps réel (vidéo) avec OpenVINO GPU
- [x] ✅ Optimisations GPU Intel (OpenVINO 6x speedup)
- [x] ✅ Organisation du code en modules logiques
- [ ] Tests unitaires et CI/CD
- [ ] Export du modèle pour déploiement mobile (ONNX, TFLite)
- [ ] Dashboard de monitoring en production

## 📝 Notes Techniques

### CPU vs GPU

#### Training
- **CPU Intel avec MKL** : Production-ready (scripts/training/train_intel.py)
  - Epoch ~5 min sur 1000 images
  - 10 epochs ~45 min
  - 100 epochs ~7.5h
- **GPU NVIDIA avec CUDA** : Recommandé pour training (10-20x plus rapide)
- **Intel Iris Xe GPU** : Non recommandé pour training (trop faible)
- **Alternative gratuite** : Google Colab avec GPU

#### Inference
- **PyTorch CPU** : 58ms/image (17 FPS) - Baseline
- **OpenVINO CPU** : 26ms/image (39 FPS) - 2.26x speedup
- **OpenVINO GPU Intel Iris Xe** : 10ms/image (103 FPS) - **6x speedup!** ✅
- **PyTorch CUDA** : Très rapide si GPU NVIDIA disponible

### Technologies GPU Intel

| Solution | Training | Inference | Statut | Recommandation |
|----------|----------|-----------|--------|----------------|
| **OpenVINO** | ❌ Non | ✅ 6x speedup | ✅ Production | **Utilisez ceci!** |
| **IPEX** | ✅ Oui | ✅ Oui | ❌ Échoué | Évitez (drivers manquants) |
| **Intel MKL** | ✅ Oui | ✅ Oui | ✅ Production | Inclus dans PyTorch |

**Voir documentation complète:**
- `docs/OPENVINO_SUCCESS.md` - Guide OpenVINO GPU
- `docs/GPU_INTEL_CONCLUSION.md` - Pourquoi IPEX a échoué
- `scripts/README.md` - Organisation des scripts

### Taille des Modèles
- **YOLOv8n** (nano) : 6MB, 3M paramètres, le plus rapide
- **YOLOv8s** (small) : 22MB, 11M paramètres, meilleur compromis
- **YOLOv8m** (medium) : 52MB, 26M paramètres, haute précision

### Amélioration des Performances
- **Plus de données** : Variété d'échiquiers, angles, éclairages
- **Data augmentation** : Rotation, flip, changement luminosité
- **Fine-tuning** : Partir d'un modèle pré-entraîné
- **Ensemble** : Combiner plusieurs modèles
- **OpenVINO** : Export pour accélération GPU Intel

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
