#!/bin/bash

# Security Hardening Demo Runner
# This script demonstrates how Propact handles various security threats

echo "🔒 Propact Security Hardening Demo"
echo "=================================="
echo

# Check if we're in the right directory
if [ ! -f "attack_samples.md" ]; then
    echo "❌ Error: Please run from the 05-security-hardening directory"
    exit 1
fi

# Install required dependencies if not present
echo "📦 Checking dependencies..."
python3 -c "import bleach" 2>/dev/null || {
    echo "Installing bleach for HTML sanitization..."
    pip3 install bleach
}

python3 -c "import jsonschema" 2>/dev/null || {
    echo "Installing jsonschema for validation..."
    pip3 install jsonschema
}

python3 -c "import pillow" 2>/dev/null || {
    echo "Installing pillow for image optimization..."
    pip3 install pillow
}

echo
echo "🚀 Running security demo..."
echo

# Run the secure handler demo
python3 secure_handler.py

echo
echo "📚 What was demonstrated:"
echo "  • XSS attack prevention"
echo "  • Base64 payload limits"
echo "  • Script tag blocking"
echo "  • SSRF protection"
echo "  • Content optimization"
echo "  • Security audit logging"
echo
echo "🔍 Check the output above to see how each attack was mitigated!"
echo
echo "💡 Try editing attack_samples.md to test your own scenarios!"
