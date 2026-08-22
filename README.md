# codeguard 🛡️

A lightweight Python code analyzer that scans `.py` files for common issues — bad naming, overly long functions, and risky security patterns — and reports them with a quality score.

Built as a hands-on demonstration of core Object-Oriented Programming concepts in Python: abstraction, inheritance, polymorphism, composition, and encapsulation.

```
codeguard — Analyzing: sample_bad.py
──────────────────────────────────────────────────
⚠️  Line   6: Function 'GetUserData' should be snake_case
❌ Line  10: Bare 'except:' hides all errors — use 'except Exception'
⚠️  Line  15: Function 'ProcessOrders' should be snake_case
❌ Line  47: Possible password printed to console
──────────────────────────────────────────────────

  Score  : 54/100
  Errors : 2
  Warnings: 2
  Lines  : 53
```

## Features

- **Naming convention checks** — flags function names that aren't `snake_case`
- **Complexity checks** — flags functions longer than a configurable line limit
- **Security checks** — flags bare `except:` clauses, `eval()`, `exec()`, and passwords printed to the console
- **Quality score** — a 0–100 score based on the number and severity of issues found
- **Two output formats** — human-friendly console output or machine-readable JSON (for piping into CI tools)
- **Non-zero exit code on errors** — so it can be dropped straight into a CI pipeline as a gate

## Project structure

```
codeguard/
├── codeguard.py       # CLI entry point
├── analyzer.py         # Analyzer + AnalysisResult (composition)
├── rules.py            # Rule base class + NamingRule, ComplexityRule, SecurityRule, Issue
├── reporter.py          # Reporter base class + ConsoleReporter, JSONReporter
├── sample_bad.py        # Example file with intentional issues, for testing
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

- Python 3.9+
- No third-party dependencies — standard library only

## Installation

```bash
git clone https://github.com/<your-username>/codeguard.git
cd codeguard
```

No `pip install` needed — just run it with Python directly.

## Usage

Analyze a file with the default console output:

```bash
python codeguard.py analyze sample_bad.py
```

Get JSON output instead (handy for CI or scripting):

```bash
python codeguard.py analyze sample_bad.py --format json
```

Try it on the included clean/messy example, or point it at any Python file in your own project:

```bash
python codeguard.py analyze path/to/your_file.py
```

The command exits with status code `1` if any errors are found (useful for failing a CI build), and `0` otherwise.

## How it works

1. **`Rule` (abstract base class)** defines the contract every check must follow — a `check(source_code)` method that returns a list of `Issue` objects.
2. **`NamingRule`, `ComplexityRule`, and `SecurityRule`** each inherit from `Rule` and override `check()` with their own logic — a straightforward example of **inheritance** and **polymorphism**.
3. **`Analyzer`** doesn't inherit from `Rule` — it *has a* list of rules (**composition**) and runs each one polymorphically, without knowing or caring what each rule actually checks for.
4. **`Reporter` (base class)** defines a `report()` contract; **`ConsoleReporter`** and **`JSONReporter`** each implement it differently, so adding a new output format never requires touching the analysis logic.
5. **`Issue`** is a simple `dataclass` that holds the data for a single finding, kept separate from the logic that produces it (Single Responsibility Principle).

## Extending codeguard

Adding a new rule is just a new subclass — no existing code needs to change:

```python
from rules import Rule, Issue

class TodoRule(Rule):
    name = "TODO Comments"
    description = "Flags leftover TODO comments"

    def check(self, source_code: str) -> list:
        issues = []
        for line_num, line in enumerate(source_code.splitlines(), start=1):
            if "TODO" in line:
                issues.append(Issue(
                    line=line_num,
                    message="Leftover TODO comment",
                    severity="warning",
                    rule=self.name
                ))
        return issues
```

Then register it with the analyzer:

```python
analyzer = Analyzer()
analyzer.add_rule(TodoRule())
```

## License

MIT — feel free to use, modify, and share.
