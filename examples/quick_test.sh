#!/bin/bash

# Script de test simple pour l'API Senchess AI
# Usage: ./quick_test.sh [chemin/vers/image.jpg] [model]

API_URL="https://senchess-api-929629832495.us-central1.run.app"

# Couleurs pour l'affichage
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}     🎯 Senchess AI - Test Rapide              ${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Test 1: Health Check
echo -e "${YELLOW}📡 Test de connexion à l'API...${NC}"
health_response=$(curl -s "${API_URL}/health")

if echo "$health_response" | grep -q '"status":"healthy"'; then
    echo -e "${GREEN}✅ API opérationnelle !${NC}"
    echo "$health_response" | python3 -m json.tool
else
    echo -e "${RED}❌ API non disponible${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}------------------------------------------------${NC}"
echo ""

# Test 2: Prédiction
IMAGE_PATH="${1:-imgTest/capture2.jpg}"
MODEL="${2:-ensemble}"

if [ ! -f "$IMAGE_PATH" ]; then
    echo -e "${RED}❌ Erreur: Image '$IMAGE_PATH' introuvable${NC}"
    echo ""
    echo "Usage: $0 [chemin/image.jpg] [model]"
    echo "Modèles disponibles: gear, haki, ensemble"
    exit 1
fi

echo -e "${YELLOW}🖼️  Analyse de l'image: ${IMAGE_PATH}${NC}"
echo -e "${YELLOW}🤖 Modèle: ${MODEL}${NC}"
echo ""

# Envoyer la requête
response=$(curl -s -X POST \
    -F "image=@${IMAGE_PATH}" \
    -F "model=${MODEL}" \
    "${API_URL}/predict")

# Vérifier le succès
if echo "$response" | grep -q '"success":true'; then
    echo -e "${GREEN}✅ Analyse réussie !${NC}"
    echo ""
    
    # Extraire et afficher les informations clés
    fen=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin)['fen'])")
    pieces=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin)['detectedPieces'])")
    confidence=$(echo "$response" | python3 -c "import sys, json; print(f\"{json.load(sys.stdin)['confidence']*100:.1f}%\")")
    
    echo -e "${BLUE}📋 Résultats:${NC}"
    echo -e "  ${GREEN}FEN:${NC} ${fen}"
    echo -e "  ${GREEN}Pièces détectées:${NC} ${pieces}"
    echo -e "  ${GREEN}Confiance:${NC} ${confidence}"
    echo ""
    
    # Afficher le détail des pièces
    echo -e "${BLUE}🎯 Détail des pièces:${NC}"
    echo "$response" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for i, piece in enumerate(sorted(data['pieces'], key=lambda x: x['confidence'], reverse=True), 1):
    print(f\"  {i}. {piece['class']:15} - {piece['confidence']*100:.1f}%\")
"
    
    # Sauvegarder le résultat
    OUTPUT_FILE="last_prediction.json"
    echo "$response" | python3 -m json.tool > "$OUTPUT_FILE"
    echo ""
    echo -e "${GREEN}💾 Résultat sauvegardé dans: ${OUTPUT_FILE}${NC}"
    
else
    echo -e "${RED}❌ Erreur lors de l'analyse${NC}"
    echo "$response" | python3 -m json.tool
    exit 1
fi

echo ""
echo -e "${BLUE}================================================${NC}"
echo -e "${GREEN}✨ Test terminé avec succès !${NC}"
echo -e "${BLUE}================================================${NC}"
