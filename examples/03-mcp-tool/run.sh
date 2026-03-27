#!/bin/bash

# OpenAPI REST Example Runner
# This script demonstrates propact's schema-aware multipart handling

python3 -c "
from pathlib import Path
import sys

# Get the directory of this script
script_dir = Path.cwd()
src_path = script_dir.parent.parent / 'src'
sys.path.insert(0, str(src_path))

from propact.testing import ExampleHelper

# Create sample image file
helper = ExampleHelper()
helper.print_status('Creating sample image file...')
image_file = helper.create_sample_file('medical_scan.png')

# Run propact with OpenAI endpoint
helper.print_status('Running propact with OpenAI Vision API...')
result = helper.run_example(script_dir, 'https://api.openai.com/v1/chat/completions', 'openapi.json')

if result['success']:
    helper.print_status('Example completed successfully!', 'SUCCESS')
    if Path('README.response.md').exists():
        helper.print_status('Check README.response.md for the converted response')
else:
    helper.print_status(f'Example failed: {result.get(\"error\", result.get(\"stderr\"))}', 'ERROR')

# Cleanup
helper.print_status('Cleaning up...')
helper.cleanup_files(image_file, Path('README.response.md'))
"
