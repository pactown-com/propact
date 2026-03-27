#!/bin/bash

# YouTube Metadata Example Runner
# Demonstrates propact with YouTube Data API

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
token = helper.check_env_var('YOUTUBE_ACCESS_TOKEN')
if not token:
    helper.print_status('YOUTUBE_ACCESS_TOKEN not found in environment', 'ERROR')
    helper.print_status('Get token from Google Cloud OAuth 2.0 flow', 'WARNING')
    exit(1)

# Run propact with YouTube endpoint
helper.print_status('Setting YouTube video metadata...')
result = helper.run_example(
    script_dir, 
    'https://www.googleapis.com/youtube/v3/videos?part=snippet,status,contentDetails'
)

if result['success']:
    helper.print_status('Metadata set successfully!', 'SUCCESS')
    if Path('README.response.md').exists():
        helper.print_status('Check README.response.md for video details')
else:
    helper.print_status(f'Set failed: {result.get(\"error\", result.get(\"stderr\"))}', 'ERROR')

# Cleanup
helper.print_status('Cleaning up...')
helper.cleanup_files(Path('README.response.md'))
"
