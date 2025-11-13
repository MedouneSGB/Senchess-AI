# 🎯 Scripts Kaggle pour Senchess AI

Scripts pour entraîner vos modèles YOLO sur Kaggle avec GPU gratuit.

## 📁 Fichiers

### 1. `setup_kaggle.sh` - Configuration Automatique
Script bash pour installer et configurer Kaggle CLI.

**Usage:**
```bash
./kaggle_scripts/setup_kaggle.sh
```

**Ce qu'il fait:**
- ✅ Installe Kaggle CLI (`pip install kaggle`)
- ✅ Configure le dossier `~/.kaggle/`
- ✅ Copie et sécurise `kaggle.json`
- ✅ Teste la connexion

---

### 2. `prepare_dataset.py` - Préparation du Dataset
Script Python pour préparer votre dataset au format Kaggle.

**Usage:**
```bash
python kaggle_scripts/prepare_dataset.py
```

**Ce qu'il fait:**
- ✅ Copie les images et labels depuis `data/processed/`
- ✅ Crée le fichier `data.yaml` pour YOLO
- ✅ Génère les métadonnées Kaggle
- ✅ Crée un README pour le dataset
- ✅ Organise tout dans `kaggle_dataset/`

**Sortie:**
```
kaggle_dataset/
├── data.yaml              # Config YOLO
├── dataset-metadata.json  # Métadonnées Kaggle
├── README.md             # Documentation
├── train/
│   ├── images/
│   └── labels/
├── valid/
│   ├── images/
│   └── labels/
└── test/
    ├── images/
    └── labels/
```

---

### 3. `training_notebook.ipynb` - Notebook d'Entraînement
Notebook Jupyter complet pour Kaggle avec toutes les cellules prêtes.

**Contenu:**
- 📦 Installation des dépendances (Ultralytics)
- 🔍 Vérification du dataset
- 🚀 Entraînement YOLOv8
- 📊 Visualisation des résultats
- 🧪 Test du modèle
- 💾 Sauvegarde des fichiers
- 🤗 Upload vers Hugging Face (optionnel)

**Usage:**
1. Créer un nouveau notebook sur [Kaggle](https://www.kaggle.com/code)
2. Activer le GPU (Settings → Accelerator → GPU T4)
3. Copier-coller le contenu du notebook
4. Ajouter votre dataset
5. Run All

---

## 🚀 Guide Rapide - Démarrage

### Étape 1: Configuration
```bash
# Installer et configurer Kaggle
./kaggle_scripts/setup_kaggle.sh
```

### Étape 2: Préparation du Dataset
```bash
# Préparer le dataset
python kaggle_scripts/prepare_dataset.py

# Le dataset est maintenant dans kaggle_dataset/
```

### Étape 3: Upload du Dataset

**Option A: Interface Web (Recommandé)**
1. Allez sur https://www.kaggle.com/datasets
2. Cliquez sur "New Dataset"
3. Uploadez le contenu de `kaggle_dataset/`
4. Notez le nom: `votre-username/senchess-dataset`

**Option B: CLI**
```bash
cd kaggle_dataset
kaggle datasets create -p .
```

### Étape 4: Entraînement

**Option A: Interface Web (Plus Simple)**
1. Allez sur https://www.kaggle.com/code
2. New Notebook → GPU T4
3. Add Data → Votre dataset
4. Copier le code de `training_notebook.ipynb`
5. Run All

**Option B: Push du Notebook**
```bash
# Créer kernel-metadata.json
cat > kaggle_scripts/kernel-metadata.json << EOF
{
  "id": "votre-username/senchess-training",
  "title": "Senchess AI Training",
  "code_file": "training_notebook.ipynb",
  "language": "python",
  "kernel_type": "notebook",
  "is_private": true,
  "enable_gpu": true,
  "enable_internet": true,
  "dataset_sources": ["votre-username/senchess-dataset"],
  "competition_sources": [],
  "kernel_sources": []
}
EOF

# Push le notebook
kaggle kernels push -p kaggle_scripts/
```

---

## 📊 Paramètres d'Entraînement

Le notebook est configuré avec les meilleurs paramètres :

```python
results = model.train(
    data='/kaggle/input/senchess-dataset/data.yaml',
    epochs=100,          # Nombre d'epochs
    imgsz=640,          # Taille des images
    batch=16,           # Batch size
    optimizer='AdamW',  # Optimiseur
    lr0=0.001,         # Learning rate
    patience=20,        # Early stopping
    device=0,          # GPU
    amp=True,          # Mixed precision
    plots=True         # Générer graphiques
)
```

**Ajustements selon GPU:**
- GPU T4 (16GB): `batch=16`
- GPU P100 (16GB): `batch=32`
- TPU v3-8: `batch=64`

---

## 📥 Récupérer les Modèles

### Méthode 1: Téléchargement Direct
Les modèles sont dans `/kaggle/working/output/`:
- `senchess_best.pt` - Meilleur modèle
- `senchess_last.pt` - Dernier checkpoint
- `results.csv` - Métriques
- `results.png` - Graphiques
- `confusion_matrix.png` - Matrice de confusion

### Méthode 2: Upload Automatique vers Hugging Face
Le notebook inclut une cellule pour uploader automatiquement vers HF:
```python
api.upload_file(
    path_or_fileobj="best.pt",
    path_in_repo="senchess_kaggle_v1.pt",
    repo_id="MedouneSGB/senchess-models",
    token="votre_token"
)
```

---

## ⏱️ Temps d'Entraînement Estimé

| Configuration | Epochs | Temps |
|--------------|--------|-------|
| GPU T4 | 100 | ~2-3h |
| GPU P100 | 100 | ~1.5-2h |
| TPU v3-8 | 100 | ~1-1.5h |

---

## 🔧 Troubleshooting

### Erreur "403 Forbidden"
```bash
# Vérifier les credentials
cat ~/.kaggle/kaggle.json

# Vérifier les permissions
ls -la ~/.kaggle/kaggle.json
# Doit afficher: -rw------- (600)
```

### Erreur "Phone verification required"
1. Allez sur https://www.kaggle.com/settings/account
2. Ajoutez et vérifiez votre numéro de téléphone
3. Requis pour utiliser les GPUs gratuits

### "Out of Memory" pendant l'entraînement
Réduire le batch size dans le notebook:
```python
batch=8  # au lieu de 16
```

### Dataset non trouvé
Vérifier que le dataset est bien ajouté au notebook:
- Click sur "Add Data" (panneau droit)
- Chercher "senchess-dataset"
- Cliquer sur "Add"

---

## 📈 Monitoring

### Voir les Logs en Direct
Si vous utilisez la CLI:
```bash
# Voir le status
kaggle kernels status votre-username/senchess-training

# Voir les logs
kaggle kernels output votre-username/senchess-training -v
```

### Metrics dans le Notebook
Le notebook affiche automatiquement:
- mAP50, mAP50-95
- Precision, Recall
- Loss curves
- Confusion matrix
- Exemples de prédictions

---

## 🎯 Après l'Entraînement

1. **Télécharger les modèles** depuis `/kaggle/working/output/`

2. **Tester en local**:
```bash
# Copier le modèle dans models/
cp senchess_best.pt models/senchess_kaggle_v1/weights/best.pt

# Tester
python test_models.py
```

3. **Comparer avec les modèles existants**:
```bash
python compare_all_models.py
```

4. **Déployer sur l'API**:
- Uploader vers Hugging Face
- Modifier `api/index.py` pour utiliser le nouveau modèle
- Redéployer sur Cloud Run

---

## 📚 Ressources

- **Documentation Kaggle**: https://www.kaggle.com/docs
- **API Reference**: https://github.com/Kaggle/kaggle-api
- **GPU Usage**: https://www.kaggle.com/docs/efficient-gpu-usage
- **Guide complet**: Voir `docs/KAGGLE_TRAINING.md`

---

## 💡 Conseils

1. **Vérifiez votre téléphone** avant de commencer (requis pour GPU)
2. **Utilisez les sauvegardes** : Le notebook sauvegarde tous les 10 epochs
3. **Mixed Precision** : `amp=True` accélère l'entraînement de ~40%
4. **Early Stopping** : `patience=20` arrête si pas d'amélioration
5. **Upload automatique** : Configurez HF pour ne pas perdre les modèles

---

**Prêt à entraîner ? Lancez `./setup_kaggle.sh` !** 🚀
