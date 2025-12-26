"""Base classes for rules."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class Severity(Enum):
    """Severity levels for rule violations."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class RuleCategory(Enum):
    """Categories for organizing rules."""
    READABILITY = "readability"
    SECURITY = "security"
    PERFORMANCE = "performance"
    MAINTAINABILITY = "maintainability"
    BEST_PRACTICES = "best_practices"


@dataclass
class RuleViolation:
    """Represents a violation of a rule."""
    rule_id: str
    rule_name: str
    severity: Severity
    category: RuleCategory
    message: str
    file_path: str
    line_number: int
    column: Optional[int] = None
    code_snippet: Optional[str] = None


class Rule(ABC):
    """Base class for all rules."""
    
    def __init__(self):
        self.enabled = True
    
    @property
    @abstractmethod
    def rule_id(self) -> str:
        """Unique identifier for the rule."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name of the rule."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Description of what the rule checks."""
        pass
    
    @property
    @abstractmethod
    def severity(self) -> Severity:
        """Default severity level for violations."""
        pass
    
    @property
    @abstractmethod
    def category(self) -> RuleCategory:
        """Category this rule belongs to."""
        pass
    
    @abstractmethod
    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        """
        Check the file content for rule violations.
        
        Args:
            file_path: Path to the file being checked
            content: Content of the file
            
        Returns:
            List of rule violations found
        """
        pass
    
    def create_violation(
        self,
        file_path: str,
        line_number: int,
        message: str,
        column: Optional[int] = None,
        code_snippet: Optional[str] = None
    ) -> RuleViolation:
        """Helper method to create a violation."""
        return RuleViolation(
            rule_id=self.rule_id,
            rule_name=self.name,
            severity=self.severity,
            category=self.category,
            message=message,
            file_path=file_path,
            line_number=line_number,
            column=column,
            code_snippet=code_snippet
        )
