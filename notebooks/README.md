# 🚀 Entraînement sur Google Colab

Ce dossier contient le notebook pour entraîner Senchess-AI sur Google Colab avec GPU gratuit.

## 📂 Fichiers

- **`train_on_colab.ipynb`** : Notebook prêt à l'emploi pour Colab

## 🎯 Comment utiliser

### Option 1 : Lien direct (RECOMMANDÉ)

Cliquez sur le badge ci-dessous pour ouvrir directement dans Colab :

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MedouneSGB/Senchess-AI/blob/gpu-cloud-training/notebooks/train_on_colab.ipynb)

### Option 2 : Upload manuel

1. Allez sur [Google Colab](https://colab.research.google.com/)
2. Cliquez sur `File` → `Upload notebook`
3. Sélectionnez `train_on_colab.ipynb`

### Option 3 : Via GitHub

1. Allez sur [Google Colab](https://colab.research.google.com/)
2. Cliquez sur l'onglet `GitHub`
3. Entrez : `MedouneSGB/Senchess-AI`
4. Sélectionnez la branche : `gpu-cloud-training`
5. Ouvrez le notebook

## ⚡ Configuration GPU

**IMPORTANT** : Avant d'exécuter le notebook, activez le GPU :

1. Menu `Runtime` → `Change runtime type`
2. Sélectionnez `GPU` (T4 GPU)
3. Cliquez `Save`

## 📊 Dataset inclus

Ce notebook utilise **`chess_dataset_1000`** qui est inclus dans la branche `gpu-cloud-training`.

Structure :
```
data/chess_dataset_1000/
├── dataset.yaml
├── train/
│   ├── images/
│   └── labels/
├── val/
│   ├── images/
│   └── labels/
└── test/
    ├── images/
    └── labels/
```

**Total** : ~1000 images de plateaux d'échecs annotés

## 🎓 Ordre d'exécution

1. ✅ Cellule 2 : Vérifier le GPU
2. ✅ Cellule 3 : Installer les dépendances
3. ✅ Cellule 4 : Cloner le repo (charge automatiquement le dataset)
4. ✅ Cellule 7 : Entraîner le modèle
5. ✅ Cellule 8 : Télécharger le modèle entraîné
6. ✅ Cellule 9 : Tester le modèle
7. ✅ Cellule 11 : Visualiser les métriques

## ⏱️ Temps estimé

- **Installation** : 2-3 minutes
- **Clone + Dataset** : 1-2 minutes
- **Entraînement (100 epochs)** : 1-2 heures (avec GPU T4)
- **Total** : ~1h30-2h30

## 💡 Astuces

### Réduire le temps d'entraînement
Dans la cellule 7, modifiez :
```python
epochs=50,  # Au lieu de 100
```

### Augmenter la performance
Si vous avez assez de VRAM :
```python
batch=32,  # Au lieu de 16
```

### Utiliser un modèle plus puissant
```python
model = YOLO('yolov8m.pt')  # Au lieu de yolov8n.pt
```

## 🆘 Problèmes courants

### "Unable to read file"
- ✅ Vérifiez que vous avez exécuté la cellule 4 pour cloner le repo
- ✅ Assurez-vous d'être sur la branche `gpu-cloud-training`

### "Out of memory"
- ✅ Réduisez `batch_size` à 8 ou 4
- ✅ Utilisez un modèle plus petit (yolov8n.pt)

### Session déconnectée
- ✅ Colab Free limite les sessions à 12h
- ✅ Téléchargez régulièrement vos checkpoints (cellule 8)
- ✅ Passez à Colab Pro pour des sessions plus longues

## 📈 Résultats attendus

Après l'entraînement, vous devriez obtenir :

- **mAP50** : ~85-95%
- **Précision** : ~90%+
- **Rappel** : ~85%+

## 📥 Télécharger les résultats

La cellule 8 créera un fichier `trained_model.zip` contenant :
- `weights/best.pt` : Meilleur modèle
- `weights/last.pt` : Dernier checkpoint
- Graphiques d'entraînement
- Métriques détaillées

## 🔗 Ressources supplémentaires

- [Documentation YOLOv8](https://docs.ultralytics.com/)
- [Guide GPU Cloud complet](../docs/GPU_CLOUD_GUIDE.md)
- [Repo principal](https://github.com/MedouneSGB/Senchess-AI)

## 📞 Support

En cas de problème, ouvrez une issue sur [GitHub](https://github.com/MedouneSGB/Senchess-AI/issues)

---

**Bon entraînement ! 🚀♟️**
