#!/bin/bash

# Discord Message Example Runner
# Demonstrates propact with Discord API

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
token = helper.check_env_var('DISCORD_TOKEN')
channel_id = helper.check_env_var('DISCORD_CHANNEL_ID')
if not token or not channel_id:
    helper.print_status('DISCORD_TOKEN or DISCORD_CHANNEL_ID not found', 'ERROR')
    helper.print_status('Create a Discord bot at https://discord.com/developers/applications', 'WARNING')
    exit(1)

# Create sample dashboard image
helper.print_status('Creating sample dashboard image...')
dashboard_file = helper.create_sample_file('dashboard.png')

# Run propact with Discord endpoint
helper.print_status('Sending to Discord...')
endpoint = f'https://discord.com/api/v10/channels/{channel_id}/messages'
result = helper.run_example(script_dir, endpoint)

if result['success']:
    helper.print_status('Message sent successfully!', 'SUCCESS')
    if Path('README.response.md').exists():
        helper.print_status('Check README.response.md for message details')
else:
    helper.print_status(f'Send failed: {result.get(\"error\", result.get(\"stderr\"))}', 'ERROR')

# Cleanup
helper.print_status('Cleaning up...')
helper.cleanup_files(dashboard_file, Path('README.response.md'))
"
