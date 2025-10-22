"""Tests for individual rules."""

import unittest

from gdsmeller.rules.readability import (
    LineTooLongRule, MissingClassDocstringRule,
    MissingFunctionDocstringRule, InconsistentIndentationRule
)
from gdsmeller.rules.security import (
    HardcodedPasswordRule, UnsafeEvalRule,
    SQLInjectionRiskRule, InsecureRandomRule
)
from gdsmeller.rules.performance import (
    ProcessInLoopRule, StringConcatenationInLoopRule,
    UnusedSignalConnectionRule, GetNodeInProcessRule
)


class TestReadabilityRules(unittest.TestCase):
    """Test readability rules."""
    
    def test_line_too_long_rule(self):
        """Test LineTooLongRule."""
        rule = LineTooLongRule(max_length=50)
        content = "var x = 1\n" + "var y = " + "a" * 100 + "\n"
        
        violations = rule.check("test.gd", content)
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].line_number, 2)
    
    def test_line_too_long_ignores_comments(self):
        """Test that LineTooLongRule ignores comment lines."""
        rule = LineTooLongRule(max_length=50)
        content = "# " + "a" * 100 + "\n"
        
        violations = rule.check("test.gd", content)
        self.assertEqual(len(violations), 0)
    
    def test_missing_class_docstring(self):
        """Test MissingClassDocstringRule."""
        rule = MissingClassDocstringRule()
        content = "class MyClass:\n\tvar x = 1\n"
        
        violations = rule.check("test.gd", content)
        self.assertEqual(len(violations), 1)
        self.assertIn("MyClass", violations[0].message)
    
    def test_class_with_docstring(self):
        """Test that classes with docstrings pass."""
        rule = MissingClassDocstringRule()
        content = "class MyClass:\n\t# This is a docstring\n\tvar x = 1\n"
        
        violations = rule.check("test.gd", content)
        self.assertEqual(len(violations), 0)
    
    def test_missing_function_docstring(self):
        """Test MissingFunctionDocstringRule."""
        rule = MissingFunctionDocstringRule()
        content = "func my_function():\n\tpass\n"
        
        violations = rule.check("test.gd", content)
        self.assertEqual(len(violations), 1)
    
    def test_private_function_no_docstring(self):
        """Test that private functions don't require docstrings."""
        rule = MissingFunctionDocstringRule()
        content = "func _private_function():\n\tpass\n"
        
        violations = rule.check("test.gd", content)
        self.assertEqual(len(violations), 0)
    
    def test_inconsistent_indentation(self):
        """Test InconsistentIndentationRule."""
        rule = InconsistentIndentationRule()
        content = "func test():\n\t\tvar x = 1\n    var y = 2\n"
        
        violations = rule.check("test.gd", content)
        self.assertEqual(len(violations), 1)


class TestSecurityRules(unittest.TestCase):
    """Test security rules."""
    
    def test_hardcoded_password(self):
        """Test HardcodedPasswordRule."""
        rule = HardcodedPasswordRule()
        content = 'var password = "secret123"\n'
        
        violations = rule.check("test.gd", content)
        self.assertEqual(len(violations), 1)
    
    def test_password_placeholder(self):
        """Test that password placeholders don't trigger."""
        rule = HardcodedPasswordRule()
        content = 'var password = "password"\n'
        
        violations = rule.check("test.gd", content)
        self.assertEqual(len(violations), 0)
    
    def test_unsafe_eval(self):
        """Test UnsafeEvalRule."""
        rule = UnsafeEvalRule()
        content = 'var expr = Expression.parse("2 + 2")\n'
        
        violations = rule.check("test.gd", content)
        self.assertEqual(len(violations), 1)
    
    def test_sql_injection(self):
        """Test SQLInjectionRiskRule."""
        rule = SQLInjectionRiskRule()
        content = 'var query = "SELECT * FROM users WHERE id = " + user_id\n'
        
        violations = rule.check("test.gd", content)
        self.assertEqual(len(violations), 1)
    
    def test_insecure_random(self):
        """Test InsecureRandomRule."""
        rule = InsecureRandomRule()
        content = 'var token = str(randi())\n'
        
        violations = rule.check("test.gd", content)
        self.assertEqual(len(violations), 1)


class TestPerformanceRules(unittest.TestCase):
    """Test performance rules."""
    
    def test_process_in_loop(self):
        """Test ProcessInLoopRule."""
        rule = ProcessInLoopRule()
        content = """func _process(delta):
\tfor i in range(10):
\t\tvar node = get_node("Player")
"""
        
        violations = rule.check("test.gd", content)
        self.assertEqual(len(violations), 1)
    
    def test_string_concatenation_in_loop(self):
        """Test StringConcatenationInLoopRule."""
        rule = StringConcatenationInLoopRule()
        content = """func build_string():
\tvar result = ""
\tfor i in range(10):
\t\tresult += "test"
"""
        
        violations = rule.check("test.gd", content)
        self.assertEqual(len(violations), 1)
    
    def test_unused_signal_connection(self):
        """Test UnusedSignalConnectionRule."""
        rule = UnusedSignalConnectionRule()
        content = """func _ready():
\tsignal_obj.connect("my_signal", self, "_on_signal")
"""
        
        violations = rule.check("test.gd", content)
        self.assertEqual(len(violations), 1)
    
    def test_signal_with_disconnect(self):
        """Test that signals with disconnect don't trigger."""
        rule = UnusedSignalConnectionRule()
        content = """func _ready():
\tsignal_obj.connect("my_signal", self, "_on_signal")

func _exit_tree():
\tsignal_obj.disconnect("my_signal", self, "_on_signal")
"""
        
        violations = rule.check("test.gd", content)
        self.assertEqual(len(violations), 0)
    
    def test_get_node_in_process(self):
        """Test GetNodeInProcessRule."""
        rule = GetNodeInProcessRule()
        content = """func _process(delta):
\tvar player = get_node("Player")
\tplayer.update()
"""
        
        violations = rule.check("test.gd", content)
        self.assertEqual(len(violations), 1)
    
    def test_get_node_in_ready(self):
        """Test that get_node in _ready is fine."""
        rule = GetNodeInProcessRule()
        content = """func _ready():
\tvar player = get_node("Player")
"""
        
        violations = rule.check("test.gd", content)
        self.assertEqual(len(violations), 0)


if __name__ == '__main__':
    unittest.main()
