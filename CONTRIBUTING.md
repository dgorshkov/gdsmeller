# Contributing to GDSmeller

Thank you for your interest in contributing to GDSmeller! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork and clone the repository:
```bash
git clone https://github.com/YOUR-USERNAME/gdsmeller.git
cd gdsmeller
```

2. GDSmeller uses only Python standard library, so no additional dependencies are needed for core functionality.

3. Run the tests to ensure everything is working:
```bash
python -m unittest discover tests -v
```

## Project Structure

```
gdsmeller/
├── action.yml              # GitHub Action definition
├── requirements.txt        # Python dependencies
├── gdsmeller/
│   ├── __init__.py        # Package initialization
│   ├── main.py            # CLI entry point
│   ├── analyzer.py        # Main analyzer class
│   └── rules/
│       ├── __init__.py
│       ├── base.py        # Base classes for rules
│       ├── readability.py # Readability rules
│       ├── security.py    # Security rules
│       └── performance.py # Performance rules
├── tests/
│   ├── test_analyzer.py   # Analyzer tests
│   └── test_rules.py      # Individual rule tests
└── examples/              # Example GDScript files
```

## Adding a New Rule

1. **Choose the appropriate category:**
   - Readability: Code style and documentation
   - Security: Security vulnerabilities
   - Performance: Performance issues
   - Maintainability: Code maintainability
   - Best Practices: GDScript best practices

2. **Create the rule class:**

```python
# In gdsmeller/rules/readability.py (or appropriate file)

class MyNewRule(Rule):
    """Brief description of what this rule checks."""
    
    @property
    def rule_id(self) -> str:
        # Use next available ID in category (R005, S005, P005, etc.)
        return "R005"
    
    @property
    def name(self) -> str:
        return "My New Rule"
    
    @property
    def description(self) -> str:
        return "Detailed description of what this rule checks"
    
    @property
    def severity(self) -> Severity:
        # ERROR, WARNING, or INFO
        return Severity.WARNING
    
    @property
    def category(self) -> RuleCategory:
        return RuleCategory.READABILITY
    
    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Your checking logic here
            if line.strip().startswith('bad_pattern'):
                violations.append(self.create_violation(
                    file_path=file_path,
                    line_number=i,
                    message="Description of the violation",
                    code_snippet=line.strip()
                ))
        
        return violations
```

3. **Register the rule in `analyzer.py`:**

```python
def _load_rules(self):
    # ... existing rules ...
    self.rules.append(readability.MyNewRule())
```

4. **Add tests:**

```python
# In tests/test_rules.py

def test_my_new_rule(self):
    """Test MyNewRule."""
    rule = MyNewRule()
    content = "bad_pattern here\n"
    
    violations = rule.check("test.gd", content)
    self.assertEqual(len(violations), 1)
```

5. **Update documentation:**
   - Add rule description to `RULES.md`
   - Include examples of good and bad code

## Testing

Run all tests:
```bash
python -m unittest discover tests -v
```

Run specific test file:
```bash
python -m unittest tests.test_rules -v
```

Run specific test:
```bash
python -m unittest tests.test_rules.TestReadabilityRules.test_my_new_rule -v
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write clear docstrings for public functions and classes
- Keep functions focused and single-purpose

## Pull Request Process

1. **Create a feature branch:**
```bash
git checkout -b feature/my-new-rule
```

2. **Make your changes:**
   - Write code
   - Add tests
   - Update documentation

3. **Run tests:**
```bash
python -m unittest discover tests -v
```

4. **Test the tool manually:**
```bash
python -m gdsmeller.main --path examples/
```

5. **Commit your changes:**
```bash
git add .
git commit -m "Add rule R005: My New Rule"
```

6. **Push to your fork:**
```bash
git push origin feature/my-new-rule
```

7. **Create a Pull Request:**
   - Go to GitHub and create a PR from your fork
   - Provide a clear description of the changes
   - Reference any related issues

## PR Checklist

- [ ] Tests added/updated and passing
- [ ] Documentation updated (README.md, RULES.md)
- [ ] Code follows project style guidelines
- [ ] Commit messages are clear and descriptive
- [ ] Rule IDs follow the naming convention
- [ ] Examples included in documentation

## Rule ID Conventions

- **R-series**: Readability (R001, R002, ...)
- **S-series**: Security (S001, S002, ...)
- **P-series**: Performance (P001, P002, ...)
- **M-series**: Maintainability (M001, M002, ...)
- **B-series**: Best Practices (B001, B002, ...)

Use the next available number in the appropriate series.

## Severity Levels

- **ERROR**: Critical issues that should always be fixed (e.g., security vulnerabilities)
- **WARNING**: Important issues that should be addressed (e.g., performance problems)
- **INFO**: Suggestions for improvement (e.g., missing documentation)

## Questions or Problems?

- Open an issue on GitHub
- Check existing issues and discussions
- Review the documentation in README.md and RULES.md

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
