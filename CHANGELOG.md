# 📜 Changelog - Senchess AI

Toutes les modifications notables du projet sont documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.0.0] - 2024-12-XX

### 🎉 Version Initiale - Production Ready

#### ✨ Added (Ajouts)
- **Modèles de Production**
  - Senchess Haki v1.0 (99.5% mAP50) - Spécialisé diagrammes 2D
  - Senchess Gear v1.0 (98.5% mAP50) - Spécialisé photos 3D physiques
  
- **Scripts Principaux**
  - `src/train.py` - Entraînement YOLOv8n
  - `src/predict.py` - Prédiction sur images
  - `src/model_manager.py` - Gestionnaire de modèles professionnel
  - `src/evaluate.py` - Évaluation et comparaison des modèles ⭐ NEW
  - `src/prepare_data.py` - Préparation des datasets
  - `src/adapt_roboflow_dataset.py` - Adaptation dataset Roboflow
  - `src/merge_datasets.py` - Fusion de datasets

- **Exemples Pratiques** ⭐ NEW
  - `examples/quick_start.py` - 7 exemples interactifs
  - Détection simple, batch, benchmark, comparaison
  - Prototype extraction FEN

- **Documentation**
  - README.md complet avec tableau comparatif ⭐ UPDATED
  - MODEL_CONFIG.yaml avec 6 modèles documentés
  - IMPROVEMENTS.md - Suivi des améliorations ⭐ NEW
  - CHANGELOG.md - Historique des versions ⭐ NEW

- **Datasets**
  - Chess Decoder 1000 (Haki) - 1000 images de diagrammes 2D
  - Chess Dataset 693 (Gear) - 693 photos d'échiquiers physiques
  - Total : 1693 images annotées

#### 🔧 Changed (Modifications)
- **README.md** - Refonte complète
  - Ajout tableau comparatif des modèles
  - Structure mise à jour (1693 images, 2 datasets)
  - Guide Quick Start avec SenchessModelManager
  - 3 exemples pratiques de code
  - Section évaluation détaillée
  - Notes techniques CPU/GPU

- **MODEL_CONFIG.yaml** - Corrections
  - Haki : "2D Chess Diagrams - Generated" (au lieu de "3D Rendered")
  - Gear : "3D Physical Chess Pieces - Photos" (confirmé)

- **Structure du Projet**
  - Création de `models/pretrained/` pour modèles de base
  - Organisation de `examples/` pour les exemples
  - Déplacement de `yolov8n.pt` vers `models/pretrained/`

#### 📊 Performance
- **Senchess Haki v1.0**
  - mAP50: 99.5%
  - mAP50-95: 85.3%
  - Precision: 98.2%
  - Recall: 97.8%
  - Entraînement: 10 epochs, 2.24h (CPU)

- **Senchess Gear v1.0**
  - mAP50: 98.5%
  - mAP50-95: 82.1%
  - Precision: 97.5%
  - Recall: 96.8%
  - Entraînement: 100 epochs, 6h43m (CPU)

#### 🎯 Specializations
- **Haki** : Diagrammes 2D (Chess Decoder style)
  - Thèmes ocean/marble/wood
  - Fond coloré avec symboles stylisés
  - Optimal pour contenus générés/digitaux

- **Gear** : Photos 3D physiques
  - Échiquiers réels
  - Éclairage variable
  - Optimal pour captures smartphone

#### 🏗️ Infrastructure
- Python 3.9.6
- YOLOv8n (3M paramètres, 8.2 GFLOPs)
- PyTorch 2.2.2 (CPU)
- Ultralytics 8.3.225
- Environnement virtuel .venv (1.3GB)

---

## [0.5.0] - 2024-XX-XX (Développement)

### Travaux Préliminaires

#### Added
- Scripts de base pour entraînement
- Préparation des datasets Roboflow
- Structure initiale du projet
- Premiers tests avec YOLOv8n

#### Changed
- Expérimentation avec différents hyperparamètres
- Tests de différents datasets
- Itérations sur l'architecture

---

## 🗺️ Roadmap Future

### [1.1.0] - Moyen Terme (1-2 semaines)

#### Planned
- [ ] Tests automatisés (pytest)
  - `tests/test_models.py`
  - `tests/test_predict.py`
  - `tests/test_evaluate.py`
  - Coverage > 80%

- [ ] Dashboard Streamlit
  - Interface web interactive
  - Visualisation des métriques
  - Comparaison en temps réel
  - Upload d'images

- [ ] API REST (FastAPI)
  - Endpoint `/predict`
  - Endpoint `/compare`
  - Documentation Swagger
  - Déploiement Docker

- [ ] Amélioration Continue
  - Fine-tuning des hyperparamètres
  - Augmentation de données
  - Optimisation vitesse d'inférence

### [2.0.0] - Long Terme (1-2 mois)

#### Planned
- [ ] Senchess Ultimate (modèle unifié)
  - Fusion Haki + Gear
  - Dataset combiné (1693+ images)
  - mAP50 > 99.7%
  - Polyvalent 2D + 3D

- [ ] Support GPU
  - Accélération CUDA
  - Inférence < 50ms
  - Batch processing optimisé

- [ ] Extraction FEN Complète
  - Calibration pixel → cases
  - Mapping 8x8
  - Notation algébrique
  - Validation positions légales

- [ ] Déploiement Mobile
  - Export ONNX
  - iOS (CoreML)
  - Android (TensorFlow Lite)
  - < 10MB par modèle

- [ ] Dataset v2
  - 5000+ images
  - Plus de variations
  - Éclairages extrêmes
  - Angles variés

---

## 🏷️ Format des Versions

Ce projet suit [Semantic Versioning](https://semver.org/):

```
MAJOR.MINOR.PATCH

MAJOR : Changements incompatibles (breaking changes)
MINOR : Nouvelles fonctionnalités (rétrocompatible)
PATCH : Corrections de bugs
```

### Exemples
- `1.0.0` → Version production initiale
- `1.1.0` → Ajout dashboard + API
- `1.1.1` → Fix bug prédiction
- `2.0.0` → Nouveau modèle Ultimate (breaking)

---

## 📝 Types de Changements

- **Added** : Nouvelles fonctionnalités
- **Changed** : Modifications de fonctionnalités existantes
- **Deprecated** : Fonctionnalités obsolètes (bientôt supprimées)
- **Removed** : Fonctionnalités supprimées
- **Fixed** : Corrections de bugs
- **Security** : Corrections de sécurité

---

**🔗 Liens Utiles**
- [README.md](README.md) - Documentation principale
- [MODEL_CONFIG.yaml](models/MODEL_CONFIG.yaml) - Configuration des modèles
- [IMPROVEMENTS.md](IMPROVEMENTS.md) - Améliorations récentes

---

*Dernière mise à jour : 2024*
