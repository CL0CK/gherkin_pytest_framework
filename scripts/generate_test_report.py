"""
Generates a test report PNG from Allure results using Painter.

Usage:
    poetry run python scripts/generate_test_report.py                           # CI: allure-results-merged
    poetry run python scripts/generate_test_report.py allure-results            # local run
    poetry run python scripts/generate_test_report.py allure-results --previous gh-pages/last_result.json

Output:
    reports/test-report.png
    reports/last_result.json
"""

import json
from datetime import datetime
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
    session_start = None

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
        if duration is None:
            stop = data.get("stop")
            start = data.get("start")
            if stop is not None and start is not None:
                duration = stop - start

        if duration is not None:
            total_duration += duration

        start = data.get("start")
        if start is not None and (session_start is None or start < session_start):
            session_start = start

    duration_minutes = int(total_duration // 60000)
    duration_seconds = int((total_duration % 60000) // 1000)
    duration_str = f"{duration_minutes}m {duration_seconds}s"

    session_date = ""
    if session_start is not None:
        session_date = datetime.fromtimestamp(session_start / 1000).strftime("%Y-%m-%d")

    return {
        "number_of_cases": statuses,
        "total_number_of_cases": total_cases,
        "application_version": "1.0.0",
        "test_session_date": session_date,
        "test_session_duration": duration_str,
    }


def main():
    args = sys.argv[1:]

    allure_dir = BASE_DIR / "allure-results-merged"
    previous_path = None

    i = 0
    while i < len(args):
        if args[i] == "--previous" and i + 1 < len(args):
            previous_path = Path(args[i + 1])
            i += 2
        elif not args[i].startswith("--"):
            allure_dir = BASE_DIR / args[i]
            i += 1
        else:
            i += 1

    report_dir = BASE_DIR / "reports"
    report_dir.mkdir(exist_ok=True)

    data = parse_allure_results(str(allure_dir))
    if not data:
        print("No Allure results found. Nothing to report.")
        return

    report_data = {"today": data}

    if previous_path and previous_path.exists():
        try:
            report_data["previous"] = json.loads(previous_path.read_text(encoding="utf-8"))
            print(f"Loaded previous results from: {previous_path}")
        except (json.JSONDecodeError, Exception) as e:
            print(f"Could not read previous results: {e}")

    from scripts.painter import Painter

    result = Painter.create_statistic_image(report_data, "chromium", "main")
    print(result)

    source = BASE_DIR / "statistic_image.png"
    dest = report_dir / "test-report.png"
    if source.exists():
        if dest.exists():
            dest.unlink()
        source.rename(dest)
        print(f"Report saved to: {dest}")
    else:
        print("Error: statistic_image.png not created")

    last_result = report_dir / "last_result.json"
    last_result.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Current result saved to: {last_result}")


if __name__ == "__main__":
    main()
