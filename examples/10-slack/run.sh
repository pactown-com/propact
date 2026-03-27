#!/bin/bash

# Slack Upload Example Runner
# Demonstrates propact with Slack API

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
token = helper.check_env_var('SLACK_TOKEN')
if not token:
    helper.print_status('SLACK_TOKEN not found in environment', 'ERROR')
    helper.print_status('Create a Slack bot app at https://api.slack.com/apps', 'WARNING')
    exit(1)

# Create sample screenshot
helper.print_status('Creating sample screenshot...')
screenshot_file = helper.create_sample_file('screenshot.png')

# Run propact with Slack endpoint
helper.print_status('Uploading to Slack...')
result = helper.run_example(
    script_dir, 
    'https://slack.com/api/files.upload'
)

if result['success']:
    helper.print_status('Upload completed successfully!', 'SUCCESS')
    if Path('README.response.md').exists():
        helper.print_status('Check README.response.md for file details')
else:
    helper.print_status(f'Upload failed: {result.get(\"error\", result.get(\"stderr\"))}', 'ERROR')

# Cleanup
helper.print_status('Cleaning up...')
helper.cleanup_files(screenshot_file, Path('README.response.md'))
"
