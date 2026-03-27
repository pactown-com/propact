#!/bin/bash
# Run all new API examples

set -e

echo "🚀 Running Complete API Examples"
echo "================================="

cd "$(dirname "$0")/.."

# Example 1: Todo API
echo ""
echo "📋 Example 1: Todo API"
echo "----------------------"
cd examples/18-todo-api
poetry run propact run README.md --endpoint "https://jsonplaceholder.typicode.com/todos/1"
cd ../..

# Example 2: Users API
echo ""
echo "👤 Example 2: Users API"
echo "-----------------------"
cd examples/19-users-api
poetry run propact run README.md --endpoint "https://jsonplaceholder.typicode.com/users/1"
cd ../..

# Example 3: Posts API
echo ""
echo "📝 Example 3: Posts API"
echo "----------------------"
cd examples/20-posts-api
poetry run propact run README.md --endpoint "https://jsonplaceholder.typicode.com/posts/1"
cd ../..

echo ""
echo "✅ All examples complete!"
echo ""
echo "Response files created:"
echo "  - examples/18-todo-api/README.response.md"
echo "  - examples/19-users-api/README.response.md"
echo "  - examples/20-posts-api/README.response.md"
