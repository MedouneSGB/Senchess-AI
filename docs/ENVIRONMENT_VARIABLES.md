# 🔐 Configuration des Variables d'Environnement

## 📋 Pour l'API en local ou sur Vercel

### 1️⃣ Créer le fichier `.env.local`

```bash
cp .env.example .env.local
```

### 2️⃣ Obtenir votre Token Hugging Face

1. Allez sur https://huggingface.co/settings/tokens
2. Créez un nouveau token (lecture seule suffit)
3. Copiez le token

### 3️⃣ Modifier `.env.local`

```bash
# Votre token HuggingFace
HF_TOKEN=hf_VotreTokEnIci

# Votre repo (si différent)
HUGGINGFACE_REPO_ID=MedouneSGB/senchess-models

# Type de modèle
MODEL_TYPE=ensemble
```

### 4️⃣ Sur Vercel (Production)

Dans les **Environment Variables** du projet Vercel :
- `HF_TOKEN` = votre token HuggingFace
- `HUGGINGFACE_REPO_ID` = MedouneSGB/senchess-models
- `MODEL_TYPE` = ensemble

---

## 📓 Pour Google Colab (Entraînement)

Dans votre notebook Colab, remplacez :

```python
# Cellule 2 : ID de votre dataset sur Google Drive
DRIVE_FILE_ID = "VOTRE_ID_ICI"

# Cellule 8 : Votre token HuggingFace
HF_TOKEN = "VOTRE_TOKEN_HF_ICI"
```

### Comment obtenir l'ID Google Drive ?

1. Clic droit sur votre fichier ZIP → **Partager**
2. **Modifier** → **Toute personne avec le lien**
3. Copiez le lien : `https://drive.google.com/file/d/`**`1ABC...XYZ`**`/view`
4. **L'ID est la partie entre `/d/` et `/view`**

---

## 🔒 Sécurité

✅ **Fichiers ignorés par Git** (déjà dans `.gitignore`) :
- `.env.local`
- `.env`
- `.env.production`

❌ **Ne jamais commiter** :
- Tokens HuggingFace
- IDs Google Drive
- Clés API

✅ **Utiliser** :
- `.env.local` pour les secrets locaux
- Variables d'environnement Vercel pour la production
- Variables dans Colab pour l'entraînement

---

## 📚 Référence

| Variable | Description | Exemple |
|----------|-------------|---------|
| `HF_TOKEN` | Token HuggingFace | `hf_abc123...` |
| `HUGGINGFACE_REPO_ID` | Repository des modèles | `user/repo` |
| `MODEL_TYPE` | Type de modèle | `ensemble` |
| `DRIVE_FILE_ID` | ID fichier Google Drive | `1ABC...XYZ` |
