#!/bin/bash
# Test all examples in examples/ directory and verify response format

echo "=========================================="
echo "Testing All Propact Examples"
echo "=========================================="

PASS=0
FAIL=0
SKIP=0

# Test function
test_example() {
    local dir=$1
    local name=$(basename "$dir")
    
    echo ""
    echo "📁 Testing: $name"
    echo "------------------------------------------"
    
    if [ ! -f "$dir/README.md" ]; then
        echo "   ⚠️ SKIP - No README.md"
        ((SKIP++))
        return
    fi
    
    cd "$dir"
    
    # Determine endpoint and method based on example type
    local endpoint=""
    local method="GET"
    
    case "$name" in
        *todo*|*18-todo*) 
            endpoint="https://jsonplaceholder.typicode.com/todos/1" ;;
        *users*|*19-users*) 
            endpoint="https://jsonplaceholder.typicode.com/users/1" ;;
        *posts*|*20-posts*) 
            endpoint="https://jsonplaceholder.typicode.com/posts/1" ;;
        *github*|*13-github*) 
            endpoint="https://api.github.com/users/octocat" ;;
        *rest-ws-proxy*)
            endpoint="http://localhost:8080/api/proxy"
            method="POST" ;;
        *)
            echo "   ⚠️ SKIP - No endpoint configured"
            ((SKIP++))
            cd - > /dev/null
            return ;;
    esac
    
    echo "   🌐 Endpoint: $endpoint"
    echo "   📡 Method: $method"
    
    # Run propact
    if poetry run propact run README.md --endpoint "$endpoint" --method "$method" > /tmp/test_output.txt 2>&1; then
        if [ -f "README.response.md" ]; then
            # Check response format
            local has_header=$(grep -c "# Response from Propact" README.response.md || echo 0)
            local has_status=$(grep -c "Status:" README.response.md || echo 0)
            local has_json=$(grep -c "json" README.response.md || echo 0)
            local size=$(wc -c < README.response.md)
            
            if [ "$has_header" -gt 0 ] && [ "$has_status" -gt 0 ] && [ "$size" -gt 100 ]; then
                echo "   ✅ PASS - Valid markdown response"
                echo "      📊 Size: $size bytes"
                echo "      📝 Has header: $has_header"
                echo "      📈 Has status: $has_status"
                echo "      💻 Has JSON: $has_json"
                ((PASS++))
            else
                echo "   ❌ FAIL - Invalid response format"
                echo "      📊 Size: $size bytes"
                cat README.response.md | head -5
                ((FAIL++))
            fi
        else
            echo "   ❌ FAIL - No response file created"
            ((FAIL++))
        fi
    else
        echo "   ❌ FAIL - Command failed"
        tail -5 /tmp/test_output.txt
        ((FAIL++))
    fi
    
    cd - > /dev/null
}

# Main test loop
cd /home/tom/github/pactown-com/propact/examples

for dir in */; do
    # Skip certain directories
    if [[ "$dir" =~ ^(dsl/|uniconverter/|smart-test/|public-apis/|openapi-llm-demo/|error-demo/)$ ]]; then
        continue
    fi
    test_example "$dir"
done

echo ""
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo "✅ PASS:  $PASS"
echo "❌ FAIL:  $FAIL"
echo "⚠️  SKIP:  $SKIP"
echo "=========================================="

if [ $FAIL -eq 0 ]; then
    echo "🎉 All tested examples passed!"
    exit 0
else
    echo "⚠️  Some tests failed"
    exit 1
fi
