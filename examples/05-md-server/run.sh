#!/bin/bash

# Helper script for 05-md-server example
echo "=== MD Server Example ==="
echo ""

# Create sample status image
echo "Creating sample status image..."
echo "FAKE STATUS IMAGE" > status.png

echo ""
echo "Starting propact in server mode..."
echo "Command: propact server.md --mode server --port 8080"
echo ""
echo "Note: Server mode is a placeholder in current implementation"
echo ""

# Run propact in server mode
python -m propact.cli server.md --mode server --port 8080

echo ""
echo "✓ Example completed!"
echo ""

# Cleanup
echo "Cleaning up..."
rm -f status.png
