#!/bin/bash
# Test all examples in examples/ directory

echo "Testing all Propact examples..."
echo "================================"

RESULTS_FILE="/tmp/propact_test_results.txt"
echo "Test Results - $(date)" > $RESULTS_FILE
echo "================================" >> $RESULTS_FILE

# Function to test an example
test_example() {
    local dir=$1
    local name=$(basename "$dir")
    
    echo ""
    echo "Testing: $name"
    echo "----------------"
    
    if [ -f "$dir/README.md" ]; then
        cd "$dir"
        
        # Determine endpoint from README or use default
        local endpoint=""
        
        # Check for run.sh first
        if [ -f "run.sh" ]; then
            echo "  Found run.sh - executing..."
            bash run.sh 2>&1 | head -20
        else
            # Try to find endpoint in README
            endpoint=$(grep -oP 'https?://[^\s")]+' README.md | head -1)
            
            if [ -z "$endpoint" ]; then
                # Use default endpoints based on example type
                case "$name" in
                    *weather*|*01-weather*) 
                        endpoint="https://api.openweathermap.org/data/2.5/weather?lat=54.35&lon=18.65&appid=demo" ;;
                    *todo*|*18-todo*) 
                        endpoint="https://jsonplaceholder.typicode.com/todos/1" ;;
                    *users*|*19-users*) 
                        endpoint="https://jsonplaceholder.typicode.com/users/1" ;;
                    *posts*|*20-posts*) 
                        endpoint="https://jsonplaceholder.typicode.com/posts/1" ;;
                    *) 
                        echo "  ⚠️  No endpoint found, skipping..."
                        echo "$name: SKIPPED (no endpoint)" >> $RESULTS_FILE
                        cd - > /dev/null
                        return ;;
                esac
            fi
            
            echo "  Using endpoint: $endpoint"
            poetry run propact run README.md --endpoint "$endpoint" 2>&1 | head -10
        fi
        
        # Check if response file was created and has content
        if [ -f "README.response.md" ]; then
            local size=$(stat -f%z "README.response.md" 2>/dev/null || stat -c%s "README.response.md" 2>/dev/null || echo "0")
            if [ "$size" -gt 10 ]; then
                echo "  ✅ Response saved: $size bytes"
                echo "$name: PASS ($size bytes)" >> $RESULTS_FILE
            else
                echo "  ❌ Response empty or too small: $size bytes"
                echo "$name: FAIL (empty response)" >> $RESULTS_FILE
            fi
        else
            echo "  ❌ No response file created"
            echo "$name: FAIL (no response file)" >> $RESULTS_FILE
        fi
        
        cd - > /dev/null
    else
        echo "  ⚠️  No README.md found"
        echo "$name: SKIP (no README)" >> $RESULTS_FILE
    fi
}

# Main test loop
cd /home/tom/github/pactown-com/propact/examples

for dir in */; do
    # Skip non-directory entries and special dirs
    if [[ "$dir" == "dsl/" ]] || [[ "$dir" == "uniconverter/" ]] || [[ "$dir" == "smart-test/" ]]; then
        continue
    fi
    test_example "$dir"
done

echo ""
echo "================================"
echo "Test Summary"
echo "================================"
cat $RESULTS_FILE
