#!/bin/bash

# Helper script for gRPC inference example
echo "=== gRPC Inference Example ==="
echo ""

# Create sample image file (placeholder)
echo "Creating sample medical image..."
echo "FAKE MEDICAL IMAGE DATA" > medical.jpg

echo ""
echo "Running propact with gRPC endpoint..."
echo "Note: This requires gRPC dependencies and a running inference server"
echo ""

# Check for gRPC dependencies
python -c "import grpc" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Warning: gRPC dependencies not installed. Install with: pip install propact[grpc]"
    echo ""
fi

# Run propact
python -m propact.cli README.md --endpoint "grpc://localhost:50051/InferenceService/AnalyzeImage"

echo ""
echo "✓ Example completed!"
echo "Check README.response.md for inference results"
echo ""

# Cleanup
echo "Cleaning up..."
rm -f medical.jpg README.response.md
