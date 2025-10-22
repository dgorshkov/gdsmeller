"""Security rules for GDScript."""

import re
from typing import List

from .base import Rule, RuleViolation, Severity, RuleCategory


class HardcodedPasswordRule(Rule):
    """Check for hardcoded passwords in the code."""
    
    @property
    def rule_id(self) -> str:
        return "S001"
    
    @property
    def name(self) -> str:
        return "Hardcoded Password"
    
    @property
    def description(self) -> str:
        return "Avoid hardcoding passwords in the code"
    
    @property
    def severity(self) -> Severity:
        return Severity.ERROR
    
    @property
    def category(self) -> RuleCategory:
        return RuleCategory.SECURITY
    
    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')
        
        # Pattern to detect password assignments
        password_patterns = [
            re.compile(r'password\s*=\s*["\'](.+)["\']', re.IGNORECASE),
            re.compile(r'passwd\s*=\s*["\'](.+)["\']', re.IGNORECASE),
            re.compile(r'pwd\s*=\s*["\'](.+)["\']', re.IGNORECASE),
        ]
        
        for i, line in enumerate(lines, 1):
            # Skip comments
            if line.strip().startswith('#'):
                continue
            
            for pattern in password_patterns:
                match = pattern.search(line)
                if match:
                    password_value = match.group(1)
                    # Skip if it's empty or looks like a placeholder
                    if password_value and password_value.lower() not in ['', 'password', 'your_password', 'your_password_here', 'changeme']:
                        violations.append(self.create_violation(
                            file_path=file_path,
                            line_number=i,
                            message="Hardcoded password detected. Use environment variables or secure storage instead",
                            code_snippet=line.strip()[:50]
                        ))
                        break
        
        return violations


class UnsafeEvalRule(Rule):
    """Check for use of unsafe eval or execute functions."""
    
    @property
    def rule_id(self) -> str:
        return "S002"
    
    @property
    def name(self) -> str:
        return "Unsafe Eval/Execute"
    
    @property
    def description(self) -> str:
        return "Avoid using Expression.parse() or execute() with untrusted input"
    
    @property
    def severity(self) -> Severity:
        return Severity.WARNING
    
    @property
    def category(self) -> RuleCategory:
        return RuleCategory.SECURITY
    
    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')
        
        # Patterns to detect potentially unsafe eval/execute
        unsafe_patterns = [
            re.compile(r'Expression\.parse\s*\(', re.IGNORECASE),
            re.compile(r'\.execute\s*\(', re.IGNORECASE),
        ]
        
        for i, line in enumerate(lines, 1):
            # Skip comments
            if line.strip().startswith('#'):
                continue
            
            for pattern in unsafe_patterns:
                if pattern.search(line):
                    violations.append(self.create_violation(
                        file_path=file_path,
                        line_number=i,
                        message="Potentially unsafe use of Expression.parse() or execute(). Ensure input is sanitized",
                        code_snippet=line.strip()[:50]
                    ))
                    break
        
        return violations


class SQLInjectionRiskRule(Rule):
    """Check for potential SQL injection vulnerabilities."""
    
    @property
    def rule_id(self) -> str:
        return "S003"
    
    @property
    def name(self) -> str:
        return "SQL Injection Risk"
    
    @property
    def description(self) -> str:
        return "Avoid string concatenation in SQL queries"
    
    @property
    def severity(self) -> Severity:
        return Severity.ERROR
    
    @property
    def category(self) -> RuleCategory:
        return RuleCategory.SECURITY
    
    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')
        
        # Pattern to detect SQL string concatenation
        sql_concat_pattern = re.compile(
            r'(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE).*(%s|%d|\+\s*\w+)',
            re.IGNORECASE
        )
        
        for i, line in enumerate(lines, 1):
            # Skip comments
            if line.strip().startswith('#'):
                continue
            
            # Check if line contains SQL keywords with potential concatenation
            if sql_concat_pattern.search(line):
                violations.append(self.create_violation(
                    file_path=file_path,
                    line_number=i,
                    message="Potential SQL injection risk. Use parameterized queries instead of string concatenation",
                    code_snippet=line.strip()[:50]
                ))
        
        return violations


class InsecureRandomRule(Rule):
    """Check for use of insecure random number generation for security purposes."""
    
    @property
    def rule_id(self) -> str:
        return "S004"
    
    @property
    def name(self) -> str:
        return "Insecure Random"
    
    @property
    def description(self) -> str:
        return "Use Crypto.random_bytes() for security-critical randomness, not randi()/randf()"
    
    @property
    def severity(self) -> Severity:
        return Severity.WARNING
    
    @property
    def category(self) -> RuleCategory:
        return RuleCategory.SECURITY
    
    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')
        
        # Look for security-related contexts using weak random
        security_keywords = ['token', 'key', 'password', 'secret', 'salt', 'nonce', 'session']
        random_functions = re.compile(r'\b(randi|randf|rand_range)\s*\(')
        
        for i, line in enumerate(lines, 1):
            # Skip comments
            if line.strip().startswith('#'):
                continue
            
            lower_line = line.lower()
            
            # Check if line uses weak random and contains security keywords
            if random_functions.search(line):
                if any(keyword in lower_line for keyword in security_keywords):
                    violations.append(self.create_violation(
                        file_path=file_path,
                        line_number=i,
                        message="Using insecure random function for security-critical purpose. Use Crypto.random_bytes() instead",
                        code_snippet=line.strip()[:50]
                    ))
        
        return violations
