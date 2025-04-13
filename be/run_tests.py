#!/usr/bin/env python

import os
import sys
import django
from django.test.runner import DiscoverRunner

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.test_settings'

# Setup Django
django.setup()

# Run tests
runner = DiscoverRunner(verbosity=2)
failures = runner.run_tests(['diabetes_predictor.tests'])

# Exit with appropriate status code
sys.exit(bool(failures))
