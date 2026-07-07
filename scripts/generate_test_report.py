import argparse
import json
import sys

try:
    import tomllib
except ImportError:
    import tomllib as tomllib
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))


def get_project_version() -> str:
    """Автоматически считывает версию из pyproject.toml проекта Poetry."""
    try:
        pyproject_path = BASE_DIR / "pyproject.toml"
        if pyproject_path.exists():
            with open(pyproject_path, "rb") as f:
                data = tomllib.load(f)
            return data["tool"]["poetry"]["version"]
    except Exception:
        pass
    return "1.0.0"


def parse_allure_results(allure_dir: str, app_version: str) -> dict:
    allure_path = Path(allure_dir)
    if not allure_path.exists():
        print(f"Allure results directory not found: {allure_dir}")
        return {}

    statuses = {"passed": 0, "failed": 0, "broken": 0, "skipped": 0, "expected_fail": 0}
    total_cases = 0

    session_start = None
    session_end = None

    for result_file in allure_path.glob("*.json"):
        if "-container.json" in result_file.name:
            continue

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

        start = data.get("start")
        stop = data.get("stop")

        if start is not None and (session_start is None or start < session_start):
            session_start = start
        if stop is not None and (session_end is None or stop > session_end):
            session_end = stop

    if session_start and session_end:
        total_duration = session_end - session_start
    else:
        total_duration = 0

    duration_minutes = int(total_duration // 60000)
    duration_seconds = int((total_duration % 60000) // 1000)
    duration_str = f"{duration_minutes}m {duration_seconds}s"

    session_date = ""
    if session_start is not None:
        session_date = datetime.fromtimestamp(session_start / 1000).strftime("%Y-%m-%d")

    return {
        "number_of_cases": statuses,
        "total_number_of_cases": total_cases,
        "application_version": app_version,
        "test_session_date": session_date,
        "test_session_duration": duration_str,
    }


def main():
    parser = argparse.ArgumentParser(description="Generate PNG report from Allure results.")
    parser.add_argument("allure_dir", nargs="?", default="allure-results-merged", help="Path to allure results")
    parser.add_argument("--previous", type=str, help="Path to previous last_result.json")
    parser.add_argument("--branch", type=str, default="main", help="Current git branch")
    parser.add_argument("--browser", type=str, default="chromium", help="Target browser/environment")
    parser.add_argument("--app-version", type=str, default=None, help="App version (defaults to pyproject.toml)")

    args = parser.parse_args()

    allure_dir = BASE_DIR / args.allure_dir
    previous_path = Path(args.previous) if args.previous else None

    app_version = args.app_version if args.app_version else get_project_version()

    report_dir = BASE_DIR / "reports"
    report_dir.mkdir(exist_ok=True)

    data = parse_allure_results(str(allure_dir), app_version)
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

    result = Painter.create_statistic_image(report_data, args.browser, args.branch)
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
