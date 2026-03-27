#!/bin/bash
# Test all examples with proper HTTP methods

echo "Testing all Propact examples..."
echo "================================"

PASS=0
FAIL=0
SKIP=0

# Function to test an example
test_example() {
    local dir=$1
    local name=$(basename "$dir")
    
    echo ""
    echo "Testing: $name"
    echo "----------------"
    
    if [ -f "$dir/README.md" ]; then
        cd "$dir"
        
        # Determine endpoint and method from example type
        local endpoint=""
        local method="GET"
        
        case "$name" in
            *weather*|*01-weather*) 
                endpoint="https://api.openweathermap.org/data/2.5/weather?lat=54.35&lon=18.65&appid=demo" ;;
            *todo*|*18-todo*) 
                endpoint="https://jsonplaceholder.typicode.com/todos/1" ;;
            *users*|*19-users*) 
                endpoint="https://jsonplaceholder.typicode.com/users/1" ;;
            *posts*|*20-posts*) 
                endpoint="https://jsonplaceholder.typicode.com/posts/1" ;;
            *rest-ws-proxy*)
                endpoint="http://localhost:8080/api/proxy"
                method="POST" ;;
            *github*|*13-github*)
                endpoint="https://api.github.com/users/octocat"
                method="GET" ;;
            *) 
                echo "  ⚠️  No endpoint configured, skipping..."
                ((SKIP++))
                cd - > /dev/null
                return ;;
        esac
        
        echo "  Endpoint: $endpoint (Method: $method)"
        
        if /home/tom/github/pactown-com/propact/.venv/bin/propact run README.md --endpoint "$endpoint" --method "$method" > /tmp/propact_output.txt 2>&1; then
            if [ -f "README.response.md" ]; then
                local size=$(stat -f%z "README.response.md" 2>/dev/null || stat -c%s "README.response.md" 2>/dev/null || echo "0")
                local status=$(grep -oE '\*\*Status:\*\* [0-9]+' README.response.md | grep -oE '[0-9]+' || echo "unknown")
                
                if [ "$status" = "200" ]; then
                    echo "  ✅ PASS - Status: $status, Size: $size bytes"
                    ((PASS++))
                elif [ "$status" = "unknown" ]; then
                    echo "  ⚠️  UNKNOWN - No status found, Size: $size bytes"
                    ((FAIL++))
                else
                    echo "  ❌ FAIL - Status: $status, Size: $size bytes"
                    ((FAIL++))
                fi
            else
                echo "  ❌ FAIL - No response file created"
                ((FAIL++))
            fi
        else
            echo "  ❌ FAIL - Command failed"
            ((FAIL++))
        fi
        
        cd - > /dev/null
    else
        echo "  ⚠️  No README.md found, skipping..."
        ((SKIP++))
    fi
}

# Main test loop
cd /home/tom/github/pactown-com/propact/examples

for dir in */; do
    # Skip non-directory entries and special dirs
    if [[ "$dir" == "dsl/" ]] || [[ "$dir" == "uniconverter/" ]] || [[ "$dir" == "smart-test/" ]] || [[ "$dir" == "public-apis/" ]]; then
        continue
    fi
    test_example "$dir"
done

echo ""
echo "================================"
echo "Test Summary"
echo "================================"
echo "✅ PASS: $PASS"
echo "❌ FAIL: $FAIL"
echo "⚠️  SKIP: $SKIP"
echo "================================"
