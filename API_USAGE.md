# 📚 Manuel d'Utilisation - Senchess AI API

## 🌐 URL de l'API
```
https://senchess-api-929629832495.us-central1.run.app
```

## 📋 Endpoints Disponibles

### 1. Health Check
Vérifiez l'état de l'API et des modèles chargés.

**Endpoint:** `GET /health`

**Exemple:**
```bash
curl https://senchess-api-929629832495.us-central1.run.app/health
```

**Réponse:**
```json
{
  "status": "healthy",
  "model_type": "ensemble",
  "use_huggingface": true,
  "repo_id": "MedouneSGB/senchess-models",
  "models_loaded": {
    "gear": true,
    "haki": true
  }
}
```

---

### 2. Prédiction
Analysez une image d'échiquier et obtenez la position FEN.

**Endpoint:** `POST /predict`

**Paramètres:**
- `image` (obligatoire): Fichier image (JPG, PNG)
- `model` (optionnel): Choix du modèle
  - `gear` - Modèle Gear v1.1 (98.5% mAP)
  - `haki` - Modèle Haki v1.0 (99.5% mAP)
  - `ensemble` - Combine les deux modèles (par défaut)

---

## 🚀 Exemples d'Utilisation

### Exemple 1: Prédiction avec Ensemble (Recommandé)
```bash
curl -X POST \
  -F "image=@chemin/vers/votre/image.jpg" \
  https://senchess-api-929629832495.us-central1.run.app/predict
```

### Exemple 2: Prédiction avec Modèle Gear
```bash
curl -X POST \
  -F "image=@chemin/vers/votre/image.jpg" \
  -F "model=gear" \
  https://senchess-api-929629832495.us-central1.run.app/predict
```

### Exemple 3: Prédiction avec Modèle Haki
```bash
curl -X POST \
  -F "image=@chemin/vers/votre/image.jpg" \
  -F "model=haki" \
  https://senchess-api-929629832495.us-central1.run.app/predict
```

---

## 📤 Réponse de l'API

### Structure de la Réponse
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

### Champs de la Réponse
- **success**: `true` si la prédiction a réussi
- **fen**: Notation FEN de la position détectée
- **model_used**: Modèle utilisé pour la prédiction
- **detectedPieces**: Nombre de pièces détectées
- **confidence**: Confiance moyenne (0-1)
- **description**: Description textuelle du résultat
- **imageSize**: Dimensions de l'image analysée
- **pieces**: Liste détaillée des pièces détectées
  - **id**: Identifiant unique de la pièce
  - **class**: Type de pièce (ex: "white-king", "black-pawn")
  - **confidence**: Confiance de détection (0-1)
  - **bbox**: Coordonnées de la boîte englobante
- **warnings**: Messages d'avertissement éventuels

---

## 💻 Exemples avec Différents Langages

### Python
```python
import requests

url = "https://senchess-api-929629832495.us-central1.run.app/predict"

# Avec le modèle ensemble
with open("chemin/vers/image.jpg", "rb") as f:
    files = {"image": f}
    data = {"model": "ensemble"}
    response = requests.post(url, files=files, data=data)
    result = response.json()
    
print(f"FEN: {result['fen']}")
print(f"Pièces détectées: {result['detectedPieces']}")
print(f"Confiance: {result['confidence']:.2%}")
```

### JavaScript (Node.js)
```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

const form = new FormData();
form.append('image', fs.createReadStream('chemin/vers/image.jpg'));
form.append('model', 'ensemble');

axios.post('https://senchess-api-929629832495.us-central1.run.app/predict', form, {
  headers: form.getHeaders()
})
.then(response => {
  console.log('FEN:', response.data.fen);
  console.log('Pièces détectées:', response.data.detectedPieces);
  console.log('Confiance:', response.data.confidence);
})
.catch(error => console.error('Erreur:', error));
```

### JavaScript (Fetch API - Browser)
```javascript
const formData = new FormData();
const fileInput = document.querySelector('input[type="file"]');
formData.append('image', fileInput.files[0]);
formData.append('model', 'ensemble');

fetch('https://senchess-api-929629832495.us-central1.run.app/predict', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => {
  console.log('FEN:', data.fen);
  console.log('Pièces détectées:', data.detectedPieces);
  document.getElementById('result').textContent = data.fen;
})
.catch(error => console.error('Erreur:', error));
```

### PHP
```php
<?php
$url = "https://senchess-api-929629832495.us-central1.run.app/predict";

$curl = curl_init();
$file = new CURLFile('chemin/vers/image.jpg', 'image/jpeg', 'image.jpg');

curl_setopt_array($curl, [
    CURLOPT_URL => $url,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => [
        'image' => $file,
        'model' => 'ensemble'
    ]
]);

$response = curl_exec($curl);
curl_close($curl);

$result = json_decode($response, true);
echo "FEN: " . $result['fen'] . "\n";
echo "Pièces détectées: " . $result['detectedPieces'] . "\n";
?>
```

---

## 🎯 Classes de Pièces Détectées

L'API peut détecter les 12 types de pièces suivants :

| Classe | Description |
|--------|-------------|
| `white-king` | Roi blanc ♔ |
| `white-queen` | Dame blanche ♕ |
| `white-rook` | Tour blanche ♖ |
| `white-bishop` | Fou blanc ♗ |
| `white-knight` | Cavalier blanc ♘ |
| `white-pawn` | Pion blanc ♙ |
| `black-king` | Roi noir ♚ |
| `black-queen` | Dame noire ♛ |
| `black-rook` | Tour noire ♜ |
| `black-bishop` | Fou noir ♝ |
| `black-knight` | Cavalier noir ♞ |
| `black-pawn` | Pion noir ♟ |

---

## 📊 Comparaison des Modèles

| Modèle | mAP | Spécialité | Recommandation |
|--------|-----|------------|----------------|
| **Gear v1.1** | 98.5% | Détection générale | Bon pour la plupart des cas |
| **Haki v1.0** | 99.5% | Pièces stratégiques | Meilleur pour positions complexes |
| **Ensemble** | - | Combine les deux | **Recommandé** - Meilleure précision |

---

## ⚠️ Limitations et Bonnes Pratiques

### Formats d'Image Supportés
- ✅ JPG/JPEG
- ✅ PNG
- ✅ WEBP
- ✅ BMP

### Recommandations
- **Résolution**: 416x416 pixels (optimale)
- **Taille max**: 10 MB
- **Qualité**: Image claire avec bon éclairage
- **Angle**: Vue de dessus de l'échiquier
- **Contraste**: Pièces bien visibles sur le plateau

### Gestion des Erreurs
```python
import requests

try:
    response = requests.post(url, files=files, data=data, timeout=60)
    response.raise_for_status()
    result = response.json()
    
    if not result.get('success'):
        print(f"Erreur: {result.get('error', 'Erreur inconnue')}")
    else:
        print(f"FEN: {result['fen']}")
        
except requests.exceptions.Timeout:
    print("Timeout: La requête a pris trop de temps")
except requests.exceptions.RequestException as e:
    print(f"Erreur de connexion: {e}")
```

---

## 🔧 Configuration Cloud Run

L'API est déployée sur Google Cloud Run avec :
- **Région**: us-central1
- **Mémoire**: 2 GB
- **CPU**: 2 vCPU
- **Timeout**: 300 secondes
- **Accès**: Public (sans authentification)

---

## 📞 Support

Pour toute question ou problème :
- **Repository**: https://github.com/MedouneSGB/Senchess-AI
- **Models**: https://huggingface.co/MedouneSGB/senchess-models

---

## 📝 Notes sur la Notation FEN

La notation FEN (Forsyth-Edwards Notation) retournée suit le format standard :
```
8/4r3/3Pp3/2K5/5k2/2P5/8/8 w KQkq - 0 1
```

Structure :
- `8/4r3/...`: Position des pièces (rang 8 à rang 1)
- `w`: Trait aux blancs (w) ou aux noirs (b)
- `KQkq`: Droits de roque
- `-`: Case en passant
- `0`: Nombre de demi-coups
- `1`: Numéro du coup

---

**Dernière mise à jour**: 10 novembre 2025
**Version de l'API**: 1.0
