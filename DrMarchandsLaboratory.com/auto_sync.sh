#!/bin/bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📡 [WATCHTOWER] Online. Monitoring GitHub..."
echo "Node will automatically update every 60 seconds."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

while true; do
    OUTPUT=$(git pull origin main 2>&1)
    
    if [[ $OUTPUT != *"Already up to date."* ]]; then
        echo ""
        echo "🔄 [SYNC INCOMING] Architecture updated from Sovereign Truth:"
        echo "$OUTPUT"
        echo "⚙️  Restart your Engine (engine_core.py) if core files changed."
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    fi
    
    sleep 60
done
