#!/bin/bash
# Albums API Example Runner
# 
# This example demonstrates fetching photo albums from JSONPlaceholder API

set -e

echo "📷 Albums API Example"
echo "====================="
echo ""

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "1️⃣  Get a single album (GET)"
echo "---------------------------"
poetry run propact run README.md \
    --endpoint "https://jsonplaceholder.typicode.com/albums/1" \
    --method GET

echo ""
echo "✅ Response saved to: README.response.md"
echo ""

echo "📄 Response Preview:"
echo "-------------------"
head -15 README.response.md

echo ""
echo "2️⃣  Get photos in album (GET)"
echo "-----------------------------"
poetry run propact run README.md \
    --endpoint "https://jsonplaceholder.typicode.com/albums/1/photos?_limit=3" \
    --method GET

echo ""
echo "✅ Done! Check README.response.md for full output"
