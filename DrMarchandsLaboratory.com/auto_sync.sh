#!/bin/bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📡 [WATCHTOWER] Online. Monitoring configured Git repository..."
echo "Node will check for repository updates every 60 seconds."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

while true; do
    OUTPUT=$(git pull origin main 2>&1)

    if [[ $OUTPUT != *"Already up to date."* ]]; then
        echo ""
        echo "🔄 [SYNC INCOMING] Repository source changed:"
        echo "$OUTPUT"
        echo "⚙️  Review and restart the Engine runtime if the changed files require it."
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    fi

    sleep 60
done
