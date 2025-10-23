#!/bin/bash
# Automated loop to upload all files in batches

echo "🚀 Starting automated batch upload..."
echo "This will run until all files are uploaded"
echo ""

COUNTER=1
MAX_RUNS=50  # Safety limit: max 50 batches (1000 files)

while [ $COUNTER -le $MAX_RUNS ]; do
    echo "======================================"
    echo "Batch Round #$COUNTER"
    echo "======================================"
    
    python3 batch_upload.py
    
    # Check if upload_progress.json shows we're done
    if [ -f upload_progress.json ]; then
        # Count remaining files
        REMAINING=$(find . -type f -name "*.py" -o -name "*.md" -o -name "*.json" | wc -l)
        
        echo ""
        echo "Waiting 2 seconds before next batch..."
        sleep 2
    fi
    
    COUNTER=$((COUNTER + 1))
done

echo ""
echo "🎉 Batch upload complete or max runs reached!"
echo "Check upload_progress.json for details"
