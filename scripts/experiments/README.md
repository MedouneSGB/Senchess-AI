# Experiments Scripts

Scripts expérimentaux pour tester différentes technologies GPU Intel.

## ⚠️ IPEX - ÉCHOUÉ

### experiment_ipex.py
Test complet d'Intel Extension for PyTorch (IPEX).

**Statut:** ❌ ÉCHOUÉ
**Raison:** DLL manquante (esimd_kernels.dll) - nécessite Intel OneAPI Base Toolkit (~10GB)

**Test en 4 étapes:**
1. ✅ Installation IPEX
2. ✅ Import IPEX
3. ✅ Optimisation modèle
4. ❌ **Inference avec GPU** (DLL manquante)

**Usage:**
```bash
python scripts/experiments/experiment_ipex.py
```

**Erreur rencontrée:**
```
OSError: [WinError 126] The specified module could not be found
esimd_kernels.dll not found
```

**Documentation complète:** Voir `GPU_INTEL_CONCLUSION.md`

### downgrade_pytorch.py
Script pour downgrader PyTorch 2.9 → 2.8 (requis pour IPEX).

**Statut:** ✅ Fonctionne (mais IPEX reste bloqué)

**Usage:**
```bash
python scripts/experiments/downgrade_pytorch.py
```

**Actions:**
- Désinstalle PyTorch 2.9+cpu
- Installe PyTorch 2.8.0+cpu
- Installe torchvision 0.19.0+cpu compatible

**Note:** Après échec IPEX, projet revenu à PyTorch 2.9 (stable).

### install_gpu_intel.py
Installateur automatique IPEX + dépendances.

**Statut:** ✅ Installation OK, ❌ Runtime échoue

**Usage:**
```bash
python scripts/experiments/install_gpu_intel.py
```

**Installe:**
- intel-extension-for-pytorch
- oneccl_bind_pt (communication collective)

**Problème:** Installation réussit mais IPEX nécessite Intel OneAPI drivers.

### install_gpu.py
Installateur GPU générique (essai initial).

**Statut:** ⚠️ Obsolète (remplacé par install_gpu_intel.py)

## Conclusion IPEX vs OpenVINO

### IPEX ❌
**Avantages:**
- Intégration transparente avec PyTorch
- Même API que PyTorch CUDA
- Pas de conversion de modèle

**Inconvénients:**
- ❌ Nécessite Intel OneAPI (~10GB)
- ❌ DLL manquantes (esimd_kernels.dll)
- ❌ Compatible seulement PyTorch 2.8 (pas 2.9)
- ❌ Setup complexe sous Windows
- ⚠️ Gains théoriques faibles pour Intel Iris Xe

### OpenVINO ✅ SOLUTION RETENUE
**Avantages:**
- ✅ Installation simple (pip install openvino)
- ✅ 6x speedup prouvé (103 FPS vs 17 FPS)
- ✅ Détection automatique Intel Iris Xe GPU
- ✅ API stable et mature
- ✅ Fonctionne out-of-the-box

**Inconvénients:**
- ⚠️ Inference seulement (pas training)
- ⚠️ Nécessite export du modèle

**Résultat:** OpenVINO est la meilleure solution pour Intel Iris Xe.

## Leçons Apprises

### 1. IPEX n'est pas prêt pour Windows + Intel iGPU
- Setup trop complexe
- Drivers manquants
- Documentation insuffisante

### 2. OpenVINO est la solution officielle Intel
- Supporté par Intel
- Optimisé spécifiquement pour leurs GPUs
- Production-ready

### 3. Intel Iris Xe = GPU d'inférence, pas training
- Trop faible pour training YOLO
- Excellent pour inference (103 FPS!)
- CPU reste optimal pour training

### 4. PyTorch 2.9 > PyTorch 2.8
- Plus stable
- Meilleures performances CPU
- Pas besoin de downgrade pour OpenVINO

## Recommandations

### Pour Intel Iris Xe:
1. ✅ **Training:** CPU avec Intel MKL (train_intel.py)
2. ✅ **Inference:** OpenVINO GPU (103 FPS)
3. ❌ **IPEX:** Ne pas utiliser (trop complexe, gains faibles)

### Pour NVIDIA GPU:
1. ✅ **Training:** PyTorch CUDA
2. ✅ **Inference:** PyTorch CUDA ou TensorRT
3. ❌ **OpenVINO:** Possible mais moins optimisé que TensorRT

### Pour CPU uniquement:
1. ✅ **Training:** Intel MKL (train_intel.py)
2. ✅ **Inference:** OpenVINO CPU (2.26x speedup)
3. ⚠️ **PyTorch:** Baseline (17 FPS)

## Documentation Complète

- **IPEX failure:** `GPU_INTEL_CONCLUSION.md`
- **OpenVINO success:** `OPENVINO_SUCCESS.md`
- **Setup initial:** `GPU_SETUP.md`

## Ne PAS Utiliser Pour Production

Ces scripts sont expérimentaux et servent uniquement à:
- Comprendre les limitations IPEX
- Documenter les tentatives
- Éducation et apprentissage

**Pour production, utiliser:**
- Training: `scripts/training/train_intel.py`
- Inference: `scripts/inference/benchmark_openvino_fixed.py`
