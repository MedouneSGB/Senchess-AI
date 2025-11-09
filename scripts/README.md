# Scripts Directory

Cette organisation du projet permet de mieux comprendre et maintenir le code.

## Structure

### 📚 training/
Scripts d'entraînement des modèles YOLO.
- **train_intel.py** - Production : Entraînement optimisé pour CPU Intel (MKL)
- **train_ultimate.py** - Entraînement sur dataset ultimate
- **train_new_model.py** - Entraînement nouveau modèle 13 classes
- **ensemble_model.py** - Modèle ensemble (combinaison de plusieurs modèles)

### 🚀 inference/
Scripts pour utiliser les modèles entraînés.
- **export_openvino.py** - Export modèle YOLO vers OpenVINO
- **benchmark_openvino_fixed.py** - Benchmark OpenVINO (GPU/CPU) - 6x speedup! ✅
- **benchmark_openvino.py** - Premier benchmark via Ultralytics API
- **test_models.py** - Tests de validation des modèles
- **analyze_image.py** - Analyse d'images avec le modèle

### 🔧 utils/
Outils utilitaires et scripts de diagnostic.
- **check_devices.py** - Vérifier devices OpenVINO disponibles
- **check_gpu.py** - Détecter GPU NVIDIA
- **check_gpu_intel.py** - Détecter GPU Intel
- **debug_openvino.py** - Diagnostics OpenVINO
- **view_results.py** - Visualiser résultats d'entraînement
- **compare_all_models.py** - Comparer performances des modèles
- **compare_ultimate_haki.py** - Comparaison modèles ultimate vs haki
- **view_ensemble.py** - Visualiser modèle ensemble
- **view_ultimate_haki.py** - Visualiser modèles ultimate et haki
- **create_ultimate_dataset.py** - Créer dataset ultimate
- **regenerate_annotations.py** - Regénérer annotations dataset

### 🧪 experiments/
Expérimentations et tests (IPEX, PyTorch downgrade, etc.)
- **experiment_ipex.py** - Test complet IPEX (échoué - drivers manquants)
- **downgrade_pytorch.py** - Downgrade PyTorch 2.9 → 2.8 pour IPEX
- **install_gpu_intel.py** - Installateur IPEX
- **install_gpu.py** - Installateur GPU générique

## Usage Rapide

### Entraînement
```bash
# Entraînement rapide (10 epochs)
python scripts/training/train_intel.py --quick

# Entraînement complet (100 epochs)
python scripts/training/train_intel.py
```

### Export OpenVINO
```bash
python scripts/inference/export_openvino.py
```

### Benchmark Performances
```bash
python scripts/inference/benchmark_openvino_fixed.py
```

## Résultats OpenVINO GPU ✅

**Intel Iris Xe Graphics - 6x speedup!**
- PyTorch CPU: 58ms (17 FPS)
- OpenVINO CPU: 26ms (39 FPS) - 2.26x speedup
- **OpenVINO GPU: 10ms (103 FPS) - 6.01x speedup** 🚀

Voir `OPENVINO_SUCCESS.md` pour plus de détails.
