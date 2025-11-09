# 🚀 Lien direct pour Google Colab

## Ouvrir le notebook dans Colab

Cliquez sur ce lien pour ouvrir directement le notebook dans Google Colab :

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MedouneSGB/Senchess-AI/blob/gpu-cloud-training/notebooks/train_on_colab.ipynb)

## OU

1. Allez sur : https://colab.research.google.com/
2. Cliquez sur `GitHub`
3. Entrez : `MedouneSGB/Senchess-AI`
4. Sélectionnez la branche : `gpu-cloud-training`
5. Ouvrez : `notebooks/train_on_colab.ipynb`

## Après ouverture dans Colab

### ⚠️ IMPORTANT : Activer le GPU

Une fois dans Colab, vous verrez le menu en haut :

```
File  Edit  View  Insert  Runtime  Tools  Help
              👆
```

**Étapes :**
1. Cliquez sur `Runtime` (dans le menu du haut)
2. Sélectionnez `Change runtime type`
3. Dans la popup :
   - Hardware accelerator : **GPU**
   - GPU type : **T4 GPU** (gratuit)
4. Cliquez `Save`
5. Vous verrez une icône GPU apparaître en haut à droite ✅

### Vérifier que le GPU est activé

Exécutez la première cellule de code :
```python
!nvidia-smi
```

Vous devriez voir les informations du GPU Tesla T4.

---

## 💡 Différence VS Code vs Colab

| Où ? | Quoi ? | GPU ? |
|------|--------|-------|
| **VS Code (Local)** | Éditer le notebook | ❌ Votre CPU local |
| **Google Colab** | Exécuter avec GPU | ✅ GPU Tesla T4 gratuit |

---

## 📤 Comment envoyer le notebook sur GitHub (pour le lien Colab)

```powershell
# Dans votre terminal PowerShell
cd C:\Users\MSGB\Downloads\Senchess-AI-main

# Ajouter les fichiers
git add notebooks/train_on_colab.ipynb docs/GPU_CLOUD_GUIDE.md

# Commit
git commit -m "Add GPU cloud training notebook"

# Push vers la branche
git push origin gpu-cloud-training
```

Ensuite, le lien Colab fonctionnera directement !

---

## 🎥 Guide visuel rapide

### Dans Google Colab, vous verrez :

```
┌─────────────────────────────────────────────────┐
│ File Edit View Insert [Runtime] Tools Help     │ ← Menu ici
├─────────────────────────────────────────────────┤
│                                    🔌 GPU (T4)  │ ← Icône GPU
├─────────────────────────────────────────────────┤
│  # 🎯 Entraînement Senchess-AI...               │
│                                                  │
│  [ ▶️ ] # Vérifier le GPU disponible           │
│         !nvidia-smi                             │
└─────────────────────────────────────────────────┘
```

Le bouton ▶️ permet d'exécuter chaque cellule.
