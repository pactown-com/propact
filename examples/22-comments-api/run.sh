#!/bin/bash
# Comments API Example Runner
# 
# This example demonstrates fetching comments from JSONPlaceholder API

set -e

echo "💬 Comments API Example"
echo "======================="
echo ""

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "1️⃣  Get a single comment (GET)"
echo "-----------------------------"
poetry run propact run README.md \
    --endpoint "https://jsonplaceholder.typicode.com/comments/1" \
    --method GET

echo ""
echo "✅ Response saved to: README.response.md"
echo ""

echo "📄 Response Preview:"
echo "-------------------"
head -15 README.response.md

echo ""
echo "2️⃣  Get comments for post (GET)"
echo "------------------------------"
poetry run propact run README.md \
    --endpoint "https://jsonplaceholder.typicode.com/posts/1/comments?_limit=3" \
    --method GET

echo ""
echo "✅ Done! Check README.response.md for full output"
