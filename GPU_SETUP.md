# Support GPU - Senchess AI

## 🎮 Configuration GPU

Cette branche ajoute le support complet du GPU pour accélérer l'entraînement des modèles.

## 📋 Changements

### 1. Requirements.txt mis à jour
- Ajout de PyTorch avec support CUDA
- Versions compatibles avec les GPUs NVIDIA

### 2. Scripts d'entraînement modifiés
- `train_ultimate.py` : Détection automatique du GPU
- Batch size adaptatif (16 avec GPU, 8 avec CPU)
- Affichage des informations GPU au démarrage

### 3. Nouveau script : check_gpu.py
- Vérifie la disponibilité du GPU
- Affiche les spécifications (mémoire, compute capability)
- Benchmark GPU vs CPU
- Recommandations pour l'entraînement

## 🚀 Installation

### Étape 1 : Vérifier les drivers NVIDIA
Assurez-vous que les drivers NVIDIA sont installés :
```powershell
nvidia-smi
```

### Étape 2 : Installer les dépendances
```powershell
# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Installer PyTorch avec CUDA (pour GPU NVIDIA)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Installer les autres dépendances
pip install -r requirements.txt
```

**Note :** Remplacez `cu118` par votre version CUDA :
- CUDA 11.8 → `cu118`
- CUDA 12.1 → `cu121`

Vérifier votre version CUDA avec : `nvidia-smi`

### Étape 3 : Vérifier le GPU
```powershell
python check_gpu.py
```

Ce script affichera :
- ✅ Si le GPU est détecté et fonctionnel
- 📊 Les spécifications du GPU (nom, mémoire)
- ⚡ Un benchmark de performance
- 💡 Des recommandations pour l'entraînement

## 📈 Performance attendue

### Temps d'entraînement (50 epochs, ~1700 images)

| Device | Temps estimé | Accélération |
|--------|-------------|--------------|
| CPU (Intel Core i5) | 8-15 heures | 1x |
| GPU (GTX 1660) | 60-90 minutes | ~10x |
| GPU (RTX 3060) | 30-45 minutes | ~15x |
| GPU (RTX 4090) | 15-25 minutes | ~25x |

### Batch size recommandé

| Mémoire GPU | Batch size |
|-------------|------------|
| 4 GB | 8 |
| 6 GB | 12-16 |
| 8 GB | 16-24 |
| 12+ GB | 24-32 |

## 🏋️ Entraînement avec GPU

L'entraînement détecte automatiquement le GPU :

```powershell
# Entraînement complet (50 epochs)
python train_ultimate.py

# Entraînement rapide pour tester (10 epochs)
python train_ultimate.py --quick
```

Le script affichera :
```
🖥️  Device détecté : CUDA
   GPU : NVIDIA GeForce RTX 3060
   CUDA Version : 11.8
```

## ❌ Résolution de problèmes

### Le GPU n'est pas détecté

1. **Vérifier les drivers NVIDIA**
   ```powershell
   nvidia-smi
   ```

2. **Vérifier la version CUDA**
   ```powershell
   nvcc --version
   ```

3. **Réinstaller PyTorch avec CUDA**
   ```powershell
   pip uninstall torch torchvision torchaudio
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

### Erreur "Out of Memory" (OOM)

Si vous obtenez une erreur de mémoire GPU :

1. Réduire le batch size dans `train_ultimate.py` :
   ```python
   'batch': 8,  # ou 4 si toujours des problèmes
   ```

2. Réduire la taille des images :
   ```python
   'imgsz': 416,  # au lieu de 640
   ```

3. Vider le cache GPU :
   ```python
   import torch
   torch.cuda.empty_cache()
   ```

## 🔄 Retour à la version CPU

Si vous souhaitez revenir à l'utilisation du CPU uniquement :

```powershell
# Basculer vers la branche main
git checkout main

# Ou modifier manuellement dans train_ultimate.py
device = 'cpu'
```

## 📊 Monitoring GPU pendant l'entraînement

Ouvrir un nouveau terminal et exécuter :
```powershell
# Afficher l'utilisation GPU en temps réel
nvidia-smi -l 1
```

ou installer gpustat pour une vue plus détaillée :
```powershell
pip install gpustat
gpustat -i 1
```

## 💡 Conseils d'optimisation

1. **Utiliser un batch size multiple de 8** pour une meilleure efficacité GPU
2. **Activer le pinned memory** pour des transferts CPU→GPU plus rapides (déjà activé dans Ultralytics)
3. **Utiliser AMP (Automatic Mixed Precision)** pour réduire l'utilisation mémoire (activé par défaut dans YOLOv8)
4. **Fermer les autres applications GPU** pendant l'entraînement (navigateur, jeux, etc.)

## 📝 Committer les changements

```powershell
git add .
git commit -m "feat: ajout du support GPU pour l'entraînement"
git push origin gpu-support
```

Puis créer une Pull Request pour merger dans main.
