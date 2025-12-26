#!/usr/bin/env python3
"""Main entry point for GDSmeller."""

import argparse
import sys
import json
from typing import Optional, Dict

from .analyzer import GDScriptAnalyzer
from .rules.base import Severity


def load_config(config_path: Optional[str]) -> Dict:
    """Load configuration from file."""
    if not config_path:
        return {}
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load config file {config_path}: {e}")
        return {}


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='GDSmeller - Static analysis tool for GDScript',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze current directory
  python -m gdsmeller.main --path .
  
  # Analyze specific file
  python -m gdsmeller.main --path my_script.gd
  
  # Output as JSON
  python -m gdsmeller.main --path . --output-format json
  
  # Use custom config
  python -m gdsmeller.main --path . --config .gdsmeller.json
  
  # Fail on warnings
  python -m gdsmeller.main --path . --fail-on-warning
        """
    )
    
    parser.add_argument(
        '--path',
        default='.',
        help='Path to GDScript file or directory to analyze (default: current directory)'
    )
    
    parser.add_argument(
        '--config',
        help='Path to configuration file (JSON format)'
    )
    
    parser.add_argument(
        '--output-format',
        choices=['text', 'json', 'github'],
        default='text',
        help='Output format (default: text)'
    )
    
    parser.add_argument(
        '--fail-on-warning',
        action='store_true',
        help='Exit with error code if warnings are found'
    )
    
    parser.add_argument(
        '--version',
        action='store_true',
        help='Show version information'
    )
    
    args = parser.parse_args()
    
    if args.version:
        from . import __version__
        print(f"GDSmeller version {__version__}")
        return 0
    
    # Load configuration
    config = load_config(args.config)
    
    # Create analyzer
    analyzer = GDScriptAnalyzer(config)
    
    # Analyze path
    try:
        violations = analyzer.analyze(args.path)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    # Format and print output
    output = analyzer.format_violations(violations, args.output_format)
    print(output)
    
    # Determine exit code
    has_errors = any(v.severity == Severity.ERROR for v in violations)
    has_warnings = any(v.severity == Severity.WARNING for v in violations)
    
    if has_errors:
        return 1
    elif has_warnings and args.fail_on_warning:
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
