# Utilities Scripts

Outils de diagnostic, visualisation et comparaison des modèles.

## Device Detection

### check_devices.py
Vérifie les devices OpenVINO disponibles.

**Usage:**
```bash
python scripts/utils/check_devices.py
```

**Sortie typique:**
```
Devices: ['CPU', 'GPU']
CPU: Intel(R) Core(TM) i7-1185G7 @ 3.00GHz
GPU: Intel(R) Iris(R) Xe Graphics [0x9a49]
```

### check_gpu.py
Détecte les GPU NVIDIA (CUDA).

**Usage:**
```bash
python scripts/utils/check_gpu.py
```

**Sortie si pas de GPU NVIDIA:**
```
No NVIDIA GPU detected
PyTorch CUDA available: False
```

### check_gpu_intel.py
Détecte les GPU Intel et affiche les informations.

**Usage:**
```bash
python scripts/utils/check_gpu_intel.py
```

### debug_openvino.py
Diagnostics complets OpenVINO (devices, versions, capabilities).

**Usage:**
```bash
python scripts/utils/debug_openvino.py
```

## Model Comparison

### compare_all_models.py
Compare les performances de tous les modèles disponibles.

**Usage:**
```bash
python scripts/utils/compare_all_models.py
```

**Métriques comparées:**
- mAP50, mAP50-95
- Precision, Recall
- Temps d'inférence
- Taille du modèle

### compare_ultimate_haki.py
Comparaison spécifique entre modèles ultimate et haki.

**Usage:**
```bash
python scripts/utils/compare_ultimate_haki.py
```

## Visualization

### view_results.py
Visualise les résultats d'entraînement (courbes loss, métriques).

**Usage:**
```bash
python scripts/utils/view_results.py
```

**Génère:**
- Graphiques de loss (box_loss, cls_loss, dfl_loss)
- Courbes de métriques (mAP, Precision, Recall)
- Comparaison train vs validation

### view_ensemble.py
Visualise les performances du modèle ensemble.

**Usage:**
```bash
python scripts/utils/view_ensemble.py
```

### view_ultimate_haki.py
Visualise et compare ultimate vs haki.

**Usage:**
```bash
python scripts/utils/view_ultimate_haki.py
```

## Dataset Management

### create_ultimate_dataset.py
Crée le dataset ultimate en combinant plusieurs datasets.

**Usage:**
```bash
python scripts/utils/create_ultimate_dataset.py
```

**Processus:**
1. Combine chess_dataset_1000 + chess_decoder_1000
2. Fusionne les annotations
3. Vérifie la cohérence
4. Génère data.yaml

**Sortie:** `data/chess_ultimate_1693/`

### regenerate_annotations.py
Régénère les fichiers d'annotations YOLO.

**Usage:**
```bash
python scripts/utils/regenerate_annotations.py
```

**Utilité:**
- Corriger format d'annotations
- Convertir d'autres formats vers YOLO
- Filtrer classes invalides

## Workflow Typique

### 1. Vérifier Hardware
```bash
python scripts/utils/check_devices.py
python scripts/utils/check_gpu_intel.py
```

### 2. Entraîner Modèle
```bash
python scripts/training/train_intel.py --quick
```

### 3. Visualiser Résultats
```bash
python scripts/utils/view_results.py
```

### 4. Comparer Modèles
```bash
python scripts/utils/compare_all_models.py
```

### 5. Export Production
```bash
python scripts/inference/export_openvino.py
```

## Tips

### Debug OpenVINO Issues
```bash
python scripts/utils/debug_openvino.py > openvino_debug.txt
```

### Compare Before/After Training
```bash
# Avant nouvel entraînement
python scripts/utils/compare_all_models.py > before.txt

# Après entraînement
python scripts/utils/compare_all_models.py > after.txt

# Comparer
diff before.txt after.txt
```

### Monitor Training Live
```bash
# Terminal 1: Training
python scripts/training/train_intel.py --quick

# Terminal 2: Watch results
watch -n 10 python scripts/utils/view_results.py
```
