#!/bin/bash

# Helper script for 03-mcp-tool example
echo "=== MCP Tool Example ==="
echo ""

# Create sample video file
echo "Creating sample video file..."
echo "FAKE VIDEO DATA FOR DEMONSTRATION" > demo.mp4

echo ""
echo "Running propact with MCP endpoint..."
echo "Command: propact README.md --endpoint 'mcp://localhost:8080/video-tool'"
echo ""

# Run propact
python -m propact.cli README.md --endpoint "mcp://localhost:8080/video-tool"

echo ""
echo "✓ Example completed!"
echo "Check README.response.md for the converted response"
echo ""

# Cleanup
echo "Cleaning up..."
rm -f demo.mp4 README.response.md
