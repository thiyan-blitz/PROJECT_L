"""
reporter.py - Reporter classes
OOP Concepts demonstrated: Abstract base class, Multiple implementations,
                           Open/Closed Principle
"""

from analyzer import AnalysisResult


class Reporter:
    """
    BASE CLASS for all reporters.
    Interview talking point:
    "This is the same pattern as Rule. I define a contract (report method),
    and each subclass fulfills that contract differently.
    Adding a new output format = just writing a new Reporter subclass."
    """

    def report(self, result: AnalysisResult, filename: str):
        raise NotImplementedError("Subclasses must implement report()")


# ─────────────────────────────────────────────
# SUBCLASS 1: Console Reporter
# ─────────────────────────────────────────────

class ConsoleReporter(Reporter):
    """Prints a colorful, human-readable report to the terminal."""

    # ANSI color codes for terminal colors
    COLORS = {
        "error":   "\033[91m",  # Red
        "warning": "\033[93m",  # Yellow
        "ok":      "\033[92m",  # Green
        "bold":    "\033[1m",
        "reset":   "\033[0m",
    }

    def report(self, result: AnalysisResult, filename: str):
        c = self.COLORS
        print(f"\n{c['bold']}codeguard — Analyzing: {filename}{c['reset']}")
        print("─" * 50)

        if not result.issues:
            print(f"{c['ok']}✅  No issues found! Great code.{c['reset']}")
        else:
            for issue in result.issues:
                color = c["error"] if issue.severity == "error" else c["warning"]
                icon  = "❌" if issue.severity == "error" else "⚠️ "
                print(f"{icon} {color}Line {issue.line:>3}{c['reset']}: {issue.message}")

        print("─" * 50)
        self._print_summary(result, c)

    def _print_summary(self, result: AnalysisResult, c: dict):
        score_color = c["ok"] if result.score >= 80 else (
                      c["warning"] if result.score >= 50 else c["error"])

        print(f"\n  Score  : {score_color}{c['bold']}{result.score}/100{c['reset']}")
        print(f"  Errors : {c['error']}{result.error_count}{c['reset']}")
        print(f"  Warnings: {c['warning']}{result.warning_count}{c['reset']}")
        print(f"  Lines  : {result.line_count}")
        print()


# ─────────────────────────────────────────────
# SUBCLASS 2: JSON Reporter
# ─────────────────────────────────────────────

class JSONReporter(Reporter):
    """
    Outputs the report in JSON format.
    Useful for piping codeguard into CI tools or other scripts.
    Interview talking point: "Same data, completely different format.
    I didn't touch the Analyzer or Rules to make this work."
    """

    def report(self, result: AnalysisResult, filename: str):
        import json

        output = {
            "file": filename,
            "score": result.score,
            "summary": {
                "errors": result.error_count,
                "warnings": result.warning_count,
                "total_issues": len(result.issues),
                "lines_analyzed": result.line_count,
            },
            "issues": [
                {
                    "line": issue.line,
                    "severity": issue.severity,
                    "rule": issue.rule,
                    "message": issue.message,
                }
                for issue in result.issues
            ]
        }

        print(json.dumps(output, indent=2))
