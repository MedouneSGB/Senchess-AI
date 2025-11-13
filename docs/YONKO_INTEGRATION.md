# Intégration du Modèle Yonko v1.0

## 📅 Date d'intégration
13 Novembre 2025

## 🌊 À propos de Yonko v1.0

### Caractéristiques
- **Architecture**: YOLOv8n (nano)
- **Dataset**: 10,000+ images avec augmentation de données extensive
- **Classes**: 12 classes (toutes les pièces d'échecs)
- **Augmentation**: Rotation, flip, luminosité, contraste, et plus
- **Epochs**: 20+

### Performances
- ✅ Test local réussi: 41 pièces détectées
- ✅ Confiance moyenne: 75.69%
- ✅ Poids du modèle: 6.0 MB

## 📦 Déploiement

### 1. Structure locale
```
models/senchess_yonko_v1.0/
├── weights/
│   └── best.pt (6.0 MB)
├── args.yaml
├── results.csv
└── README.md
```

### 2. Hugging Face Hub
- **Repository**: `MedouneSGB/senchess-models`
- **Fichier**: `yonko_v1.0.pt`
- **URL**: https://huggingface.co/MedouneSGB/senchess-models
- **Statut**: ✅ Uploadé avec succès

### 3. API (api/index.py)
Modifications effectuées:
- ✅ Ajout de la variable globale `model_yonko`
- ✅ Fonction `load_model()` mise à jour pour charger Yonko
- ✅ Support du paramètre `model=yonko` dans `/predict`
- ✅ Endpoint `/health` mis à jour pour afficher le statut de Yonko
- ✅ Logique de fallback pour utiliser Yonko si disponible

### 4. Interface Web (examples/web_interface.html)
Modifications effectuées:
- ✅ Ajout du bouton "🌊 Yonko v1.0"
- ✅ Support de l'emoji et du nom dans les résultats
- ✅ Ordre des modèles: Haki → Gear → Yonko → Ensemble
- ✅ Rechargement automatique lors du changement de modèle

## 🚀 Utilisation

### Via l'interface web
1. Ouvrir `examples/web_interface.html`
2. Sélectionner "🌊 Yonko v1.0"
3. Télécharger une image
4. Comparer avec les autres modèles en un clic

### Via l'API
```bash
curl -X POST https://senchess-api-929629832495.us-central1.run.app/predict \
  -F "image=@chess_board.jpg" \
  -F "model=yonko" \
  -F "conf=0.25"
```

### En Python
```python
import requests

response = requests.post(
    'https://senchess-api-929629832495.us-central1.run.app/predict',
    files={'image': open('chess_board.jpg', 'rb')},
    data={'model': 'yonko', 'conf': 0.25}
)

data = response.json()
print(f"FEN: {data['fen']}")
print(f"Pièces détectées: {data['detectedPieces']}")
print(f"Confiance: {data['confidence']:.2%}")
```

### En local
```python
from ultralytics import YOLO

model = YOLO('models/senchess_yonko_v1.0/weights/best.pt')
results = model.predict('chess_board.jpg', conf=0.25)
```

## 📊 Comparaison des Modèles

| Modèle | Dataset | Spécialisation | Poids | Recommandé pour |
|--------|---------|----------------|-------|-----------------|
| **Haki v1.0** | Standard | Pièces stratégiques (K,Q,R,B) | 6 MB | Précision sur pièces importantes |
| **Gear v1.1** | Standard | Toutes les pièces | 6 MB | Détection équilibrée |
| **Yonko v1.0** | 10k+ images | Toutes les pièces | 6 MB | Robustesse et variété |
| **Ensemble** | - | Gear + Haki | - | Précision maximale |

## ✅ Checklist d'intégration

- [x] Extraction du modèle depuis le ZIP
- [x] Organisation dans `models/senchess_yonko_v1.0/`
- [x] Upload sur Hugging Face Hub
- [x] Mise à jour de l'API (`api/index.py`)
- [x] Mise à jour de l'interface web (`examples/web_interface.html`)
- [x] Création du README du modèle
- [x] Test local réussi
- [x] Documentation de l'intégration

## 🔄 Prochaines étapes

### Pour déployer sur Cloud Run:
1. Redéployer l'API avec le code mis à jour
2. Le modèle sera automatiquement téléchargé depuis Hugging Face
3. Vérifier avec `/health` que le modèle est chargé

### Commandes de déploiement:
```bash
# Construire l'image Docker
docker build -t senchess-api .

# Tagger pour Cloud Run
docker tag senchess-api gcr.io/[PROJECT-ID]/senchess-api

# Pousser vers Google Container Registry
docker push gcr.io/[PROJECT-ID]/senchess-api

# Déployer sur Cloud Run
gcloud run deploy senchess-api \
  --image gcr.io/[PROJECT-ID]/senchess-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars HUGGINGFACE_REPO_ID=MedouneSGB/senchess-models,MODEL_TYPE=ensemble,USE_HUGGINGFACE=true
```

## 📝 Notes
- Le modèle Yonko apporte une diversité supplémentaire grâce à son entraînement sur un dataset étendu avec augmentation
- Les 4 modèles (Haki, Gear, Yonko, Ensemble) offrent maintenant un choix complet pour différents besoins
- L'interface web permet de comparer facilement les résultats entre les modèles

## 🎉 Succès !
Le modèle Yonko v1.0 est maintenant complètement intégré dans le projet Senchess AI !
