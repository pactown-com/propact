#!/bin/bash

# Imgur Upload Example Runner
# Demonstrates propact with Imgur API

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
client_id = helper.check_env_var('IMGUR_CLIENT_ID')
if not client_id:
    helper.print_status('IMGUR_CLIENT_ID not found in environment', 'ERROR')
    helper.print_status('Register at https://api.imgur.com/oauth2/addclient', 'WARNING')
    exit(1)

# Create sample meme image
helper.print_status('Creating sample meme image...')
meme_file = helper.create_sample_file('meme.png')

# Run propact with Imgur endpoint
helper.print_status('Uploading to Imgur...')
result = helper.run_example(
    script_dir, 
    'https://api.imgur.com/3/image'
)

if result['success']:
    helper.print_status('Upload completed successfully!', 'SUCCESS')
    if Path('README.response.md').exists():
        helper.print_status('Check README.response.md for the image link')
else:
    helper.print_status(f'Upload failed: {result.get(\"error\", result.get(\"stderr\"))}', 'ERROR')

# Cleanup
helper.print_status('Cleaning up...')
helper.cleanup_files(meme_file, Path('README.response.md'))
"
