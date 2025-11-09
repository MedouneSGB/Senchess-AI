# Inference Scripts

Scripts pour utiliser les modèles entraînés en production et tester leurs performances.

## Scripts Disponibles

### export_openvino.py
Export d'un modèle YOLO vers le format OpenVINO.

**Usage:**
```bash
python scripts/inference/export_openvino.py
```

**Sortie:** Dossier avec le modèle OpenVINO (ex: `best_openvino_model/`)

**Options du script:**
- Modèle source (best.pt)
- Format: OpenVINO IR
- Taille: 640x640
- FP16: Désactivé (meilleure compatibilité)

### benchmark_openvino_fixed.py ⭐ PRODUCTION
Benchmark complet avec l'API native OpenVINO (pas via Ultralytics).

**Résultats Intel Iris Xe:**
```
PyTorch CPU:    58.0ms / image → 17.2 FPS (baseline)
OpenVINO CPU:   25.7ms / image → 38.9 FPS (2.26x speedup)
OpenVINO GPU:    9.7ms / image → 103.6 FPS (6.01x speedup) 🚀
```

**Usage:**
```bash
python scripts/inference/benchmark_openvino_fixed.py
```

**Caractéristiques:**
- Preprocessing natif OpenVINO (pas PIL/PyTorch)
- Performance hint: LATENCY (optimal pour single image)
- 100 iterations de warmup
- 1000 iterations de benchmark
- Statistiques complètes (mean, std, min, max)

### benchmark_openvino.py
Premier benchmark via l'API Ultralytics (plus lent).

**Note:** Utiliser `benchmark_openvino_fixed.py` à la place.

### test_models.py
Tests de validation des modèles entraînés.

**Usage:**
```bash
python scripts/inference/test_models.py
```

### analyze_image.py
Analyse d'images avec un modèle entraîné.

**Usage:**
```bash
python scripts/inference/analyze_image.py --image <path> --model <path>
```

## Workflow OpenVINO

### 1. Entraîner le modèle
```bash
python scripts/training/train_intel.py --quick
```

### 2. Exporter vers OpenVINO
```bash
python scripts/inference/export_openvino.py
```

### 3. Benchmarker les performances
```bash
python scripts/inference/benchmark_openvino_fixed.py
```

### 4. Utiliser en production
```python
import openvino as ov
import numpy as np

# Charger le modèle
core = ov.Core()
model = core.read_model("best_openvino_model/best.xml")
compiled = core.compile_model(model, "GPU", {"PERFORMANCE_HINT": "LATENCY"})

# Inference
input_data = np.random.randn(1, 3, 640, 640).astype(np.float32)
result = compiled([input_data])
```

## OpenVINO GPU Performance ✅

**Pourquoi OpenVINO GPU est 6x plus rapide?**

1. **Optimisations bas niveau**: OpenVINO compile le modèle spécifiquement pour Intel Iris Xe
2. **Kernel fusion**: Combine plusieurs opérations en une seule
3. **Memory management**: Allocation mémoire GPU optimisée
4. **Native preprocessing**: Pas de conversion PIL/PyTorch → NumPy
5. **LATENCY hint**: Optimise pour inference single-image

**Comparaison:**
- PyTorch: CPU only, overhead Python élevé
- OpenVINO CPU: Optimisé mais reste sur CPU
- **OpenVINO GPU: Hardware acceleration + optimisations** 🚀

## Cas d'Usage

### Development (Local)
- Test rapide: PyTorch CPU (simplicité)
- Validation: OpenVINO GPU (performances réelles)

### Production
- Webcam real-time: OpenVINO GPU (103 FPS)
- Batch processing: OpenVINO CPU (parallélisation)
- Cloud inference: PyTorch CUDA (si NVIDIA disponible)

### Embedded/Edge
- Intel NUC: OpenVINO GPU
- Raspberry Pi: OpenVINO CPU + NEON
- NVIDIA Jetson: PyTorch CUDA/TensorRT

## Documentation

Voir `OPENVINO_SUCCESS.md` à la racine pour le guide complet.
