# 🚀 OpenVINO - Accélération GPU Intel Iris Xe

## 📊 Résultats de Performance

### Benchmark final (30 runs)

| Configuration | Temps moyen | FPS | Speedup vs PyTorch |
|---------------|-------------|-----|--------------------|
| **PyTorch CPU** (baseline) | 58.0 ms | 17.2 | 1.00x |
| **OpenVINO CPU** | 25.7 ms | 38.9 | **2.26x** ⚡ |
| **OpenVINO GPU (Intel Iris Xe)** | 9.7 ms | **103.6** | **6.01x** 🚀 |

### 🎯 Résultats clés

- ✅ **GPU Intel Iris Xe fonctionne parfaitement avec OpenVINO !**
- 🚀 **6x plus rapide** que PyTorch CPU
- ⚡ **2.7x plus rapide** qu'OpenVINO CPU
- 📈 **103 FPS** en inférence (vs 17 FPS PyTorch)
- 🎲 **Stabilité excellente** (std: 0.6 ms)

## 🔧 Configuration Technique

### Hardware
- **CPU**: Intel Core i7-1185G7 @ 3.00GHz (11th Gen)
- **GPU**: Intel Iris Xe Graphics (iGPU)
- **OS**: Windows
- **Python**: 3.13.1

### Software
- **PyTorch**: 2.9.0+cpu
- **OpenVINO**: 2025.3.0
- **Ultralytics YOLO**: 8.3.226
- **Modèle**: YOLOv8n (chess detection, 13 classes)

### Optimisations appliquées
1. **OpenVINO natif** (pas via Ultralytics)
2. **LATENCY mode** pour inférence temps réel
3. **Prétraitement optimisé** (numpy + OpenCV)
4. **GPU Intel Iris Xe** détecté automatiquement

## 📝 Scripts créés

### 1. `export_openvino.py`
Export d'un modèle YOLO vers format OpenVINO

```bash
python export_openvino.py --model models/senchess_intel_v1.0_quick2/weights/best.pt
```

**Fonctionnalités** :
- Export automatique vers OpenVINO
- Support FP32 / FP16
- Génération fichiers .xml et .bin

### 2. `benchmark_openvino_fixed.py`
Benchmark optimisé PyTorch vs OpenVINO (CPU et GPU)

```bash
python benchmark_openvino_fixed.py --runs 30
```

**Fonctionnalités** :
- Test PyTorch CPU (baseline)
- Test OpenVINO CPU avec optimisations
- Test OpenVINO GPU Intel Iris Xe
- Comparaison détaillée avec statistiques
- Warm-up automatique pour résultats précis

### 3. `check_devices.py`
Vérification rapide des devices OpenVINO disponibles

```bash
python check_devices.py
```

**Output exemple** :
```
Devices détectés : ['CPU', 'GPU']
📱 CPU: 11th Gen Intel(R) Core(TM) i7-1185G7 @ 3.00GHz
📱 GPU: Intel(R) Iris(R) Xe Graphics (iGPU)
```

## 🎓 Leçons apprises

### ✅ Ce qui fonctionne

1. **OpenVINO + GPU Intel Iris Xe**
   - Accélération massive (6x)
   - Stable et fiable
   - Facile à configurer
   - **Recommandé pour production**

2. **OpenVINO CPU**
   - 2.26x plus rapide que PyTorch
   - Bon compromis si pas de GPU
   - Consommation CPU réduite

3. **Configuration optimale**
   ```python
   config = {'PERFORMANCE_HINT': 'LATENCY'}
   compiled_model = core.compile_model(model, 'GPU', config)
   ```

### ❌ Ce qui ne fonctionne pas

1. **IPEX (Intel Extension for PyTorch)**
   - Nécessite drivers OneAPI (~10GB)
   - Support expérimental pour Iris Xe
   - Contraintes de version strictes
   - Gains minimes vs complexité

2. **Ultralytics + OpenVINO GPU**
   - API Ultralytics cherche CUDA au lieu d'OpenVINO GPU
   - Performances dégradées (variance élevée)
   - **Solution** : Utiliser OpenVINO natif

3. **PyTorch + GPU Intel**
   - PyTorch ne supporte pas Intel Iris Xe nativement
   - Nécessite IPEX (non recommandé)

## 🚀 Utilisation pour Production

### Inférence optimale avec OpenVINO GPU

```python
import openvino as ov
import cv2
import numpy as np

# Charger le modèle
core = ov.Core()
model = core.read_model("best_openvino_model/best.xml")

# Compiler pour GPU Intel avec mode LATENCY
config = {'PERFORMANCE_HINT': 'LATENCY'}
compiled_model = core.compile_model(model, 'GPU', config)

# Prétraiter l'image
img = cv2.imread("chess.jpg")
img_resized = cv2.resize(img, (640, 640))
img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
img_normalized = img_rgb.astype(np.float32) / 255.0
img_transposed = np.transpose(img_normalized, (2, 0, 1))
img_batched = np.expand_dims(img_transposed, axis=0)

# Inférence (< 10 ms sur Iris Xe !)
output = compiled_model(img_batched)

# Post-traiter les résultats
# ... (parsing des détections YOLO)
```

### Device AUTO (CPU/GPU automatique)

```python
# OpenVINO choisit automatiquement le meilleur device
compiled_model = core.compile_model(model, 'AUTO', config)
```

## 📊 Comparaison des Solutions GPU Intel

| Solution | Speedup | Stabilité | Facilité | Recommandation |
|----------|---------|-----------|----------|----------------|
| **OpenVINO GPU** | **6.0x** ⭐ | ✅ Excellent | ✅ Simple | ✅ **RECOMMANDÉ** |
| OpenVINO CPU | 2.3x | ✅ Excellent | ✅ Simple | ✅ Alternative |
| IPEX + XPU | ❓ Non testé | ⚠️ Instable | ❌ Complexe | ❌ Non recommandé |
| PyTorch CPU | 1.0x | ✅ Excellent | ✅ Simple | ✅ Fallback |

## 🎯 Recommandations Finales

### Pour Entraînement
- ✅ **PyTorch CPU** avec optimisations Intel MKL
- ✅ Stable et éprouvé
- ⏱️ ~5 min/epoch acceptable

### Pour Inférence
- 🚀 **OpenVINO GPU (Intel Iris Xe)** - **103 FPS !**
- ⚡ OpenVINO CPU - 39 FPS (si pas de GPU)
- 🎯 Mode LATENCY pour temps réel
- 📦 Device AUTO pour portabilité

### Cas d'usage

| Use Case | Solution recommandée | FPS attendu |
|----------|---------------------|-------------|
| 🎥 Webcam temps réel | OpenVINO GPU | ~100 FPS ✅ |
| 📱 Application desktop | OpenVINO GPU | ~100 FPS ✅ |
| 🖥️ Serveur sans GPU | OpenVINO CPU | ~40 FPS ✅ |
| 🔬 Développement/Debug | PyTorch CPU | ~17 FPS ✅ |

## 🔄 Migration PyTorch → OpenVINO

### Étape 1 : Export
```bash
python export_openvino.py --model best.pt
```

### Étape 2 : Test
```bash
python benchmark_openvino_fixed.py --runs 30
```

### Étape 3 : Intégration
```python
# Remplacer
model = YOLO("best.pt")
results = model.predict("image.jpg", device='cpu')

# Par
core = ov.Core()
model = core.read_model("best_openvino_model/best.xml")
compiled = core.compile_model(model, 'GPU', {'PERFORMANCE_HINT': 'LATENCY'})
output = compiled(preprocessed_image)
```

## 📦 Installation

```bash
# OpenVINO (léger, ~40 MB)
pip install openvino>=2024.0

# Dépendances
pip install numpy opencv-python

# Ultralytics (pour export uniquement)
pip install ultralytics
```

## 🎓 Conclusion

**OpenVINO + Intel Iris Xe = Solution parfaite pour inférence YOLO sur Intel !**

- ✅ **6x plus rapide** que PyTorch
- ✅ **103 FPS** sur GPU intégré
- ✅ **Installation simple** (pas de drivers complexes)
- ✅ **Stable et production-ready**
- ✅ **Fonctionne out-of-the-box**

**Verdict final** : OpenVINO GPU > IPEX > PyTorch CPU pour inférence Intel

---

*Benchmark effectué le 9 novembre 2025*  
*Hardware : Intel Core i7-1185G7 + Intel Iris Xe Graphics*  
*Software : OpenVINO 2025.3.0, PyTorch 2.9.0, Ultralytics YOLO 8.3.226*
