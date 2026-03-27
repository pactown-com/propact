#!/bin/bash

# Stripe Payment Example Runner
# Demonstrates propact with Stripe API

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
key = helper.check_env_var('STRIPE_SECRET_KEY')
if not key:
    helper.print_status('STRIPE_SECRET_KEY not found in environment', 'ERROR')
    helper.print_status('Get key from https://dashboard.stripe.com/apikeys', 'WARNING')
    exit(1)

# Run propact with Stripe endpoint
helper.print_status('Creating Stripe payment intent...')
result = helper.run_example(
    script_dir, 
    'https://api.stripe.com/v1/payment_intents'
)

if result['success']:
    helper.print_status('Payment intent created successfully!', 'SUCCESS')
    if Path('README.response.md').exists():
        helper.print_status('Check README.response.md for client_secret')
else:
    helper.print_status(f'Creation failed: {result.get(\"error\", result.get(\"stderr\"))}', 'ERROR')

# Cleanup
helper.print_status('Cleaning up...')
helper.cleanup_files(Path('README.response.md'))
"
