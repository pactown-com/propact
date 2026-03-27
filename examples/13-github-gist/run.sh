#!/bin/bash

# GitHub Gist Example Runner
# Demonstrates propact with GitHub Gists API

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
token = helper.check_env_var('GITHUB_TOKEN')
if not token:
    helper.print_status('GITHUB_TOKEN not found in environment', 'ERROR')
    helper.print_status('Create token at https://github.com/settings/tokens', 'WARNING')
    exit(1)

# Run propact with GitHub endpoint
helper.print_status('Creating GitHub Gist...')
result = helper.run_example(
    script_dir, 
    'https://api.github.com/gists'
)

if result['success']:
    helper.print_status('Gist created successfully!', 'SUCCESS')
    if Path('README.response.md').exists():
        helper.print_status('Check README.response.md for gist URLs')
else:
    helper.print_status(f'Creation failed: {result.get(\"error\", result.get(\"stderr\"))}', 'ERROR')

# Cleanup
helper.print_status('Cleaning up...')
helper.cleanup_files(Path('README.response.md'))
"
