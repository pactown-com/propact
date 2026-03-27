#!/bin/bash

# Notion Page Creation Example Runner
# Demonstrates propact with Notion API

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
token = helper.check_env_var('NOTION_TOKEN')
if not token:
    helper.print_status('NOTION_TOKEN not found in environment', 'ERROR')
    helper.print_status('Create integration at https://www.notion.so/my-integrations', 'WARNING')
    exit(1)

# Create sample cover image
helper.print_status('Creating sample cover image...')
cover_file = helper.create_sample_file('cover.jpg')

# Run propact with Notion endpoint
helper.print_status('Creating Notion page...')
result = helper.run_example(
    script_dir, 
    'https://api.notion.com/v1/pages'
)

if result['success']:
    helper.print_status('Page created successfully!', 'SUCCESS')
    if Path('README.response.md').exists():
        helper.print_status('Check README.response.md for page details')
else:
    helper.print_status(f'Creation failed: {result.get(\"error\", result.get(\"stderr\"))}', 'ERROR')

# Cleanup
helper.print_status('Cleaning up...')
helper.cleanup_files(cover_file, Path('README.response.md'))
"
