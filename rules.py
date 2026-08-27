
import ast
import re
from abc import ABC, abstractmethod

class Rule(ABC):
    """
    BASE CLASS (Abstract-style)
    Every rule must have a name and must implement check().
    This is the parent that all other rules inherit from.
    """

    name = "Base Rule"
    description = "Base class — do not use directly"

    @abstractmethod
    def check(self, source_code: str) -> list:
        """
        Every subclass MUST override this method.
        Returns a list of Issue objects found in the source code.
        """
        pass


# ─────────────────────────────────────────────
# SUBCLASS 1: Naming Rule
# ─────────────────────────────────────────────

class NamingRule(Rule):
    

    name = "Naming Convention"
    description = "Function names should be lowercase with underscores (snake_case)"

    import re

def check(self, source_code: str) -> list:
    issues = []
    lines = source_code.splitlines()

    snake_case_pattern = re.compile(r'^[a-z_][a-z0-9_]*$')
    
    dunder_pattern = re.compile(r'^__[a-z0-9_]+__$')

    for line_num, line in enumerate(lines, start=1):
        match = re.match(r'\s*def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(.*?\):', line)
        if match:
            func_name = match.group(1)

            if dunder_pattern.match(func_name):
                continue

            if not snake_case_pattern.match(func_name):
                issues.append(Issue(
                    line=line_num,
                    message=f"Function '{func_name}' should be snake_case",
                    severity="warning",
                    rule=self.name
                ))

        return issues


# ─────────────────────────────────────────────
# SUBCLASS 2: Complexity Rule
# ─────────────────────────────────────────────

class ComplexityRule(Rule):
    name = "Function Length"
    description = "Functions should ideally be under 30 lines"

    def __init__(self, max_lines: int = 30):
        self.max_lines = max_lines  

    def check(self, source_code: str) -> list:
        issues = []

        try:
            tree = ast.parse(source_code)
        except SyntaxError:
            return []  

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_length = node.end_lineno - node.lineno
                if func_length > self.max_lines:
                    issues.append(Issue(
                        line=node.lineno,
                        message=f"Function '{node.name}' is {func_length} lines (max: {self.max_lines})",
                        severity="warning",
                        rule=self.name
                    ))

        return issues


# ─────────────────────────────────────────────
# SUBCLASS 3: Security Rule
# ─────────────────────────────────────────────

class SecurityRule(Rule):
    """
    SUBCLASS - inherits from Rule
    Catches common Python anti-patterns that can hide bugs.
    Interview talking point: "I used a list of patterns so adding
    new security checks is just adding to the list — Open/Closed principle."
    """

    name = "Security & Best Practices"
    description = "Detects bare except clauses and other anti-patterns"

    # Patterns to look for (easy to extend!)
    PATTERNS = [
        (r'\bexcept\s*:', "Bare 'except:' hides all errors — use 'except Exception'"),
        (r'\beval\s*\(', "Avoid eval() — it can execute arbitrary code"),
        (r'\bexec\s*\(', "Avoid exec() — it can execute arbitrary code"),
        (r'print\s*\(.*password', "Possible password printed to console"),
    ]

    def check(self, source_code: str) -> list:
        issues = []
        lines = source_code.splitlines()

        for line_num, line in enumerate(lines, start=1):
            for pattern, message in self.PATTERNS:
                if re.search(pattern, line):
                    issues.append(Issue(
                        line=line_num,
                        message=message,
                        severity="error",
                        rule=self.name
                    ))

        return issues


# ─────────────────────────────────────────────
# Helper: Issue data class
# ─────────────────────────────────────────────
from dataclasses import dataclass

@dataclass

class Issue:
    """
    Represents a single problem found in the code.
    Interview talking point: "I separated the data (Issue) from
    the logic (Rule) — Single Responsibility Principle."
    """

    line: int
    message: str
    severity: str
    rule: str

    def __repr__(self):
        return f"Issue(line={self.line}, severity='{self.severity}')"
