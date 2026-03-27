#!/bin/bash
# Users API Example Runner
# 
# This example demonstrates fetching user data from JSONPlaceholder API
# using propact with proper HTTP method handling

set -e

echo "👤 Users API Example"
echo "==================="
echo ""

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "1️⃣  Get a single user (GET)"
echo "---------------------------"
poetry run propact run README.md \
    --endpoint "https://jsonplaceholder.typicode.com/users/1" \
    --method GET

echo ""
echo "✅ Response saved to: README.response.md"
echo ""

# Show response preview
echo "📄 Response Preview:"
echo "-------------------"
head -20 README.response.md

echo ""
echo "2️⃣  List all users (GET)"
echo "------------------------"
poetry run propact run README.md \
    --endpoint "https://jsonplaceholder.typicode.com/users?_limit=3" \
    --method GET

echo ""
echo "✅ Done! Check README.response.md for full output"
