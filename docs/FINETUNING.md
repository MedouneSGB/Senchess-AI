# 🎯 Guide de Fine-Tuning Senchess AI

Ce guide explique comment fine-tuner les modèles pour améliorer leurs performances.

---

## 📋 Options Disponibles

### Option 1 : Gear v1.1 (Quick Win) ⚡
**Durée :** 2-3 heures  
**Objectif :** 98.5% → 99%+ mAP50

```bash
./run_finetune_gear.sh
```

**Ce qui se passe :**
- Part de Gear v1.0 (98.5% mAP50)
- 30 epochs supplémentaires
- Learning rate réduit (0.0001)
- Dataset : 693 images (photos physiques)

---

### Option 2 : Gear-Haki Ultimate 🏆
**Durée :** 4-6 heures  
**Objectif :** Modèle universel 2D + 3D

```bash
./run_finetune.sh
```

**Ce qui se passe :**
1. **Fusion des datasets** (automatique)
   - Gear : 693 images (photos 3D)
   - Haki : 1000 images (diagrammes 2D)
   - Total : 1693 images

2. **Fine-tuning depuis Haki v1.0**
   - Meilleur modèle de base (99.5% mAP50)
   - 50 epochs
   - Learning rate : 0.001

---

## 🔧 Fine-Tuning Manuel

### Script Python
```bash
source .venv/bin/activate

python src/finetune.py \
    --gear-data data/processed \
    --haki-data data/chess_decoder_1000 \
    --output-data data/gear_haki_merged \
    --base-model models/senchess_haki_v1.0/weights/best.pt \
    --epochs 50 \
    --lr0 0.001 \
    --name senchess_gear_haki_finetune
```

### Options disponibles
```
--gear-data      : Chemin dataset Gear (défaut: data/processed)
--haki-data      : Chemin dataset Haki (défaut: data/chess_decoder_1000)
--output-data    : Chemin dataset fusionné (défaut: data/gear_haki_merged)
--base-model     : Modèle de base (défaut: haki v1.0)
--epochs         : Nombre d'epochs (défaut: 50)
--lr0            : Learning rate (défaut: 0.001)
--name           : Nom du modèle (défaut: senchess_gear_haki_finetune)
--skip-merge     : Skip fusion dataset (si déjà fait)
```

---

## 📊 Résultats Attendus

### Gear v1.1
- **mAP50 :** 99%+ (vs 98.5%)
- **Spécialisation :** Photos physiques 3D
- **Usage :** Production pour photos smartphone

### Gear-Haki Ultimate
- **mAP50 :** 99%+ (objectif)
- **Spécialisation :** Universel (2D + 3D)
- **Usage :** Production pour tous types d'images

---

## 🧪 Évaluation

Après le fine-tuning, évaluez le nouveau modèle :

```bash
# Évaluation simple
python src/evaluate.py --model models/senchess_gear_v1.1/weights/best.pt

# Comparaison avec modèles existants
python src/evaluate.py --compare

# Métriques détaillées par classe
python src/evaluate.py --model models/senchess_gear_v1.1/weights/best.pt --detailed

# Benchmark sur image
python src/evaluate.py --benchmark imgTest/capture2.jpg
```

---

## 📈 Monitoring

Pendant l'entraînement, suivez :

### Terminal
- Loss progression
- mAP50 / mAP50-95
- Precision / Recall
- Temps par epoch

### Fichiers générés
```
models/[nom_modele]/
├── weights/
│   ├── best.pt           # Meilleur modèle (mAP50)
│   └── last.pt           # Dernier epoch
├── results.csv           # Métriques par epoch
├── results.png           # Courbes d'apprentissage
├── confusion_matrix.png  # Matrice de confusion
└── args.yaml            # Configuration
```

---

## 💡 Conseils

### Pour améliorer mAP50
- ✅ Augmenter epochs (30-100)
- ✅ Réduire learning rate (0.0001-0.001)
- ✅ Activer data augmentation
- ✅ Partir du meilleur modèle

### Pour éviter l'overfitting
- ⚠️ Early stopping (patience=50)
- ⚠️ Validation régulière
- ⚠️ Dropout si nécessaire
- ⚠️ Surveiller val_loss

### Pour accélérer
- 🚀 Réduire batch size si RAM limitée
- 🚀 Utiliser GPU si disponible (--device cuda)
- 🚀 Réduire image size (--imgsz 416)

---

## 🐛 Troubleshooting

### Problème : CUDA Out of Memory
```bash
# Solution : Réduire batch size
python src/finetune.py --batch 4  # au lieu de 8
```

### Problème : Val Loss augmente
```bash
# Solution : Réduire learning rate
python src/finetune.py --lr0 0.0001
```

### Problème : Dataset merge échoue
```bash
# Solution : Skip merge si déjà fait
python src/finetune.py --skip-merge
```

---

## 📊 Comparaison des Stratégies

| Stratégie | Durée | Complexité | mAP50 attendu | Usage |
|-----------|-------|------------|---------------|-------|
| Gear v1.1 | 2-3h | ⭐ Facile | 99%+ | Photos 3D uniquement |
| Ultimate | 4-6h | ⭐⭐ Moyenne | 99%+ | Universel 2D + 3D |
| Custom | Variable | ⭐⭐⭐ Avancé | Variable | Cas spécifique |

---

## 🚀 Prochaines Étapes

Après le fine-tuning :

1. **Évaluation complète**
   ```bash
   python src/evaluate.py --model models/[nouveau_modele]/weights/best.pt --detailed
   ```

2. **Benchmark comparatif**
   ```bash
   python src/evaluate.py --compare
   ```

3. **Tests en production**
   ```bash
   python src/predict.py --model models/[nouveau_modele]/weights/best.pt --source imgTest/
   ```

4. **Mise à jour MODEL_CONFIG.yaml**
   - Ajouter les nouvelles métriques
   - Documenter les spécialisations
   - Versionner le modèle

5. **Commit et push**
   ```bash
   git add models/[nouveau_modele]
   git commit -m "🎯 Ajout [nouveau_modele] via fine-tuning"
   git push origin main
   ```

---

## 📝 Notes

- Le fine-tuning conserve les connaissances du modèle de base
- Learning rate plus faible = apprentissage plus stable
- Plus d'epochs = meilleure performance (jusqu'à un certain point)
- Toujours valider sur données de test non vues

---

**🎯 Bon fine-tuning !**
