"""Performance rules for GDScript."""

import re
from typing import List

from .base import Rule, RuleViolation, Severity, RuleCategory


class ProcessInLoopRule(Rule):
    """Check for _process() or _physics_process() calls in loops."""
    
    @property
    def rule_id(self) -> str:
        return "P001"
    
    @property
    def name(self) -> str:
        return "Process in Loop"
    
    @property
    def description(self) -> str:
        return "Avoid expensive operations in loops within _process() or _physics_process()"
    
    @property
    def severity(self) -> Severity:
        return Severity.WARNING
    
    @property
    def category(self) -> RuleCategory:
        return RuleCategory.PERFORMANCE
    
    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')
        
        in_process_func = False
        loop_depth = 0
        process_line = 0
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Check if we're entering a process function
            if re.match(r'func\s+(_process|_physics_process)\s*\(', stripped, re.IGNORECASE):
                in_process_func = True
                process_line = i
                loop_depth = 0
            
            # Check if we're exiting the function
            if in_process_func and re.match(r'func\s+\w+\s*\(', stripped, re.IGNORECASE) and i != process_line:
                in_process_func = False
            
            if in_process_func:
                # Check for loop keywords
                if re.match(r'(for|while)\s+', stripped, re.IGNORECASE):
                    loop_depth += 1
                
                # Check for expensive operations in loops
                if loop_depth > 0:
                    # Check for expensive operations
                    expensive_patterns = [
                        r'get_node\s*\(',
                        r'\$',  # $ node reference
                        r'find_node\s*\(',
                        r'get_tree\s*\(',
                        r'instance\s*\(',
                    ]
                    
                    for pattern in expensive_patterns:
                        if re.search(pattern, line):
                            violations.append(self.create_violation(
                                file_path=file_path,
                                line_number=i,
                                message="Expensive operation in loop within _process() function. Cache results outside the loop",
                                code_snippet=line.strip()[:50]
                            ))
                            break
        
        return violations


class StringConcatenationInLoopRule(Rule):
    """Check for string concatenation in loops."""
    
    @property
    def rule_id(self) -> str:
        return "P002"
    
    @property
    def name(self) -> str:
        return "String Concatenation in Loop"
    
    @property
    def description(self) -> str:
        return "Avoid string concatenation in loops. Use Array.join() or PackedStringArray instead"
    
    @property
    def severity(self) -> Severity:
        return Severity.WARNING
    
    @property
    def category(self) -> RuleCategory:
        return RuleCategory.PERFORMANCE
    
    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')
        
        in_loop = False
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Check for loop keywords
            if re.match(r'(for|while)\s+', stripped, re.IGNORECASE):
                in_loop = True
            
            # Reset loop flag on function definition
            if re.match(r'func\s+\w+\s*\(', stripped, re.IGNORECASE):
                in_loop = False
            
            if in_loop:
                # Check for string concatenation using +=
                if re.search(r'\w+\s*\+=\s*["\']', line):
                    violations.append(self.create_violation(
                        file_path=file_path,
                        line_number=i,
                        message="String concatenation in loop detected. Use Array and join() for better performance",
                        code_snippet=line.strip()[:50]
                    ))
        
        return violations


class UnusedSignalConnectionRule(Rule):
    """Check for signals that might not be properly disconnected."""
    
    @property
    def rule_id(self) -> str:
        return "P003"
    
    @property
    def name(self) -> str:
        return "Signal Not Disconnected"
    
    @property
    def description(self) -> str:
        return "Signals connected with connect() should be disconnected in cleanup to prevent memory leaks"
    
    @property
    def severity(self) -> Severity:
        return Severity.INFO
    
    @property
    def category(self) -> RuleCategory:
        return RuleCategory.PERFORMANCE
    
    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')
        
        has_connect = False
        has_disconnect = False
        has_exit_tree = False
        connect_lines = []
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Check for connect calls
            if '.connect(' in line and not stripped.startswith('#'):
                has_connect = True
                connect_lines.append(i)
            
            # Check for disconnect calls
            if '.disconnect(' in line and not stripped.startswith('#'):
                has_disconnect = True
            
            # Check for _exit_tree function
            if re.match(r'func\s+_exit_tree\s*\(', stripped, re.IGNORECASE):
                has_exit_tree = True
        
        # If we have connects but no disconnects and no _exit_tree, warn
        if has_connect and not has_disconnect and not has_exit_tree:
            for line_num in connect_lines[:1]:  # Report only first occurrence
                violations.append(self.create_violation(
                    file_path=file_path,
                    line_number=line_num,
                    message="Signal connected but no disconnect() found. Consider disconnecting in _exit_tree() to prevent memory leaks",
                    code_snippet=lines[line_num - 1].strip()[:50]
                ))
        
        return violations


class GetNodeInProcessRule(Rule):
    """Check for repeated get_node() calls in _process() functions."""
    
    @property
    def rule_id(self) -> str:
        return "P004"
    
    @property
    def name(self) -> str:
        return "Get Node in Process"
    
    @property
    def description(self) -> str:
        return "Cache node references in _ready() instead of calling get_node() in _process()"
    
    @property
    def severity(self) -> Severity:
        return Severity.WARNING
    
    @property
    def category(self) -> RuleCategory:
        return RuleCategory.PERFORMANCE
    
    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')
        
        in_process_func = False
        process_line = 0
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Check if we're entering a process function
            if re.match(r'func\s+(_process|_physics_process)\s*\(', stripped, re.IGNORECASE):
                in_process_func = True
                process_line = i
            
            # Check if we're exiting the function
            if in_process_func and re.match(r'func\s+\w+\s*\(', stripped, re.IGNORECASE) and i != process_line:
                in_process_func = False
            
            if in_process_func:
                # Check for get_node calls or $ syntax
                if 'get_node(' in line or (re.search(r'\$\w+', line) and 'signal' not in line.lower()):
                    violations.append(self.create_violation(
                        file_path=file_path,
                        line_number=i,
                        message="get_node() or $ called in _process(). Cache the reference in _ready() for better performance",
                        code_snippet=line.strip()[:50]
                    ))
        
        return violations
