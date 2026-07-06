"""
Scans all .feature files and tests to produce a coverage summary
of implemented Gherkin scenarios.

Usage:
    python scripts/check_unimplemented.py
"""

import os
import re
import sys
from pathlib import Path

from utils.gherkin_parser import GherkinFeature, parse_feature_file

os.environ["PYTHONIOENCODING"] = "utf-8"

BASE_DIR = Path(__file__).resolve().parent.parent
FEATURES_DIR = BASE_DIR / "features"
TESTS_DIR = BASE_DIR / "tests"


def get_all_feature_scenarios() -> dict[str, list[str]]:
    feature_scenarios: dict[str, list[str]] = {}

    for feature_file in sorted(FEATURES_DIR.glob("*.feature")):
        feature = parse_feature_file(feature_file.name)
        scenario_names = [s.name for s in feature.scenarios]
        feature_scenarios[feature_file.name] = scenario_names

    return feature_scenarios


def get_implemented_scenarios() -> dict[str, set[str]]:
    implemented: dict[str, set[str]] = {}

    test_files = list(TESTS_DIR.rglob("*.py"))
    pattern = re.compile(r'@Gherkin\(\s*["\']([^"\']+)["\']\s*,\s*["\']([^"\']+)["\']')

    for test_file in test_files:
        content = test_file.read_text(encoding="utf-8")
        for match in pattern.finditer(content):
            feature_file, scenario_name = match.group(1), match.group(2)
            if feature_file not in implemented:
                implemented[feature_file] = set()
            implemented[feature_file].add(scenario_name)

    return implemented


def main():
    all_scenarios = get_all_feature_scenarios()
    implemented = get_implemented_scenarios()

    if not all_scenarios:
        print("No .feature files found in features/")
        return

    header = f"{'Feature File':<25} | {'Total':>5} | {'Implemented':>11} | {'Unimplemented':>13} | {'Coverage':>8}"
    separator = "=" * len(header)

    total_all = 0
    implemented_all = 0
    unimplemented_all = 0
    rows: list[str] = []

    for feature_file, scenarios in all_scenarios.items():
        total = len(scenarios)
        implemented_set = implemented.get(feature_file, set())
        implemented_count = len(implemented_set)
        unimplemented_count = total - implemented_count
        coverage = (implemented_count / total * 100) if total > 0 else 0

        total_all += total
        implemented_all += implemented_count
        unimplemented_all += unimplemented_count

        row = f"{feature_file:<25} | {total:>5} | {implemented_count:>11} | {unimplemented_count:>13} | {coverage:>6.1f}%"
        rows.append(row)

    overall_coverage = (implemented_all / total_all * 100) if total_all > 0 else 0
    total_row = f"{'TOTAL':<25} | {total_all:>5} | {implemented_all:>11} | {unimplemented_all:>13} | {overall_coverage:>6.1f}%"

    separator_line = "=" * len(header)

    print()
    print(header)
    print(separator)
    for row in rows:
        print(row)
    print(separator_line)
    print(total_row)
    print()

    unimplemented_by_file: dict[str, list[str]] = {}
    for feature_file, scenarios in all_scenarios.items():
        implemented_set = implemented.get(feature_file, set())
        missing = [s for s in scenarios if s not in implemented_set]
        if missing:
            unimplemented_by_file[feature_file] = missing

    if unimplemented_by_file:
        print("UNIMPLEMENTED SCENARIOS:")
        print("-" * 40)
        for feature_file, scenarios in unimplemented_by_file.items():
            print(f"\n  {feature_file}:")
            for scenario in scenarios:
                print(f"    - {scenario}")
        print()
    else:
        print("All scenarios are implemented.")
        print()


if __name__ == "__main__":
    main()
