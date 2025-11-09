#!/bin/bash

# Script de test rapide pour l'API Senchess
# Teste localement avant le déploiement

echo "🧪 Test de l'API Senchess"
echo "========================="
echo ""

# Couleurs pour l'output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# URL de l'API (changez si nécessaire)
API_URL="${1:-http://localhost:5000}"

echo "📍 API URL: $API_URL"
echo ""

# Test 1: Health check
echo "1️⃣  Test du health check..."
HEALTH=$(curl -s "$API_URL/health")

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ API accessible${NC}"
    echo "$HEALTH" | python3 -m json.tool 2>/dev/null || echo "$HEALTH"
else
    echo -e "${RED}❌ API non accessible${NC}"
    echo "Assurez-vous que l'API est lancée : cd api && python index.py"
    exit 1
fi

echo ""

# Test 2: Vérifier qu'une image de test existe
echo "2️⃣  Recherche d'une image de test..."
TEST_IMAGE=""

for img in imgTest/capture.jpg imgTest/capture2.jpg imgTest/capture3.jpg; do
    if [ -f "$img" ]; then
        TEST_IMAGE="$img"
        echo -e "${GREEN}✅ Image trouvée: $img${NC}"
        break
    fi
done

if [ -z "$TEST_IMAGE" ]; then
    echo -e "${YELLOW}⚠️  Aucune image de test trouvée${NC}"
    echo "Placez une image d'échiquier dans imgTest/capture.jpg"
    exit 0
fi

echo ""

# Test 3: Prédiction
echo "3️⃣  Test de prédiction..."
RESPONSE=$(curl -s -X POST "$API_URL/predict" \
    -F "image=@$TEST_IMAGE" \
    -F "conf=0.25" \
    -F "model=ensemble")

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Prédiction réussie${NC}"
    echo ""
    
    # Extraire les informations importantes
    echo "📊 Résultats:"
    echo "$RESPONSE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(f'  FEN: {data.get(\"fen\", \"N/A\")}')
    print(f'  Pièces détectées: {data.get(\"detectedPieces\", 0)}')
    print(f'  Confiance: {data.get(\"confidence\", 0):.3f}')
    print(f'  Modèle utilisé: {data.get(\"model_used\", \"N/A\")}')
    if data.get('warnings'):
        print(f'  Avertissements: {data[\"warnings\"]}')
except:
    print('  Erreur lors du parsing JSON')
    print(sys.stdin.read())
"
else
    echo -e "${RED}❌ Erreur lors de la prédiction${NC}"
    echo "$RESPONSE"
fi

echo ""
echo "=============================="
echo -e "${GREEN}🎉 Tests terminés !${NC}"
