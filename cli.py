#!/usr/bin/env python3
"""
CLI runner script for the Library Management System
"""

import sys
import os

# Add the src directory to the path so we can import revsin
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    from revsin.cli.main import cli
    cli()
