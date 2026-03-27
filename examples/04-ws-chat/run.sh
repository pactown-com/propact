#!/bin/bash

# Helper script for 04-ws-chat example
echo "=== WebSocket Chat Example ==="
echo ""

# Create sample config file
echo "Creating sample config file..."
cat > config.yaml << EOF
server:
  host: localhost
  port: 8080
  path: /chat
auth:
  token: demo-token-123
user:
  id: 123
  name: "Demo User"
EOF

echo ""
echo "Running propact with WebSocket endpoint..."
echo "Command: propact README.md --endpoint 'ws://localhost:8080/chat'"
echo ""

# Run propact
python -m propact.cli README.md --endpoint "ws://localhost:8080/chat"

echo ""
echo "✓ Example completed!"
echo "Check README.response.md for the converted response"
echo ""

# Cleanup
echo "Cleaning up..."
rm -f config.yaml README.response.md
