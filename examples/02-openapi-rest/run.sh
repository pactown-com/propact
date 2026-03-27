#!/bin/bash

# Helper script for 02-openapi-rest example
echo "=== OpenAPI REST Example ==="
echo ""

# Create sample image file
echo "Creating sample image file..."
echo "FAKE IMAGE DATA FOR DEMONSTRATION" > medical_scan.png

echo ""
echo "Running propact with OpenAPI endpoint..."
echo "Command: propact README.md --endpoint 'https://api.vision.ai/v1/analyze' --schema openapi.json"
echo ""

# Run propact
python -m propact.cli README.md --endpoint "https://api.vision.ai/v1/analyze" --schema openapi.json

echo ""
echo "✓ Example completed!"
echo "Check README.response.md for the converted response"
echo ""

# Cleanup
echo "Cleaning up..."
rm -f medical_scan.png README.response.md
