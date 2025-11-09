# Guide d'utilisation des GPU Cloud pour Senchess-AI

## 🎯 Pourquoi utiliser un GPU cloud ?

- **Vitesse** : Entraînement 10-100x plus rapide qu'un CPU
- **Coût** : Pas besoin d'acheter un GPU (1000-3000€)
- **Flexibilité** : Utilisez seulement quand vous en avez besoin

---

## 🚀 Option 1 : Google Colab (RECOMMANDÉ)

### Avantages
- ✅ **Gratuit** (avec limitations)
- ✅ Facile à utiliser
- ✅ Aucune installation locale
- ✅ GPU Tesla T4 gratuit

### Limitations
- ⏱️ Sessions limitées à 12h
- 🔄 Déconnexion si inactif
- 💾 Stockage temporaire

### Comment démarrer

1. **Ouvrez le notebook**
   - Allez sur [Google Colab](https://colab.research.google.com/)
   - Uploadez `notebooks/train_on_colab.ipynb`

2. **Activez le GPU**
   ```
   Runtime → Change runtime type → GPU → T4 GPU → Save
   ```

3. **Vérifiez le GPU**
   ```python
   !nvidia-smi
   ```

4. **Entraînez votre modèle**
   - Suivez les cellules du notebook

### Colab Pro (Optionnel)
- **Prix** : ~10€/mois
- **Avantages** :
  - Sessions plus longues (24h)
  - GPU plus puissants (V100, A100)
  - Plus de RAM
  - Priorité d'accès

---

## 🏆 Option 2 : Kaggle (Alternative gratuite)

### Avantages
- ✅ **30h GPU/semaine gratuit**
- ✅ Pas de carte de crédit requise
- ✅ GPU T4 ou P100

### Comment démarrer

1. **Créez un compte** sur [Kaggle](https://www.kaggle.com/)

2. **Créez un nouveau Notebook**
   - New Notebook → Settings → Accelerator → GPU T4 x2

3. **Uploadez vos données**
   ```python
   # Créez un dataset sur Kaggle ou uploadez
   !pip install ultralytics
   ```

4. **Entraînez**
   ```python
   from ultralytics import YOLO
   model = YOLO('yolov8n.pt')
   model.train(data='data.yaml', epochs=100, device=0)
   ```

---

## 💰 Option 3 : AWS SageMaker / EC2

### Pour qui ?
- Production
- Projets professionnels
- Besoin de GPU puissants longtemps

### Instances recommandées
- **g4dn.xlarge** : ~0.50€/h (T4 GPU) - Bon pour débuter
- **p3.2xlarge** : ~3€/h (V100 GPU) - Très puissant
- **g5.xlarge** : ~1€/h (A10G GPU) - Bon rapport qualité/prix

### Setup rapide

1. **Créez un compte AWS**
2. **Lancez une instance EC2**
   - Choisissez Deep Learning AMI (Ubuntu)
   - Type : g4dn.xlarge
   - Configure security group (ouvrir port 8888 pour Jupyter)

3. **Connectez-vous**
   ```bash
   ssh -i your-key.pem ubuntu@ec2-instance-ip
   ```

4. **Installez les dépendances**
   ```bash
   source activate pytorch
   pip install ultralytics
   git clone https://github.com/MedouneSGB/Senchess-AI.git
   cd Senchess-AI
   ```

5. **Entraînez**
   ```bash
   python train_ultimate.py
   ```

---

## ☁️ Option 4 : Azure ML

### Pour qui ?
- Entreprises avec Azure
- Intégration avec autres services Microsoft

### GPU disponibles
- **NC6** : ~1€/h (K80)
- **NC6s_v3** : ~2.5€/h (V100)

### Setup
1. Créez un workspace Azure ML
2. Créez une compute instance avec GPU
3. Uploadez votre code
4. Lancez l'entraînement

---

## 🎨 Option 5 : Paperspace Gradient

### Avantages
- Interface simple
- GPU gratuit limité
- Plans abordables

### Prix
- **Free** : GPU M4000 (8GB VRAM) - limité
- **Pro** : ~8€/mois + GPU à l'heure
- **GPU P4000** : ~0.45€/h

### Comment démarrer
1. [Créez un compte](https://www.paperspace.com/)
2. Créez un Notebook → Select GPU
3. Uploadez votre code
4. Entraînez

---

## 📊 Comparaison rapide

| Plateforme | Prix | GPU | Facilité | Limite temps |
|------------|------|-----|----------|--------------|
| **Colab Free** | Gratuit | T4 | ⭐⭐⭐⭐⭐ | 12h |
| **Colab Pro** | ~10€/mois | V100/A100 | ⭐⭐⭐⭐⭐ | 24h |
| **Kaggle** | Gratuit | T4/P100 | ⭐⭐⭐⭐⭐ | 30h/semaine |
| **AWS EC2** | ~0.5-3€/h | T4-V100 | ⭐⭐⭐ | Illimité |
| **Azure ML** | ~1-3€/h | K80-V100 | ⭐⭐⭐ | Illimité |
| **Paperspace** | ~0.45€/h | M4000-A100 | ⭐⭐⭐⭐ | Selon plan |

---

## 🎓 Recommandations selon votre cas

### Débutant / Étudiant
→ **Google Colab Free** ou **Kaggle**
- Gratuit
- Simple
- Suffisant pour apprendre

### Projet sérieux
→ **Colab Pro** ou **Paperspace**
- Bon rapport qualité/prix
- Fiable
- GPU décents

### Production / Entreprise
→ **AWS** ou **Azure**
- Puissant
- Scalable
- Support professionnel

---

## 💡 Conseils pour optimiser les coûts

1. **Surveillez vos sessions**
   - Arrêtez les instances quand vous ne les utilisez pas

2. **Utilisez Spot Instances** (AWS/Azure)
   - 70% moins cher
   - Peut être interrompu

3. **Batch training**
   - Entraînez plusieurs modèles d'affilée
   - Maximisez l'utilisation

4. **Compressez vos datasets**
   - Upload/Download plus rapide
   - Économie de stockage

5. **Utilisez les crédits gratuits**
   - AWS : 300$ de crédits (12 mois)
   - Azure : 200$ de crédits (30 jours)
   - GCP : 300$ de crédits (90 jours)

---

## 🔧 Troubleshooting

### Colab se déconnecte ?
```python
# Gardez la session active
import time
while True:
    print(".", end="")
    time.sleep(60)
```

### Out of Memory (OOM) ?
- Réduisez `batch_size` dans l'entraînement
- Utilisez un modèle plus petit (yolov8n au lieu de yolov8x)

### Dataset trop gros pour upload ?
- Compressez en .zip
- Utilisez Google Drive + Colab
- Utilisez AWS S3 / Azure Blob

---

## 📝 Script de monitoring des coûts (AWS)

```python
import boto3
from datetime import datetime, timedelta

def check_costs():
    client = boto3.client('ce', region_name='us-east-1')
    
    end = datetime.now().date()
    start = end - timedelta(days=7)
    
    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': str(start),
            'End': str(end)
        },
        Granularity='DAILY',
        Metrics=['UnblendedCost']
    )
    
    for result in response['ResultsByTime']:
        print(f"{result['TimePeriod']['Start']}: ${result['Total']['UnblendedCost']['Amount']}")

check_costs()
```

---

## 📚 Ressources supplémentaires

- [Ultralytics YOLOv8 Docs](https://docs.ultralytics.com/)
- [Google Colab Guide](https://colab.research.google.com/notebooks/intro.ipynb)
- [AWS EC2 Pricing](https://aws.amazon.com/ec2/pricing/)
- [Azure ML Pricing](https://azure.microsoft.com/pricing/details/machine-learning/)

---

## 🤝 Support

Si vous avez des questions :
1. Ouvrez une issue sur GitHub
2. Consultez la documentation
3. Rejoignez notre communauté Discord (si disponible)

Bon entraînement ! 🚀
