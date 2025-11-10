# 🚀 Senchess AI - API Déployée

## ✅ Déploiement Réussi !

Votre API de détection de pièces d'échecs est maintenant **déployée et opérationnelle** sur Google Cloud Run !

### 🌐 URL de l'API
```
https://senchess-api-929629832495.us-central1.run.app
```

---

## 📚 Documentation

### Fichiers de Documentation Créés

1. **`API_USAGE.md`** - Manuel complet d'utilisation
   - Tous les endpoints disponibles
   - Exemples dans plusieurs langages (Python, JavaScript, PHP)
   - Format des réponses
   - Gestion des erreurs

2. **`examples/test_api.py`** - Script de test Python
   - Tests automatisés de tous les endpoints
   - Comparaison des 3 modèles
   - Sauvegarde des résultats en JSON

3. **`examples/web_interface.html`** - Interface web interactive
   - Upload d'images par drag & drop
   - Sélection du modèle (Gear, Haki, Ensemble)
   - Visualisation des résultats en temps réel

---

## 🎯 Test Rapide

### Test 1: Health Check
```bash
curl https://senchess-api-929629832495.us-central1.run.app/health
```

**Résultat attendu:**
```json
{
  "status": "healthy",
  "model_type": "ensemble",
  "models_loaded": {
    "gear": true,
    "haki": true
  }
}
```

### Test 2: Prédiction
```bash
curl -X POST \
  -F "image=@imgTest/capture2.jpg" \
  -F "model=ensemble" \
  https://senchess-api-929629832495.us-central1.run.app/predict
```

**Résultat attendu:**
```json
{
  "success": true,
  "fen": "8/4r3/3Pp3/2K5/5k2/2P5/8/8 w KQkq - 0 1",
  "model_used": "ensemble",
  "detectedPieces": 9,
  "confidence": 0.827,
  "pieces": [...]
}
```

---

## 🎨 Interface Web

Ouvrez le fichier `examples/web_interface.html` dans votre navigateur pour une interface graphique complète !

**Fonctionnalités:**
- ✅ Upload d'images
- ✅ Choix du modèle (Gear / Haki / Ensemble)
- ✅ Visualisation de la notation FEN
- ✅ Liste détaillée des pièces détectées
- ✅ Statistiques de confiance

---

## 🧪 Tests Automatisés

Lancez la suite de tests complète :

```bash
python examples/test_api.py
```

**Ce script teste:**
1. ✅ Connectivité de l'API
2. ✅ Prédiction avec chaque modèle
3. ✅ Comparaison des performances
4. ✅ Gestion des erreurs
5. ✅ Sauvegarde des résultats

**Résultats des tests:**
```
TEST 1: Health Check ..................... ✅ PASSED
TEST 2: Prédiction (ensemble) ............ ✅ PASSED (9 pièces, 82.7%)
TEST 3: Comparaison des modèles .......... ✅ PASSED
  - Gear: 7 pièces (93.5%)
  - Haki: 4 pièces (38.7%)
  - Ensemble: 9 pièces (82.7%)
TEST 4: Gestion des erreurs .............. ✅ PASSED
TEST 5: Sauvegarde JSON .................. ✅ PASSED
```

---

## 🔧 Modèles Disponibles

| Modèle | Performance | Spécialité | Usage |
|--------|-------------|------------|-------|
| **Gear v1.1** | 98.5% mAP | Détection générale | Bon équilibre vitesse/précision |
| **Haki v1.0** | 99.5% mAP | Pièces stratégiques | Positions complexes |
| **Ensemble** | Meilleur | Combine les deux | **Recommandé** |

---

## 💡 Exemples d'Intégration

### Python
```python
import requests

url = "https://senchess-api-929629832495.us-central1.run.app/predict"

with open("mon_echiquier.jpg", "rb") as f:
    files = {"image": f}
    data = {"model": "ensemble"}
    response = requests.post(url, files=files, data=data)
    result = response.json()
    
print(f"Position FEN: {result['fen']}")
```

### JavaScript (Fetch)
```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]);
formData.append('model', 'ensemble');

fetch('https://senchess-api-929629832495.us-central1.run.app/predict', {
    method: 'POST',
    body: formData
})
.then(res => res.json())
.then(data => console.log('FEN:', data.fen));
```

### cURL
```bash
curl -X POST \
  -F "image=@chemin/image.jpg" \
  -F "model=ensemble" \
  https://senchess-api-929629832495.us-central1.run.app/predict
```

---

## 📊 Performances

### Configuration Cloud Run
- **Région**: us-central1 (USA)
- **Mémoire**: 2 GB
- **CPU**: 2 vCPU
- **Timeout**: 300 secondes
- **Coût**: Gratuit jusqu'à 2M requêtes/mois

### Temps de Réponse
- Health check: ~100ms
- Prédiction (première requête): ~10-15s (chargement modèles)
- Prédiction (suivantes): ~2-3s

### Limites
- Taille max image: 10 MB
- Formats supportés: JPG, PNG, WEBP, BMP
- Résolution optimale: 416x416 pixels

---

## 🔐 Sécurité

- ✅ API publique sans authentification (pour l'instant)
- ✅ HTTPS par défaut
- ✅ CORS activé pour les applications web
- ✅ Rate limiting géré par Google Cloud Run

---

## 📈 Monitoring

### Voir les logs en temps réel
```bash
gcloud run services logs read senchess-api \
  --project=senchess-ai \
  --region=us-central1 \
  --limit=50
```

### Statistiques d'utilisation
Consultez la [Console Google Cloud](https://console.cloud.google.com/run/detail/us-central1/senchess-api) pour:
- Nombre de requêtes
- Temps de réponse moyen
- Erreurs
- Coûts

---

## 🛠️ Mise à Jour de l'API

Pour déployer une nouvelle version :

```bash
cd /Users/macbookair/Desktop/Senchess\ AI

# Modifier le code dans api/index.py

# Redéployer
gcloud run deploy senchess-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300
```

---

## 🎓 Ressources

- **Code source**: `/Users/macbookair/Desktop/Senchess AI/api/index.py`
- **Modèles**: https://huggingface.co/MedouneSGB/senchess-models
- **Documentation YOLO**: https://docs.ultralytics.com/
- **Cloud Run Docs**: https://cloud.google.com/run/docs

---

## 🐛 Dépannage

### L'API ne répond pas
```bash
# Vérifier le statut
gcloud run services describe senchess-api --region=us-central1

# Voir les logs d'erreur
gcloud run services logs read senchess-api --limit=20
```

### Erreur 503 Service Unavailable
- Les modèles sont en train de se charger (première requête)
- Attendre 15-20 secondes et réessayer

### Erreur 400 Bad Request
- Vérifier que l'image est bien envoyée
- Vérifier le format de l'image (JPG, PNG)
- Vérifier que le paramètre 'model' est valide

---

## 📞 Support

Pour toute question :
- GitHub: https://github.com/MedouneSGB/Senchess-AI
- Issues: https://github.com/MedouneSGB/Senchess-AI/issues

---

## 🎉 Félicitations !

Votre API est maintenant en ligne et prête à être utilisée dans vos projets !

**Prochaines étapes possibles:**
1. Intégrer l'API dans une application mobile
2. Créer un bot Discord/Telegram pour analyser des parties
3. Développer une extension Chrome pour analyser des positions en ligne
4. Ajouter l'authentification pour un usage privé
5. Optimiser les modèles pour réduire les temps de réponse

---

**Dernière mise à jour**: 10 novembre 2025
**Version**: 1.0
**Status**: 🟢 En ligne et opérationnel
