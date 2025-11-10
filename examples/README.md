# 📦 Exemples d'Utilisation - Senchess AI

Ce dossier contient tous les exemples pour utiliser votre API déployée.

## 📂 Fichiers Disponibles

### 1. `test_api.py` - Tests Automatisés Python
Script Python complet pour tester tous les aspects de l'API.

**Usage:**
```bash
python examples/test_api.py
```

**Ce qu'il fait:**
- ✅ Vérifie la connexion (health check)
- ✅ Test de prédiction avec chaque modèle
- ✅ Compare les performances (Gear vs Haki vs Ensemble)
- ✅ Teste la gestion des erreurs
- ✅ Sauvegarde les résultats en JSON

**Sortie attendue:**
```
🎯 TESTS DE L'API SENCHESS AI
============================================================
TEST 1: Health Check ...................... ✅ PASSED
TEST 2: Prédiction (ensemble) ............. ✅ PASSED
  9 pièces détectées - Confiance: 82.7%
TEST 3: Comparaison des modèles ........... ✅ PASSED
  gear: 7 pièces (93.5%)
  haki: 4 pièces (38.7%)
  ensemble: 9 pièces (82.7%)
============================================================
```

---

### 2. `web_interface.html` - Interface Web Interactive
Interface graphique complète pour tester l'API dans le navigateur.

**Usage:**
```bash
# Ouvrir dans le navigateur
open examples/web_interface.html
```

**Fonctionnalités:**
- 📸 Upload d'images par drag & drop
- 🎯 Sélection du modèle (Gear / Haki / Ensemble)
- 📊 Visualisation des résultats en temps réel
- 📋 Liste détaillée des pièces détectées
- 🎨 Interface moderne et responsive

**Aperçu:**
- Belle interface gradient violet
- Statistiques visuelles (pièces, confiance, modèle)
- Emojis pour chaque type de pièce (♔♕♖♗♘♙)

---

### 3. `quick_test.sh` - Script Bash Rapide
Script shell pour tester rapidement l'API depuis le terminal.

**Usage:**
```bash
# Test avec image par défaut
./examples/quick_test.sh

# Test avec votre propre image
./examples/quick_test.sh chemin/vers/image.jpg

# Test avec un modèle spécifique
./examples/quick_test.sh imgTest/capture2.jpg haki
```

**Sortie:**
```
🎯 Senchess AI - Test Rapide
📡 Test de connexion à l'API... ✅
🖼️  Analyse de l'image: imgTest/capture2.jpg
✅ Analyse réussie !
📋 FEN: 8/4r3/3Pp3/2K5/5k2/2P5/8/8 w KQkq - 0 1
🎯 9 pièces détectées - Confiance: 82.7%
```

---

## 🚀 Démarrage Rapide

### Option 1: Python (Recommandé pour développeurs)
```python
import requests

url = "https://senchess-api-929629832495.us-central1.run.app/predict"

with open("mon_image.jpg", "rb") as f:
    response = requests.post(url, files={"image": f})
    result = response.json()
    print(f"FEN: {result['fen']}")
```

### Option 2: cURL (Simple et rapide)
```bash
curl -X POST \
  -F "image=@mon_image.jpg" \
  -F "model=ensemble" \
  https://senchess-api-929629832495.us-central1.run.app/predict
```

### Option 3: Interface Web (Pour non-développeurs)
1. Ouvrir `examples/web_interface.html`
2. Cliquer sur "Choisir une image"
3. Voir les résultats instantanément !

---

## 📸 Images de Test

Le dossier `imgTest/` contient des images d'exemple :
- `capture.jpg` - Position simple
- `capture2.jpg` - Position avec 9 pièces (utilisé dans les tests)
- `capture3.jpg` - Position complexe

---

## 🎯 Comparaison des Modèles

| Modèle | Quand l'utiliser | Performance |
|--------|------------------|-------------|
| **ensemble** | Par défaut, meilleur résultat | 🥇 Recommandé |
| **gear** | Vitesse, détection générale | 🥈 Rapide |
| **haki** | Pièces stratégiques | 🥉 Précis |

---

## 💻 Exemples de Code

### Python avec Requests
```python
import requests

def analyze_chess_position(image_path, model="ensemble"):
    """Analyse une position d'échecs"""
    url = "https://senchess-api-929629832495.us-central1.run.app/predict"
    
    with open(image_path, "rb") as f:
        files = {"image": f}
        data = {"model": model}
        response = requests.post(url, files=files, data=data)
    
    return response.json()

# Utilisation
result = analyze_chess_position("mon_echiquier.jpg")
print(f"Position: {result['fen']}")
print(f"Pièces: {result['detectedPieces']}")
print(f"Confiance: {result['confidence']:.1%}")
```

### JavaScript (Fetch)
```javascript
async function analyzeChess(imageFile, model = 'ensemble') {
    const formData = new FormData();
    formData.append('image', imageFile);
    formData.append('model', model);
    
    const response = await fetch(
        'https://senchess-api-929629832495.us-central1.run.app/predict',
        { method: 'POST', body: formData }
    );
    
    return await response.json();
}

// Utilisation
const file = document.querySelector('input[type="file"]').files[0];
const result = await analyzeChess(file, 'ensemble');
console.log('FEN:', result.fen);
```

### Node.js avec Axios
```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

async function analyzeChess(imagePath, model = 'ensemble') {
    const form = new FormData();
    form.append('image', fs.createReadStream(imagePath));
    form.append('model', model);
    
    const response = await axios.post(
        'https://senchess-api-929629832495.us-central1.run.app/predict',
        form,
        { headers: form.getHeaders() }
    );
    
    return response.data;
}

// Utilisation
analyzeChess('mon_image.jpg')
    .then(result => console.log('FEN:', result.fen));
```

### PHP
```php
<?php
function analyzeChess($imagePath, $model = 'ensemble') {
    $url = "https://senchess-api-929629832495.us-central1.run.app/predict";
    
    $file = new CURLFile($imagePath, 'image/jpeg', 'image.jpg');
    
    $ch = curl_init();
    curl_setopt_array($ch, [
        CURLOPT_URL => $url,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => [
            'image' => $file,
            'model' => $model
        ]
    ]);
    
    $response = curl_exec($ch);
    curl_close($ch);
    
    return json_decode($response, true);
}

// Utilisation
$result = analyzeChess('mon_image.jpg');
echo "FEN: " . $result['fen'];
?>
```

---

## 🧪 Tests Avancés

### Test de Charge
```python
import concurrent.futures
import requests

def test_concurrent_requests(n_requests=10):
    """Teste n requêtes simultanées"""
    url = "https://senchess-api-929629832495.us-central1.run.app/predict"
    
    def send_request(i):
        with open("imgTest/capture2.jpg", "rb") as f:
            response = requests.post(url, files={"image": f})
        return response.status_code
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(send_request, range(n_requests)))
    
    success = sum(1 for r in results if r == 200)
    print(f"✅ {success}/{n_requests} requêtes réussies")

test_concurrent_requests(10)
```

### Test de Performance
```python
import time
import requests

def measure_performance():
    """Mesure le temps de réponse"""
    url = "https://senchess-api-929629832495.us-central1.run.app/predict"
    
    start = time.time()
    with open("imgTest/capture2.jpg", "rb") as f:
        response = requests.post(url, files={"image": f})
    elapsed = time.time() - start
    
    print(f"⏱️  Temps de réponse: {elapsed:.2f}s")
    return elapsed

# Test sur 5 requêtes
times = [measure_performance() for _ in range(5)]
print(f"📊 Temps moyen: {sum(times)/len(times):.2f}s")
```

---

## 📊 Format de Réponse Détaillé

```json
{
  "success": true,
  "fen": "8/4r3/3Pp3/2K5/5k2/2P5/8/8 w KQkq - 0 1",
  "model_used": "ensemble",
  "detectedPieces": 9,
  "confidence": 0.827,
  "description": "Position détectée avec 9 pièces",
  "imageSize": {
    "width": 416,
    "height": 416
  },
  "pieces": [
    {
      "id": 1,
      "class": "black-rook",
      "confidence": 0.926,
      "bbox": {
        "x1": 198.5,
        "y1": 49.23,
        "x2": 223.16,
        "y2": 102.91,
        "width": 24.66,
        "height": 53.69
      }
    }
    // ... autres pièces
  ],
  "warnings": []
}
```

**Champs importants:**
- `fen`: Position en notation Forsyth-Edwards
- `detectedPieces`: Nombre total de pièces
- `confidence`: Score de confiance moyen (0-1)
- `pieces`: Liste détaillée avec coordonnées

---

## ⚠️ Gestion des Erreurs

### Erreur 400 - Bad Request
```json
{
  "error": "No image file provided"
}
```
**Solution:** Vérifier que le fichier est bien envoyé avec la clé "image"

### Erreur 503 - Service Unavailable
**Cause:** Les modèles sont en cours de chargement (première requête)
**Solution:** Attendre 15-20 secondes et réessayer

### Timeout
```python
try:
    response = requests.post(url, files=files, timeout=60)
except requests.exceptions.Timeout:
    print("Timeout - Réessayer")
```

---

## 🔗 Ressources

- **API URL**: https://senchess-api-929629832495.us-central1.run.app
- **Health Check**: https://senchess-api-929629832495.us-central1.run.app/health
- **Documentation complète**: Voir `API_USAGE.md`
- **Modèles**: https://huggingface.co/MedouneSGB/senchess-models

---

## 🎓 Tutoriel Pas à Pas

### 1. Test de Base
```bash
# Vérifier que l'API fonctionne
curl https://senchess-api-929629832495.us-central1.run.app/health
```

### 2. Première Prédiction
```bash
# Analyser une image
curl -X POST \
  -F "image=@imgTest/capture2.jpg" \
  https://senchess-api-929629832495.us-central1.run.app/predict
```

### 3. Comparer les Modèles
```bash
# Tester Gear
curl -X POST -F "image=@imgTest/capture2.jpg" -F "model=gear" \
  https://senchess-api-929629832495.us-central1.run.app/predict

# Tester Haki
curl -X POST -F "image=@imgTest/capture2.jpg" -F "model=haki" \
  https://senchess-api-929629832495.us-central1.run.app/predict
```

### 4. Intégrer dans Votre Code
Voir les exemples Python/JavaScript ci-dessus.

---

## 🎉 Prêt à Utiliser !

Choisissez l'exemple qui vous convient le mieux :
- 🐍 Python → `test_api.py`
- 🌐 Web → `web_interface.html`
- 💻 Terminal → `quick_test.sh`

**Besoin d'aide ?** Consultez `API_USAGE.md` pour la documentation complète !
