#!/bin/bash

# Run all propact examples with proper categorization and error handling
# Usage: ./run-all.sh [OPTIONS]
# Options:
#   --offline    Run only offline examples (no API keys required)
#   --online     Run only online examples (requires API keys)
#   --dry-run    Validate examples without executing
#   --category   Run specific category (core, popular, legacy)
#   --help       Show this help message

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OFFLINE_EXAMPLES=("01-shell-upload" "02-openapi-rest" "03-mcp-tool" "04-ws-chat" "05-md-server" "07-ffmpeg-cli" "08-grpc-inference")
ONLINE_EXAMPLES=("06-openai-vision" "09-imgur" "10-slack" "11-discord" "12-openai-vision" "13-github-gist" "14-stripe" "15-youtube" "16-notion" "17-twitter")
LEGACY_EXAMPLES=("shell-to-mcp" "rest-ws-proxy")

# Parse command line arguments
RUN_OFFLINE=false
RUN_ONLINE=false
RUN_LEGACY=false
DRY_RUN=false
SPECIFIC_CATEGORY=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --offline)
            RUN_OFFLINE=true
            shift
            ;;
        --online)
            RUN_ONLINE=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --category)
            SPECIFIC_CATEGORY="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo
            echo "Options:"
            echo "  --offline    Run only offline examples (no API keys required)"
            echo "  --online     Run only online examples (requires API keys)"
            echo "  --dry-run    Validate examples without executing"
            echo "  --category   Run specific category (core, popular, legacy)"
            echo "  --help       Show this help message"
            echo
            echo "Categories:"
            echo "  core     - Core examples 01-08"
            echo "  popular  - Popular services 09-17"
            echo "  legacy   - Legacy examples in subdirectories"
            echo
            echo "Examples:"
            echo "  $0 --offline          # Run all offline examples"
            echo "  $0 --category core    # Run core examples only"
            echo "  $0 --dry-run          # Validate all examples"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Default behavior
if [[ "$RUN_OFFLINE" == false && "$RUN_ONLINE" == false && -z "$SPECIFIC_CATEGORY" ]]; then
    RUN_OFFLINE=true
    RUN_ONLINE=true
    RUN_LEGACY=true
elif [[ -n "$SPECIFIC_CATEGORY" ]]; then
    # Set run flags based on category
    case "$SPECIFIC_CATEGORY" in
        "core")
            RUN_OFFLINE=true
            RUN_ONLINE=true
            ;;
        "popular")
            RUN_ONLINE=true
            ;;
        "legacy")
            RUN_LEGACY=true
            ;;
    esac
fi

# Helper functions
print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
}

print_status() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if propact source is available
check_propact() {
    if [[ ! -f "${SCRIPT_DIR}/../src/propact/cli.py" ]]; then
        print_error "propact source not found"
        print_status "Ensure you're running from the examples directory"
        exit 1
    fi
}

# Validate example directory exists and has required files
validate_example() {
    local example_name="$1"
    local example_dir="${SCRIPT_DIR}/${example_name}"
    local md_file="${example_dir}/README.md"
    local sh_file="${example_dir}/run.sh"
    
    if [[ ! -d "$example_dir" ]]; then
        print_error "Example directory not found: $example_dir"
        return 1
    fi
    
    if [[ ! -f "$md_file" ]]; then
        print_error "README.md not found in $example_dir"
        return 1
    fi
    
    if [[ ! -f "$sh_file" ]]; then
        print_error "run.sh not found in $example_dir"
        return 1
    fi
    
    if [[ ! -x "$sh_file" ]]; then
        print_warning "Script is not executable: $sh_file"
        chmod +x "$sh_file"
    fi
    
    return 0
}

# Check environment variables for online examples
check_env_vars() {
    local example_name="$1"
    local env_file="${SCRIPT_DIR}/${example_name}/.env"
    
    if [[ -f "$env_file" ]]; then
        print_status "Checking environment variables for $example_name..."
        
        # Source the env file to check variables
        local missing_vars=()
        while IFS= read -r line; do
            # Skip comments and empty lines
            [[ "$line" =~ ^[[:space:]]*# ]] && continue
            [[ -z "$line" ]] && continue
            
            # Extract variable name
            local var_name="${line%%=*}"
            if [[ -z "${!var_name}" ]]; then
                missing_vars+=("$var_name")
            fi
        done < "$env_file"
        
        if [[ ${#missing_vars[@]} -gt 0 ]]; then
            print_warning "Missing environment variables for $example_name:"
            for var in "${missing_vars[@]}"; do
                echo -e "  ${YELLOW}- $var${NC}"
            done
            print_status "Set them in your shell or create ${example_name}/.env.local"
            return 1
        fi
    fi
    
    return 0
}

# Run a single example
run_example() {
    local example_name="$1"
    local example_dir="${SCRIPT_DIR}/${example_name}"
    
    print_status "Running $example_name..."
    
    # Validate directory and files
    if ! validate_example "$example_name"; then
        return 1
    fi
    
    # Check environment for online examples
    if [[ " ${ONLINE_EXAMPLES[@]} " =~ " ${example_name} " ]]; then
        if ! check_env_vars "$example_name"; then
            print_warning "Skipping $example_name due to missing environment variables"
            return 0
        fi
    fi
    
    # Run the example
    local sh_file="${example_dir}/run.sh"
    
    if [[ "$DRY_RUN" == true ]]; then
        print_status "DRY RUN: Would execute $sh_file"
        return 0
    fi
    
    # Run the script from its directory
    cd "$example_dir"
    
    # Set PYTHONPATH to include propact source
    export PYTHONPATH="${SCRIPT_DIR}/../src:${PYTHONPATH}"
    
    if bash "$sh_file" 2>&1; then
        print_success "$example_name completed successfully"
        return 0
    else
        print_error "$example_name failed"
        return 1
    fi
}

# Run legacy examples (in subdirectories)
run_legacy_example() {
    local example_name="$1"
    local example_dir="${SCRIPT_DIR}/${example_name}"
    
    if [[ ! -d "$example_dir" ]]; then
        print_error "Legacy example directory not found: $example_dir"
        return 1
    fi
    
    print_status "Running legacy example: $example_name"
    
    if [[ "$DRY_RUN" == true ]]; then
        print_status "DRY RUN: Would run $example_name"
        return 0
    fi
    
    # Look for run.sh in the legacy directory
    local run_script="${example_dir}/run.sh"
    if [[ -f "$run_script" ]]; then
        cd "$example_dir"
        if bash "$run_script" 2>&1; then
            print_success "$example_name completed successfully"
            return 0
        else
            print_error "$example_name failed"
            return 1
        fi
    else
        print_warning "No run.sh found in $example_dir"
        return 0
    fi
}

# Main execution
main() {
    print_header "Propact Examples Test Suite"
    
    # Check dependencies
    check_propact
    
    # Track results
    local total=0
    local passed=0
    local failed=0
    local skipped=0
    
    # Run examples based on category
    if [[ -z "$SPECIFIC_CATEGORY" || "$SPECIFIC_CATEGORY" == "core" ]]; then
        if [[ "$RUN_OFFLINE" == true ]]; then
            print_header "Running Offline Core Examples"
            for example in "${OFFLINE_EXAMPLES[@]}"; do
                ((total++))
                if run_example "$example"; then
                    ((passed++))
                else
                    ((failed++))
                fi
                echo
            done
        fi
        
        if [[ "$RUN_ONLINE" == true ]]; then
            print_header "Running Online Core Examples"
            for example in "06-openai-vision"; do
                ((total++))
                if run_example "$example"; then
                    ((passed++))
                else
                    ((failed++))
                fi
                echo
            done
        fi
    fi
    
    if [[ -z "$SPECIFIC_CATEGORY" || "$SPECIFIC_CATEGORY" == "popular" ]]; then
        if [[ "$RUN_ONLINE" == true ]]; then
            print_header "Running Popular Services Examples"
            for example in "${ONLINE_EXAMPLES[@]}"; do
                # Skip the duplicate openai-vision
                if [[ "$example" == "06-openai-vision" ]]; then
                    continue
                fi
                ((total++))
                if run_example "$example"; then
                    ((passed++))
                else
                    ((failed++))
                fi
                echo
            done
        fi
    fi
    
    if [[ -z "$SPECIFIC_CATEGORY" || "$SPECIFIC_CATEGORY" == "legacy" ]]; then
        if [[ "$RUN_LEGACY" == true ]]; then
            print_header "Running Legacy Examples"
            for example in "${LEGACY_EXAMPLES[@]}"; do
                ((total++))
                if run_legacy_example "$example"; then
                    ((passed++))
                else
                    ((failed++))
                fi
                echo
            done
        fi
    fi
    
    # Print summary
    print_header "Test Suite Summary"
    echo -e "Total examples: ${BLUE}$total${NC}"
    echo -e "${GREEN}Passed: $passed${NC}"
    echo -e "${RED}Failed: $failed${NC}"
    echo -e "${YELLOW}Skipped: $skipped${NC}"
    echo
    
    if [[ $failed -eq 0 ]]; then
        print_success "All examples completed successfully!"
        exit 0
    else
        print_error "$failed example(s) failed"
        exit 1
    fi
}

# Run main function
main
