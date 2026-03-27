#!/bin/bash

# Twitter/X Upload Example Runner
# Demonstrates propact with Twitter API v2

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
token = helper.check_env_var('TWITTER_BEARER')
if not token:
    helper.print_status('TWITTER_BEARER not found in environment', 'ERROR')
    helper.print_status('Get token from https://developer.twitter.com/', 'WARNING')
    exit(1)

# Create sample announcement image
helper.print_status('Creating sample announcement image...')
image_file = helper.create_sample_file('announcement.png')

# Step 1: Upload media
helper.print_status('Step 1: Uploading media to Twitter...')
result = helper.run_example(
    script_dir, 
    'https://upload.twitter.com/1.1/media/upload.json'
)

if result['success']:
    helper.print_status('Media uploaded successfully!', 'SUCCESS')
    if Path('README.response.md').exists():
        helper.print_status('Check README.response.md for media_id')
        helper.print_status('Update JSON with media_id and run step 2 to post tweet')
else:
    helper.print_status(f'Upload failed: {result.get(\"error\", result.get(\"stderr\"))}', 'ERROR')

# Cleanup
helper.print_status('Cleaning up...')
helper.cleanup_files(image_file, Path('README.response.md'))
"
