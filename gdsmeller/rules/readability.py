"""Readability rules for GDScript."""

import re
from typing import List

from .base import Rule, RuleViolation, Severity, RuleCategory


class LineTooLongRule(Rule):
    """Check for lines that are too long."""
    
    def __init__(self, max_length: int = 100):
        super().__init__()
        self.max_length = max_length
    
    @property
    def rule_id(self) -> str:
        return "R001"
    
    @property
    def name(self) -> str:
        return "Line Too Long"
    
    @property
    def description(self) -> str:
        return f"Lines should not exceed {self.max_length} characters"
    
    @property
    def severity(self) -> Severity:
        return Severity.WARNING
    
    @property
    def category(self) -> RuleCategory:
        return RuleCategory.READABILITY
    
    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Skip comment-only lines as they might contain long URLs
            stripped = line.strip()
            if stripped.startswith('#'):
                continue
            
            if len(line) > self.max_length:
                violations.append(self.create_violation(
                    file_path=file_path,
                    line_number=i,
                    message=f"Line exceeds {self.max_length} characters (found {len(line)})",
                    code_snippet=line[:50] + "..." if len(line) > 50 else line
                ))
        
        return violations


class MissingClassDocstringRule(Rule):
    """Check for classes without docstrings."""
    
    @property
    def rule_id(self) -> str:
        return "R002"
    
    @property
    def name(self) -> str:
        return "Missing Class Docstring"
    
    @property
    def description(self) -> str:
        return "Classes should have docstrings"
    
    @property
    def severity(self) -> Severity:
        return Severity.INFO
    
    @property
    def category(self) -> RuleCategory:
        return RuleCategory.READABILITY
    
    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')
        
        class_pattern = re.compile(r'^\s*class\s+(\w+)', re.IGNORECASE)
        comment_pattern = re.compile(r'^\s*#')
        
        i = 0
        while i < len(lines):
            line = lines[i]
            match = class_pattern.match(line)
            
            if match:
                class_name = match.group(1)
                # Check if next non-empty line is a comment
                has_docstring = False
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                
                if j < len(lines) and comment_pattern.match(lines[j]):
                    has_docstring = True
                
                if not has_docstring:
                    violations.append(self.create_violation(
                        file_path=file_path,
                        line_number=i + 1,
                        message=f"Class '{class_name}' is missing a docstring",
                        code_snippet=line.strip()
                    ))
            
            i += 1
        
        return violations


class MissingFunctionDocstringRule(Rule):
    """Check for functions without docstrings."""
    
    @property
    def rule_id(self) -> str:
        return "R003"
    
    @property
    def name(self) -> str:
        return "Missing Function Docstring"
    
    @property
    def description(self) -> str:
        return "Public functions should have docstrings"
    
    @property
    def severity(self) -> Severity:
        return Severity.INFO
    
    @property
    def category(self) -> RuleCategory:
        return RuleCategory.READABILITY
    
    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')
        
        # Match public functions (not starting with _)
        func_pattern = re.compile(r'^\s*func\s+([a-zA-Z][a-zA-Z0-9_]*)\s*\(', re.IGNORECASE)
        comment_pattern = re.compile(r'^\s*#')
        
        i = 0
        while i < len(lines):
            line = lines[i]
            match = func_pattern.match(line)
            
            if match:
                func_name = match.group(1)
                # Skip private functions (starting with _)
                if func_name.startswith('_'):
                    i += 1
                    continue
                
                # Check if next non-empty line is a comment
                has_docstring = False
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                
                if j < len(lines) and comment_pattern.match(lines[j]):
                    has_docstring = True
                
                if not has_docstring:
                    violations.append(self.create_violation(
                        file_path=file_path,
                        line_number=i + 1,
                        message=f"Function '{func_name}' is missing a docstring",
                        code_snippet=line.strip()
                    ))
            
            i += 1
        
        return violations


class InconsistentIndentationRule(Rule):
    """Check for inconsistent indentation (mixing tabs and spaces)."""
    
    @property
    def rule_id(self) -> str:
        return "R004"
    
    @property
    def name(self) -> str:
        return "Inconsistent Indentation"
    
    @property
    def description(self) -> str:
        return "Indentation should be consistent (tabs or spaces, not mixed)"
    
    @property
    def severity(self) -> Severity:
        return Severity.ERROR
    
    @property
    def category(self) -> RuleCategory:
        return RuleCategory.READABILITY
    
    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')
        
        uses_tabs = False
        uses_spaces = False
        
        for i, line in enumerate(lines, 1):
            if not line or not line[0].isspace():
                continue
            
            # Check leading whitespace
            leading = len(line) - len(line.lstrip())
            if leading > 0:
                if '\t' in line[:leading]:
                    uses_tabs = True
                if ' ' in line[:leading]:
                    uses_spaces = True
            
            # If both are used, it's inconsistent
            if uses_tabs and uses_spaces:
                violations.append(self.create_violation(
                    file_path=file_path,
                    line_number=i,
                    message="Mixing tabs and spaces for indentation",
                    code_snippet=line[:30]
                ))
                break
        
        return violations
