#!/bin/bash

# Shell Upload Example Runner
# This script demonstrates how propact handles shell endpoints

echo "=== Shell Upload Example ==="
echo ""

# Create a dummy audio file for demonstration
echo "Creating sample audio file..."
echo "FAKE AUDIO DATA" > audio.mp3

echo ""
echo "Running propact with shell endpoint..."
echo ""

# Run propact with the README
python -m propact.cli README.md --endpoint "curl -X POST http://localhost:8080/upload"

echo ""
echo "Check README.response.md for the converted response"
echo ""

# Cleanup
echo "Cleaning up..."
rm -f audio.mp3
