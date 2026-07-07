"""
Generates a test report PNG from Allure results using Painter.

Usage:
    poetry run python scripts/generate_test_report.py

Output:
    reports/test-report.png
"""

import json
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))


def parse_allure_results(allure_dir: str) -> dict:
    allure_path = Path(allure_dir)
    if not allure_path.exists():
        print(f"Allure results directory not found: {allure_dir}")
        return {}

    statuses = {"passed": 0, "failed": 0, "broken": 0, "skipped": 0, "expected_fail": 0}
    total_duration = 0
    total_cases = 0

    for result_file in allure_path.glob("*.json"):
        content = result_file.read_text(encoding="utf-8")
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            continue

        status = data.get("status", "")
        if status not in statuses:
            continue

        statuses[status] += 1
        total_cases += 1

        duration = data.get("duration")
        if duration is not None:
            total_duration += duration

    duration_minutes = int(total_duration // 60000)
    duration_seconds = int((total_duration % 60000) // 1000)
    duration_str = f"{duration_minutes}m {duration_seconds}s"

    return {
        "number_of_cases": statuses,
        "total_number_of_cases": total_cases,
        "application_version": "1.0.0",
        "test_session_date": Path(allure_dir).name,
        "test_session_duration": duration_str,
    }


def main():
    allure_dir = BASE_DIR / "allure-results-merged"
    report_dir = BASE_DIR / "reports"
    report_dir.mkdir(exist_ok=True)

    data = parse_allure_results(str(allure_dir))
    if not data:
        print("No Allure results found. Nothing to report.")
        return

    from scripts.painter import Painter

    report_data = {
        "today": data,
    }

    result = Painter.create_statistic_image(report_data, "chromium", "main")
    print(result)

    # Move to reports/
    source = BASE_DIR / "statistic_image.png"
    dest = report_dir / "test-report.png"
    if source.exists():
        if dest.exists():
            dest.unlink()
        source.rename(dest)
        print(f"Report saved to: {dest}")
    else:
        print("Error: statistic_image.png not created")


if __name__ == "__main__":
    main()
