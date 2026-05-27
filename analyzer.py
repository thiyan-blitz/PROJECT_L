"""
analyzer.py - The Analyzer class
OOP Concepts demonstrated: Composition (has-a relationship), Single Responsibility
"""

from rules import Rule, NamingRule, ComplexityRule, SecurityRule


class Analyzer:
    """
    COMPOSITION example — Analyzer doesn't inherit from Rule,
    it CONTAINS a list of rules. This is the "has-a" relationship.

    Interview talking point:
    "The Analyzer doesn't know or care what rules exist.
    You can add or remove rules without changing the Analyzer at all.
    That's the power of composition + polymorphism."
    """

    def __init__(self):
        # The Analyzer "has" a list of rules — Composition
        self.rules: list[Rule] = [
            NamingRule(),
            ComplexityRule(max_lines=30),
            SecurityRule(),
        ]

    def add_rule(self, rule: Rule):
        """Easily plug in new rules without changing this class."""
        self.rules.append(rule)

    def analyze(self, source_code: str) -> "AnalysisResult":
        """
        Run every rule against the source code.
        Polymorphism in action: each rule's check() behaves differently,
        but we call them all the same way.
        """
        all_issues = []

        for rule in self.rules:
            issues = rule.check(source_code)  # Polymorphic call
            all_issues.extend(issues)

        # Sort issues by line number for clean output
        all_issues.sort(key=lambda i: i.line)

        return AnalysisResult(issues=all_issues, source_code=source_code)


class AnalysisResult:
    """
    Holds the result of an analysis run.
    Interview talking point: "I separated the result data from
    the analysis logic — makes it easy to display results in
    different ways (console, JSON, HTML) without changing the core logic."
    """

    def __init__(self, issues: list, source_code: str):
        self.issues = issues
        self.line_count = len(source_code.splitlines())

    @property
    def score(self) -> int:
        """
        Calculates a code quality score out of 100.
        Errors cost more than warnings.
        """
        penalty = 0
        for issue in self.issues:
            if issue.severity == "error":
                penalty += 15
            else:
                penalty += 8
        return max(0, 100 - penalty)

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "warning")
