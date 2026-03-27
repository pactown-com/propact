# Shell to MCP Integration Example

This example demonstrates how to pipe shell command output into MCP tools for processing.

## Overview

The pipeline:
1. Uses shell commands to generate data
2. Passes the data to MCP tools for processing
3. Stores the results

## Protocol Blocks

### Step 1: Generate Sample Data
```propact:shell
# Create sample data file
cat > sample_data.json << EOF
[
  {"id": 1, "name": "Alice", "score": 85},
  {"id": 2, "name": "Bob", "score": 92},
  {"id": 3, "name": "Charlie", "score": 78}
]
EOF

echo "Data generated: sample_data.json"
```

### Step 2: Validate Data Structure
```propact:shell
# Validate JSON structure
python3 -m json.tool sample_data.json > /dev/null
if [ $? -eq 0 ]; then
    echo "✓ JSON is valid"
else
    echo "✗ JSON validation failed"
    exit 1
fi
```

### Step 3: Process with MCP Tool
```propact:mcp
{
  "method": "tools/call",
  "params": {
    "name": "data_processor",
    "arguments": {
      "input_file": "sample_data.json",
      "operation": "calculate_average",
      "output_file": "results.json"
    }
  }
}
```

### Step 4: Transform Data
```propact:mcp
{
  "method": "tools/call",
  "params": {
    "name": "data_transformer",
    "arguments": {
      "input": "sample_data.json",
      "transform": "filter_high_scorers",
      "threshold": 80,
      "output": "high_scorers.json"
    }
  }
}
```

### Step 5: Generate Report
```propact:shell
# Generate a summary report
echo "# Data Processing Report" > report.md
echo "" >> report.md
echo "## Average Score" >> report.md
if [ -f results.json ]; then
    cat results.json >> report.md
fi
echo "" >> report.md
echo "## High Scorers (>80)" >> report.md
if [ -f high_scorers.json ]; then
    cat high_scorers.json >> report.md
fi

echo "Report generated: report.md"
```

### Step 6: Clean Up
```propact:shell
# Optional: Clean up temporary files
# rm -f sample_data.json results.json high_scorers.json
echo "Pipeline completed!"
```

## Running the Example

```bash
# Execute the full pipeline
propact README.md

# Execute only shell commands
propact README.md --protocol shell

# Execute only MCP commands
propact README.md --protocol mcp
```

## Expected Output

The pipeline will:
1. Create a sample JSON data file
2. Validate the JSON structure
3. Process the data with MCP tools (simulated)
4. Filter high scorers
5. Generate a markdown report

## Notes

- MCP tools in this example are simulated since actual MCP server is not running
- In a real scenario, you would have an MCP server with the `data_processor` and `data_transformer` tools
- The shell commands demonstrate file operations and basic data validation
