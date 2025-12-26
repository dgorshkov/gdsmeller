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
        loop_stack = []  # Stack to track loop indentation levels
        process_line = 0
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Check if we're entering a process function
            if re.match(r'func\s+(_process|_physics_process)\s*\(', stripped):
                in_process_func = True
                process_line = i
                loop_stack = []
            
            # Check if we're exiting the function
            if in_process_func and re.match(r'func\s+\w+\s*\(', stripped) and i != process_line:
                in_process_func = False
                loop_stack = []
            
            if in_process_func and stripped:
                # Get current line indentation
                indent = len(line) - len(line.lstrip())
                
                # Remove loops from stack that we've exited (based on indentation)
                loop_stack = [loop_indent for loop_indent in loop_stack if loop_indent < indent]
                
                # Check for loop keywords
                if re.match(r'(for|while)\s+', stripped):
                    loop_stack.append(indent)
                
                # Check for expensive operations in loops
                if loop_stack:
                    # Check for expensive operations
                    expensive_patterns = [
                        r'get_node\s*\(',
                        r'\$[A-Za-z_]',  # $ node reference (more specific)
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
        
        in_loop_stack = []  # Stack to track loop indentation levels
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            if stripped:
                # Get current line indentation
                indent = len(line) - len(line.lstrip())
                
                # Remove loops from stack that we've exited (based on indentation)
                in_loop_stack = [loop_indent for loop_indent in in_loop_stack if loop_indent < indent]
                
                # Check for loop keywords
                if re.match(r'(for|while)\s+', stripped):
                    in_loop_stack.append(indent)
                
                # Reset loop stack on function definition
                if re.match(r'func\s+\w+\s*\(', stripped):
                    in_loop_stack = []
                
                if in_loop_stack:
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
        
        # Track individual signal connections and disconnections.
        # Key format: "<target_expression>::<signal_literal>"
        connect_pattern = re.compile(
            r'(?P<target>\w+(?:\.\w+)*)\s*\.connect\(\s*(?P<signal>"[^"]*"|\'[^\']*\')'
        )
        disconnect_pattern = re.compile(
            r'(?P<target>\w+(?:\.\w+)*)\s*\.disconnect\(\s*(?P<signal>"[^"]*"|\'[^\']*\')'
        )
        
        connected_signals = {}  # key -> first line number where connected
        disconnected_signals = set()  # set of keys that are disconnected
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Ignore comments entirely
            if stripped.startswith('#'):
                continue
            
            # Find all connect calls on this line
            for match in connect_pattern.finditer(line):
                key = f"{match.group('target')}::{match.group('signal')}"
                # Only store the first occurrence line for reporting
                if key not in connected_signals:
                    connected_signals[key] = i
            
            # Find all disconnect calls on this line
            for match in disconnect_pattern.finditer(line):
                key = f"{match.group('target')}::{match.group('signal')}"
                disconnected_signals.add(key)
        
        # Report any signals that are connected but never disconnected
        for key, line_num in connected_signals.items():
            if key not in disconnected_signals:
                violations.append(self.create_violation(
                    file_path=file_path,
                    line_number=line_num,
                    message="Signal connected but no matching disconnect() found. Consider disconnecting in _exit_tree() to prevent memory leaks",
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
            if re.match(r'func\s+(_process|_physics_process)\s*\(', stripped):
                in_process_func = True
                process_line = i
            
            # Check if we're exiting the function
            if in_process_func and re.match(r'func\s+\w+\s*\(', stripped) and i != process_line:
                in_process_func = False
            
            if in_process_func:
                # Check for get_node calls or $ syntax (but not in signal context)
                if 'get_node(' in line or (re.search(r'\$[A-Za-z_]', line) and 'signal' not in line.lower()):
                    violations.append(self.create_violation(
                        file_path=file_path,
                        line_number=i,
                        message="get_node() or $ called in _process(). Cache the reference in _ready() for better performance",
                        code_snippet=line.strip()[:50]
                    ))
        
        return violations
