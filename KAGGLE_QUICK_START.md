# 🎯 Guide Rapide - Entraînement sur Kaggle

## ✅ TOUT EST PRÊT !

J'ai créé tous les scripts nécessaires pour entraîner vos modèles sur Kaggle avec GPU gratuit.

---

## 📚 Fichiers Créés

### 📖 Documentation
- **`docs/KAGGLE_TRAINING.md`** - Guide complet  
- **`kaggle_scripts/README.md`** - Documentation des scripts

### 🛠️ Scripts
- **`kaggle_scripts/setup_kaggle.sh`** - Installation automatique de Kaggle CLI
- **`kaggle_scripts/prepare_dataset.py`** - Préparation du dataset (version basique)
- **`kaggle_scripts/prepare_dataset_v2.py`** - Préparation avancée (recommandé)

### 📓 Notebook
- **`kaggle_scripts/training_notebook.ipynb`** - Notebook complet pour Kaggle

---

## 🚀 Guide Étape par Étape

### Étape 1: Créer un Compte Kaggle
1. Allez sur https://www.kaggle.com
2. Créez un compte gratuit
3. **IMPORTANT**: Vérifiez votre numéro de téléphone (Settings → Account)
   - Requis pour utiliser les GPUs gratuits

### Étape 2: Obtenir les Credentials API
1. Allez sur https://www.kaggle.com/settings
2. Scrollez jusqu'à la section "API"
3. Cliquez sur "Create New Token"
4. Téléchargez `kaggle.json`

### Étape 3: Configurer Kaggle CLI (Optionnel)
```bash
# Lancer le script d'installation
./kaggle_scripts/setup_kaggle.sh
```

**Le script va:**
- ✅ Installer Kaggle CLI
- ✅ Créer le dossier `~/.kaggle/`
- ✅ Copier votre `kaggle.json`
- ✅ Configurer les permissions
- ✅ Tester la connexion

### Étape 4: Uploader Votre Dataset

**Option A: Interface Web (Recommandé - Plus Simple)**

1. **Préparer localement** (optionnel):
   ```bash
   python kaggle_scripts/prepare_dataset_v2.py
   # Crée le dossier kaggle_dataset/
   ```

2. **Upload sur Kaggle**:
   - Allez sur https://www.kaggle.com/datasets
   - Cliquez sur "New Dataset"
   - Upload les dossiers de `data/processed/` ou `kaggle_dataset/`:
     - `train/` (images + labels)
     - `valid/` (images + labels)
     - `test/` (images + labels)
   - Titre: "Senchess Chess Pieces Dataset"
   - Visibilité: Public ou Private
   - Cliquez sur "Create"

3. **Notez l'URL**:
   - Exemple: `kaggle.com/datasets/votre-username/senchess-dataset`

**Option B: Kaggle CLI**
```bash
cd kaggle_dataset
kaggle datasets create -p .
```

### Étape 5: Créer un Notebook sur Kaggle

1. **Créer le Notebook**:
   - Allez sur https://www.kaggle.com/code
   - Cliquez sur "New Notebook"
   - Titre: "Senchess AI Training"

2. **Configurer le GPU**:
   - Panneau droit → Settings
   - Accelerator → **GPU T4** (ou P100 si disponible)
   - Internet → **ON**

3. **Ajouter Votre Dataset**:
   - Panneau droit → Add Data
   - Search → "senchess" ou votre nom de dataset
   - Cliquez sur "Add"

4. **Copier le Code d'Entraînement**:
   - Ouvrez `kaggle_scripts/training_notebook.ipynb` en local
   - Copiez TOUT le contenu
   - Collez dans votre notebook Kaggle

5. **Lancer l'Entraînement**:
   - Cliquez sur "Run All" en haut
   - Attendez ~2-4h pour 100 epochs

---

## 📊 Ce qui va se passer

### Pendant l'Entraînement
Le notebook va automatiquement:
1. ✅ Installer Ultralytics (YOLO)
2. ✅ Vérifier le dataset
3. ✅ Charger YOLOv8 pré-entraîné
4. ✅ Entraîner pendant 100 epochs
5. ✅ Sauvegarder le meilleur modèle
6. ✅ Générer graphiques et métriques
7. ✅ Tester sur le test set
8. ✅ (Optionnel) Upload vers Hugging Face

### Résultats Attendus
- **mAP50**: 95-99%
- **mAP50-95**: 85-95%
- **Précision**: >95%
- **Durée**: 2-4h (100 epochs)

---

## 📥 Récupérer Vos Modèles

### Méthode 1: Téléchargement Direct depuis Kaggle
1. Dans le notebook, tous les fichiers sont dans `/kaggle/working/output/`
2. À la fin de l'exécution, cliquez sur le dossier "output"
3. Téléchargez:
   - `senchess_best.pt` - Meilleur modèle
   - `senchess_last.pt` - Dernier checkpoint
   - `results.csv` - Métriques
   - `results.png` - Graphiques
   - `confusion_matrix.png`

### Méthode 2: Upload Automatique vers Hugging Face
Le notebook inclut une cellule pour uploader automatiquement:
```python
# Dernière cellule du notebook
api.upload_file(
    path_or_fileobj="best.pt",
    path_in_repo="senchess_kaggle_v1.pt",
    repo_id="MedouneSGB/senchess-models",
    token="votre_token_hf"
)
```

---

## ⏱️ Temps d'Entraînement

| GPU | Epochs | Temps Estimé |
|-----|--------|--------------|
| T4 | 100 | 2-3 heures |
| P100 | 100 | 1.5-2 heures |
| TPU v3-8 | 100 | 1-1.5 heures |

---

## 💡 Astuces

### Limites Kaggle
- **30h de GPU par semaine** (gratuit)
- **12h maximum par session**
- Sauvegardez régulièrement !

### Si Vous Manquez de Temps
Réduisez les epochs dans le notebook:
```python
results = model.train(
    epochs=50,  # Au lieu de 100
    ...
)
```

### Optimiser la Vitesse
- Utilisez GPU P100 si disponible (2x plus rapide que T4)
- Activez `amp=True` (déjà fait dans le notebook)
- Augmentez le batch size si vous avez la RAM

---

## 🔧 Dépannage

### "Phone verification required"
→ Allez sur Kaggle Settings → Account → Ajoutez votre téléphone

### "Dataset not found"
→ Vérifiez que vous avez bien ajouté le dataset au notebook (Add Data)

### "Out of Memory"
→ Réduisez le batch size dans le notebook:
```python
batch=8  # Au lieu de 16
```

### Le notebook se bloque
→ C'est normal ! L'entraînement prend 2-4h. Laissez tourner.

---

## 🎯 Après l'Entraînement

1. **Téléchargez les modèles**
2. **Testez en local**:
   ```bash
   python test_models.py
   ```

3. **Comparez avec vos modèles existants**:
   ```bash
   python compare_all_models.py
   ```

4. **Déployez sur votre API**:
   - Uploadez vers Hugging Face
   - Modifiez `api/index.py`
   - Redéployez sur Cloud Run

---

## 📞 Ressources

- **Documentation Kaggle**: https://www.kaggle.com/docs
- **Notre guide complet**: `docs/KAGGLE_TRAINING.md`
- **Scripts**: `kaggle_scripts/`
- **Notebook**: `kaggle_scripts/training_notebook.ipynb`

---

## ✅ Checklist Rapide

- [ ] Compte Kaggle créé
- [ ] Téléphone vérifié (IMPORTANT!)
- [ ] kaggle.json téléchargé
- [ ] Dataset uploadé sur Kaggle
- [ ] Notebook créé avec GPU T4
- [ ] Dataset ajouté au notebook
- [ ] Code copié du fichier local
- [ ] Run All lancé
- [ ] ☕ Café pendant que ça tourne (2-4h)

---

**Prêt ? Commencez par créer votre compte Kaggle et vérifier votre téléphone !** 🚀

**Besoin d'aide ?** Consultez `docs/KAGGLE_TRAINING.md` pour le guide détaillé.
