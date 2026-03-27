#!/bin/bash

# Shell Upload Example Runner
# This script demonstrates how propact handles shell endpoints

# Add parent directory to Python path for testing helpers
export PYTHONPATH="${PYTHONPATH}:$(dirname "$0")/../../src"

python3 -c "
from pathlib import Path
import sys

# Get the directory of this script
script_dir = Path('$(dirname "$0")').absolute()
src_path = script_dir.parent / 'src'
sys.path.insert(0, str(src_path))

from propact.testing import ExampleHelper

# Create sample audio file
helper = ExampleHelper()
helper.print_status('Creating sample audio file...')
audio_file = helper.create_sample_file('audio.mp3')

# Run propact with the README
helper.print_status('Running propact with shell endpoint...')
result = helper.run_example(script_dir, 'curl -X POST http://localhost:8080/upload')

if result['success']:
    helper.print_status('Example completed successfully!', 'SUCCESS')
    if Path('README.response.md').exists():
        helper.print_status('Check README.response.md for the converted response')
else:
    helper.print_status(f'Example failed: {result.get(\"error\", result.get(\"stderr\"))}', 'ERROR')

# Cleanup
helper.print_status('Cleaning up...')
helper.cleanup_files(audio_file, Path('README.response.md'))
"
