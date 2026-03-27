#!/bin/bash
# Photos API Example Runner
# 
# This example demonstrates fetching photos from JSONPlaceholder API

set -e

echo "📸 Photos API Example"
echo "====================="
echo ""

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "1️⃣  Get a single photo (GET)"
echo "---------------------------"
poetry run propact run README.md \
    --endpoint "https://jsonplaceholder.typicode.com/photos/1" \
    --method GET

echo ""
echo "✅ Response saved to: README.response.md"
echo ""

echo "📄 Response Preview:"
echo "-------------------"
head -15 README.response.md

echo ""
echo "2️⃣  Get photos from album (GET)"
echo "------------------------------"
poetry run propact run README.md \
    --endpoint "https://jsonplaceholder.typicode.com/albums/1/photos?_limit=3" \
    --method GET

echo ""
echo "✅ Done! Check README.response.md for full output"
