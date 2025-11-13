#!/bin/bash

# Script pour garder l'API Cloud Run active
# Usage: ./keep_alive.sh ou ajoutez-le en cron

API_URL="https://senchess-api-929629832495.us-central1.run.app/health"

echo "🔄 Keep-Alive Senchess API"
echo "Ping toutes les 5 minutes..."
echo ""

while true; do
    timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    response=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL")
    
    if [ "$response" = "200" ]; then
        echo "✅ [$timestamp] API active (HTTP $response)"
    else
        echo "⚠️  [$timestamp] API répond avec HTTP $response"
    fi
    
    sleep 300  # 5 minutes
done
