#!/usr/bin/env python3
"""
Entry point script for the Annotation Toolkit.
"""

import argparse
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.interface.generator import AnnotationGenerator

def main():
    """Parse command line arguments and run the generator."""
    parser = argparse.ArgumentParser(description='Generate annotation interface from YAML config')
    parser.add_argument('config', help='Path to YAML configuration file')
    parser.add_argument('--output', '-o', help='Output directory', default='output')
    
    args = parser.parse_args()
    
    generator = AnnotationGenerator()
    generator.generate_interface(args.config, args.output)
    
    print(f"Generated annotation interface in {args.output}")

if __name__ == '__main__':
    main() 