import sys
import argparse
from analyzer import Analyzer
from reporter import ConsoleReporter, JSONReporter


def main():
    parser = argparse.ArgumentParser(
        prog="codeguard",
        description="A Python code analyzer that checks for common issues."
    )

    subparsers = parser.add_subparsers(dest="command")

    # 'analyze' command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a Python file")
    analyze_parser.add_argument("file", help="Path to the Python file to analyze")
    analyze_parser.add_argument(
        "--format",
        choices=["console", "json"],
        default="console",
        help="Output format (default: console)"
    )

    args = parser.parse_args()

    if args.command == "analyze":
        run_analysis(args.file, args.format)
    else:
        parser.print_help()


def run_analysis(filepath: str, output_format: str):
    # Read the file
    try:
        with open(filepath, "r") as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)

    # Run analysis
    analyzer = Analyzer()
    result = analyzer.analyze(source_code)

    # Pick reporter based on format — polymorphism again!
    reporter_map = {
        "console": ConsoleReporter(),
        "json":    JSONReporter(),
    }
    reporter = reporter_map[output_format]
    reporter.report(result, filepath)

    # Exit with non-zero code if there are errors (useful for CI)
    if result.error_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
