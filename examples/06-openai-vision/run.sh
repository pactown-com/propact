#!/bin/bash

# Helper script for OpenAI Vision example
echo "=== OpenAI Vision Analysis Example ==="
echo ""

# Create sample medical image (placeholder)
echo "Creating sample medical image..."
echo "FAKE MEDICAL X-RAY IMAGE DATA" > medical_scan.png

echo ""
echo "Running propact with OpenAI Vision API..."
echo "Note: This requires an OpenAI API key in OPENAI_API_KEY environment variable"
echo ""

# Check for API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Warning: OPENAI_API_KEY not set. This will fail without a valid API key."
    echo "Set it with: export OPENAI_API_KEY='sk-...'"
    echo ""
fi

# Run propact
python -m propact.cli README.md --endpoint "https://api.openai.com/v1/chat/completions" --schema openapi.json

echo ""
echo "✓ Example completed!"
echo "Check README.response.md for the analysis results"
echo ""

# Cleanup
echo "Cleaning up..."
rm -f medical_scan.png README.response.md
