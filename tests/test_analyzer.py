"""Tests for the GDScript analyzer."""

import unittest
import tempfile
import os

from gdsmeller.analyzer import GDScriptAnalyzer


class TestGDScriptAnalyzer(unittest.TestCase):
    """Test cases for GDScriptAnalyzer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = GDScriptAnalyzer()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temp directory
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def create_temp_file(self, content: str, filename: str = "test.gd") -> str:
        """Create a temporary GDScript file for testing."""
        file_path = os.path.join(self.temp_dir, filename)
        with open(file_path, 'w') as f:
            f.write(content)
        return file_path
    
    def test_clean_file(self):
        """Test that a clean file produces no violations."""
        content = """extends Node

# This is a well-formed GDScript file
func _ready():
\t# Initialize
\tpass
"""
        file_path = self.create_temp_file(content)
        violations = self.analyzer.analyze_file(file_path)
        self.assertEqual(len(violations), 0)
    
    def test_line_too_long(self):
        """Test detection of lines that are too long."""
        long_line = "var x = " + "a" * 150
        content = f"""extends Node

{long_line}
"""
        file_path = self.create_temp_file(content)
        violations = self.analyzer.analyze_file(file_path)
        
        # Should find at least one violation for the long line
        self.assertTrue(any(v.rule_id == "R001" for v in violations))
    
    def test_missing_class_docstring(self):
        """Test detection of missing class docstrings."""
        content = """extends Node

class MyClass:
\tvar x = 5
"""
        file_path = self.create_temp_file(content)
        violations = self.analyzer.analyze_file(file_path)
        
        # Should find missing docstring
        self.assertTrue(any(v.rule_id == "R002" for v in violations))
    
    def test_missing_function_docstring(self):
        """Test detection of missing function docstrings."""
        content = """extends Node

func my_function():
\tpass
"""
        file_path = self.create_temp_file(content)
        violations = self.analyzer.analyze_file(file_path)
        
        # Should find missing docstring
        self.assertTrue(any(v.rule_id == "R003" for v in violations))
    
    def test_hardcoded_password(self):
        """Test detection of hardcoded passwords."""
        content = """extends Node

var password = "secret123"
"""
        file_path = self.create_temp_file(content)
        violations = self.analyzer.analyze_file(file_path)
        
        # Should find hardcoded password
        self.assertTrue(any(v.rule_id == "S001" for v in violations))
    
    def test_unsafe_eval(self):
        """Test detection of unsafe eval usage."""
        content = """extends Node

func test():
\tvar expr = Expression.parse("2 + 2")
"""
        file_path = self.create_temp_file(content)
        violations = self.analyzer.analyze_file(file_path)
        
        # Should find unsafe eval
        self.assertTrue(any(v.rule_id == "S002" for v in violations))
    
    def test_get_node_in_process(self):
        """Test detection of get_node in _process."""
        content = """extends Node

func _process(delta):
\tvar player = get_node("Player")
\tplayer.update()
"""
        file_path = self.create_temp_file(content)
        violations = self.analyzer.analyze_file(file_path)
        
        # Should find get_node in process
        self.assertTrue(any(v.rule_id == "P004" for v in violations))
    
    def test_analyze_directory(self):
        """Test analyzing a directory of files."""
        # Create multiple test files
        self.create_temp_file("var password = 'test123'", "file1.gd")
        self.create_temp_file("func test():\n\tpass", "file2.gd")
        
        violations = self.analyzer.analyze_directory(self.temp_dir)
        
        # Should find violations from multiple files
        self.assertGreater(len(violations), 0)
    
    def test_summary(self):
        """Test violation summary generation."""
        content = """extends Node

var password = "secret"
func my_function():
\tpass
"""
        file_path = self.create_temp_file(content)
        violations = self.analyzer.analyze_file(file_path)
        
        summary = self.analyzer.get_summary(violations)
        
        self.assertIn('total', summary)
        self.assertIn('by_severity', summary)
        self.assertIn('by_category', summary)
        self.assertIn('by_file', summary)
    
    def test_format_text(self):
        """Test text formatting."""
        content = "var password = 'test123'"
        file_path = self.create_temp_file(content)
        violations = self.analyzer.analyze_file(file_path)
        
        output = self.analyzer.format_violations(violations, 'text')
        self.assertIsInstance(output, str)
        self.assertGreater(len(output), 0)
    
    def test_format_json(self):
        """Test JSON formatting."""
        content = "var password = 'test123'"
        file_path = self.create_temp_file(content)
        violations = self.analyzer.analyze_file(file_path)
        
        output = self.analyzer.format_violations(violations, 'json')
        self.assertIsInstance(output, str)
        
        # Should be valid JSON
        import json
        data = json.loads(output)
        self.assertIn('violations', data)
        self.assertIn('summary', data)
    
    def test_format_github(self):
        """Test GitHub Actions format."""
        content = "var password = 'test123'"
        file_path = self.create_temp_file(content)
        violations = self.analyzer.analyze_file(file_path)
        
        output = self.analyzer.format_violations(violations, 'github')
        self.assertIsInstance(output, str)
        # Should contain GitHub annotation markers
        self.assertTrue('::' in output or 'No issues' in output)
    
    def test_disabled_rules(self):
        """Test that disabled rules are not applied."""
        config = {'disabled_rules': ['R001']}
        analyzer = GDScriptAnalyzer(config)
        
        # Create file with long line
        long_line = "var x = " + "a" * 150
        content = f"extends Node\n\n{long_line}\n"
        file_path = self.create_temp_file(content)
        
        violations = analyzer.analyze_file(file_path)
        
        # Should not find R001 violation
        self.assertFalse(any(v.rule_id == "R001" for v in violations))


if __name__ == '__main__':
    unittest.main()
