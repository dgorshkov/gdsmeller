# GDSmeller 🔍

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-blue.svg)

**GDSmeller** is a static analysis tool for GDScript that helps you find code smells and common issues in your Godot game projects. It's designed as a GitHub Action for seamless integration into your CI/CD workflow.

## Features

- 🎯 **Comprehensive Rule Set**: Detects common GDScript issues across multiple categories
- 📊 **Organized by Topics**: Rules are structured by readability, security, performance, and more
- 🔧 **Configurable**: Easily enable/disable rules and customize settings
- 🚀 **Easy Integration**: Works as a GitHub Action or standalone Python tool
- 📝 **Multiple Output Formats**: Text, JSON, and GitHub Actions annotations

## Rule Categories

### Readability (R-series)
- **R001**: Line Too Long - Lines should not exceed configured length
- **R002**: Missing Class Docstring - Classes should have documentation
- **R003**: Missing Function Docstring - Public functions should be documented
- **R004**: Inconsistent Indentation - Detect mixing of tabs and spaces

### Security (S-series)
- **S001**: Hardcoded Password - Avoid hardcoding sensitive credentials
- **S002**: Unsafe Eval/Execute - Detect potentially unsafe Expression.parse() usage
- **S003**: SQL Injection Risk - Prevent SQL string concatenation vulnerabilities
- **S004**: Insecure Random - Use Crypto for security-critical randomness

### Performance (P-series)
- **P001**: Process in Loop - Avoid expensive operations in _process() loops
- **P002**: String Concatenation in Loop - Use Array.join() for better performance
- **P003**: Signal Not Disconnected - Ensure signals are properly disconnected
- **P004**: Get Node in Process - Cache node references instead of repeated lookups

## Usage as GitHub Action

Add GDSmeller to your workflow:

```yaml
name: GDScript Analysis

on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run GDSmeller
        uses: dgorshkov/gdsmeller@main
        with:
          path: '.'
          output-format: 'github'
          fail-on-warning: 'false'
```

### Action Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `path` | Path to GDScript files or directory | No | `.` |
| `config` | Path to configuration file | No | - |
| `fail-on-warning` | Fail if warnings are found | No | `false` |
| `output-format` | Output format (text, json, github) | No | `github` |

## Usage as Python Tool

### Installation

```bash
pip install -r requirements.txt
```

### Command Line

```bash
# Analyze current directory
python -m gdsmeller.main --path .

# Analyze specific file
python -m gdsmeller.main --path scripts/player.gd

# Output as JSON
python -m gdsmeller.main --path . --output-format json

# Use custom config
python -m gdsmeller.main --path . --config .gdsmeller.json

# Fail on warnings
python -m gdsmeller.main --path . --fail-on-warning
```

### Python API

```python
from gdsmeller import GDScriptAnalyzer

# Create analyzer
analyzer = GDScriptAnalyzer()

# Analyze a file
violations = analyzer.analyze_file('player.gd')

# Analyze a directory
violations = analyzer.analyze_directory('./scripts')

# Get formatted output
output = analyzer.format_violations(violations, format_type='text')
print(output)
```

## Configuration

Create a `.gdsmeller.json` file in your project root:

```json
{
  "max_line_length": 100,
  "disabled_rules": ["R003", "P003"]
}
```

### Configuration Options

- `max_line_length`: Maximum allowed line length (default: 100)
- `disabled_rules`: Array of rule IDs to disable

## Example Output

### Text Format
```
Found 3 issue(s):

scripts/player.gd:
  ✗ Line 15: [S001] Hardcoded password detected
    Category: security
  ⚠ Line 23: [P004] get_node() called in _process()
    Category: performance

Summary:
  Total issues: 3
  Errors: 1
  Warnings: 2
  Info: 0
```

### GitHub Actions Format
```
::error file=scripts/player.gd,line=15,title=[S001] Hardcoded Password::Hardcoded password detected
::warning file=scripts/player.gd,line=23,title=[P004] Get Node in Process::get_node() called in _process()
```

## Development

### Running Tests

```bash
python -m unittest discover tests
```

### Adding New Rules

1. Create a new rule class inheriting from `Rule`
2. Implement required properties: `rule_id`, `name`, `description`, `severity`, `category`
3. Implement the `check()` method
4. Add the rule to the appropriate module (readability, security, or performance)
5. Register the rule in `analyzer.py`

Example:

```python
from gdsmeller.rules.base import Rule, Severity, RuleCategory

class MyCustomRule(Rule):
    @property
    def rule_id(self) -> str:
        return "R005"
    
    @property
    def name(self) -> str:
        return "My Custom Rule"
    
    @property
    def description(self) -> str:
        return "Description of what this rule checks"
    
    @property
    def severity(self) -> Severity:
        return Severity.WARNING
    
    @property
    def category(self) -> RuleCategory:
        return RuleCategory.READABILITY
    
    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        # Implementation here
        return violations
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by similar linting tools for other languages
- Built for the Godot game engine community
