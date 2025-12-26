"""GDSmeller - GDScript Static Analysis Tool."""

__version__ = "0.1.0"
__author__ = "dgorshkov"

from .analyzer import GDScriptAnalyzer
from .rules.base import Rule, RuleViolation, Severity

__all__ = ["GDScriptAnalyzer", "Rule", "RuleViolation", "Severity"]
