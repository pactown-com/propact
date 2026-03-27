#!/bin/bash
# Posts API Example Runner
# 
# This example demonstrates fetching blog posts from JSONPlaceholder API
# using propact with proper HTTP method handling

set -e

echo "📝 Posts API Example"
echo "===================="
echo ""

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "1️⃣  Get a single post (GET)"
echo "---------------------------"
poetry run propact run README.md \
    --endpoint "https://jsonplaceholder.typicode.com/posts/1" \
    --method GET

echo ""
echo "✅ Response saved to: README.response.md"
echo ""

# Show response preview
echo "📄 Response Preview:"
echo "-------------------"
head -20 README.response.md

echo ""
echo "2️⃣  Get comments for post (GET)"
echo "-------------------------------"
poetry run propact run README.md \
    --endpoint "https://jsonplaceholder.typicode.com/posts/1/comments?_limit=3" \
    --method GET

echo ""
echo "✅ Done! Check README.response.md for full output"
