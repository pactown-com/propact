#!/bin/bash

# OpenAI Vision Example Runner
# Demonstrates propact with OpenAI's Vision API

python3 -c "
from pathlib import Path
import sys

# Get the directory of this script
script_dir = Path.cwd()
src_path = script_dir.parent.parent / 'src'
sys.path.insert(0, str(src_path))

from propact.testing import ExampleHelper

# Check environment
helper = ExampleHelper()
api_key = helper.check_env_var('OPENAI_API_KEY')
if not api_key:
    helper.print_status('OPENAI_API_KEY not found in environment', 'ERROR')
    helper.print_status('Set it with: export OPENAI_API_KEY=sk-...', 'WARNING')
    exit(1)

# Create sample X-ray image
helper.print_status('Creating sample X-ray image...')
xray_file = helper.create_sample_file('xray.png')

# Run propact with OpenAI endpoint
helper.print_status('Analyzing X-ray with OpenAI Vision API...')
result = helper.run_example(
    script_dir, 
    'https://api.openai.com/v1/chat/completions'
)

if result['success']:
    helper.print_status('Analysis completed successfully!', 'SUCCESS')
    if Path('README.response.md').exists():
        helper.print_status('Check README.response.md for the medical analysis')
else:
    helper.print_status(f'Analysis failed: {result.get(\"error\", result.get(\"stderr\"))}', 'ERROR')

# Cleanup
helper.print_status('Cleaning up...')
helper.cleanup_files(xray_file, Path('README.response.md'))
"
