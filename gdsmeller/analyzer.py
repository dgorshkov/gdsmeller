"""Main analyzer for GDScript files."""

import os
from pathlib import Path
from typing import List, Dict, Optional
import json

from .rules.base import Rule, RuleViolation, Severity
from .rules import readability, security, performance


class GDScriptAnalyzer:
    """Analyzes GDScript files for code smells and issues."""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the analyzer.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.rules: List[Rule] = []
        self._load_rules()
    
    def _load_rules(self):
        """Load all available rules."""
        # Readability rules
        self.rules.append(readability.LineTooLongRule(
            max_length=self.config.get('max_line_length', 100)
        ))
        self.rules.append(readability.MissingClassDocstringRule())
        self.rules.append(readability.MissingFunctionDocstringRule())
        self.rules.append(readability.InconsistentIndentationRule())
        
        # Security rules
        self.rules.append(security.HardcodedPasswordRule())
        self.rules.append(security.UnsafeEvalRule())
        self.rules.append(security.SQLInjectionRiskRule())
        self.rules.append(security.InsecureRandomRule())
        
        # Performance rules
        self.rules.append(performance.ProcessInLoopRule())
        self.rules.append(performance.StringConcatenationInLoopRule())
        self.rules.append(performance.UnusedSignalConnectionRule())
        self.rules.append(performance.GetNodeInProcessRule())
        
        # Filter rules based on configuration
        disabled_rules = self.config.get('disabled_rules', [])
        self.rules = [rule for rule in self.rules if rule.rule_id not in disabled_rules]
    
    def analyze_file(self, file_path: str) -> List[RuleViolation]:
        """
        Analyze a single GDScript file.
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            List of rule violations found
        """
        violations = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for rule in self.rules:
                if rule.enabled:
                    violations.extend(rule.check(file_path, content))
        
        except Exception as e:
            import sys
            print(f"Error analyzing {file_path}: {e}", file=sys.stderr)
        
        return violations
    
    def analyze_directory(self, directory: str) -> List[RuleViolation]:
        """
        Analyze all GDScript files in a directory.
        
        Args:
            directory: Path to the directory to analyze
            
        Returns:
            List of all rule violations found
        """
        violations = []
        path = Path(directory)
        
        # Find all .gd files
        for gd_file in path.rglob('*.gd'):
            violations.extend(self.analyze_file(str(gd_file)))
        
        return violations
    
    def analyze(self, path: str) -> List[RuleViolation]:
        """
        Analyze a file or directory.
        
        Args:
            path: Path to file or directory
            
        Returns:
            List of all rule violations found
        """
        if os.path.isfile(path):
            return self.analyze_file(path)
        elif os.path.isdir(path):
            return self.analyze_directory(path)
        else:
            raise ValueError(f"Path {path} is not a valid file or directory")
    
    def get_summary(self, violations: List[RuleViolation]) -> Dict:
        """
        Get a summary of violations.
        
        Args:
            violations: List of violations
            
        Returns:
            Dictionary with summary statistics
        """
        summary = {
            'total': len(violations),
            'by_severity': {},
            'by_category': {},
            'by_file': {}
        }
        
        for violation in violations:
            # Count by severity
            severity = violation.severity.value
            summary['by_severity'][severity] = summary['by_severity'].get(severity, 0) + 1
            
            # Count by category
            category = violation.category.value
            summary['by_category'][category] = summary['by_category'].get(category, 0) + 1
            
            # Count by file
            file_path = violation.file_path
            summary['by_file'][file_path] = summary['by_file'].get(file_path, 0) + 1
        
        return summary
    
    def format_violations(self, violations: List[RuleViolation], format_type: str = 'text') -> str:
        """
        Format violations for output.
        
        Args:
            violations: List of violations
            format_type: Output format ('text', 'json', 'github')
            
        Returns:
            Formatted string
        """
        if format_type == 'json':
            return self._format_json(violations)
        elif format_type == 'github':
            return self._format_github(violations)
        else:
            return self._format_text(violations)
    
    def _format_text(self, violations: List[RuleViolation]) -> str:
        """Format violations as plain text."""
        if not violations:
            return "✓ No issues found!"
        
        output = []
        output.append(f"Found {len(violations)} issue(s):\n")
        
        # Group by file
        by_file = {}
        for v in violations:
            if v.file_path not in by_file:
                by_file[v.file_path] = []
            by_file[v.file_path].append(v)
        
        for file_path, file_violations in sorted(by_file.items()):
            output.append(f"\n{file_path}:")
            for v in sorted(file_violations, key=lambda x: x.line_number):
                severity_icon = {
                    Severity.ERROR: '✗',
                    Severity.WARNING: '⚠',
                    Severity.INFO: 'ℹ'
                }.get(v.severity, '•')
                
                output.append(f"  {severity_icon} Line {v.line_number}: [{v.rule_id}] {v.message}")
                output.append(f"    Category: {v.category.value}")
        
        summary = self.get_summary(violations)
        output.append(f"\n\nSummary:")
        output.append(f"  Total issues: {summary['total']}")
        output.append(f"  Errors: {summary['by_severity'].get('error', 0)}")
        output.append(f"  Warnings: {summary['by_severity'].get('warning', 0)}")
        output.append(f"  Info: {summary['by_severity'].get('info', 0)}")
        
        return '\n'.join(output)
    
    def _format_json(self, violations: List[RuleViolation]) -> str:
        """Format violations as JSON."""
        data = {
            'violations': [
                {
                    'rule_id': v.rule_id,
                    'rule_name': v.rule_name,
                    'severity': v.severity.value,
                    'category': v.category.value,
                    'message': v.message,
                    'file': v.file_path,
                    'line': v.line_number,
                    'column': v.column,
                    'code_snippet': v.code_snippet
                }
                for v in violations
            ],
            'summary': self.get_summary(violations)
        }
        return json.dumps(data, indent=2)
    
    def _format_github(self, violations: List[RuleViolation]) -> str:
        """Format violations as GitHub Actions annotations."""
        if not violations:
            return "✓ No issues found!"
        
        output = []
        for v in violations:
            # GitHub Actions annotation format
            level = {
                Severity.ERROR: 'error',
                Severity.WARNING: 'warning',
                Severity.INFO: 'notice'
            }.get(v.severity, 'notice')
            
            output.append(
                f"::{level} file={v.file_path},line={v.line_number},"
                f"title=[{v.rule_id}] {v.rule_name}::{v.message}"
            )
        
        # Add summary
        summary = self.get_summary(violations)
        output.append(f"\n📊 Analysis Summary:")
        output.append(f"- Total issues: {summary['total']}")
        output.append(f"- Errors: {summary['by_severity'].get('error', 0)}")
        output.append(f"- Warnings: {summary['by_severity'].get('warning', 0)}")
        output.append(f"- Info: {summary['by_severity'].get('info', 0)}")
        
        return '\n'.join(output)
