import sys
import json
import logging
from collections import Counter
from pathlib import Path

from custom_python_logger import get_logger


def summarize_tests(json_path: str, output_md_path: Path = Path("reports/test_summary.md"), commit_hash: str = None):
    if not output_md_path.parent.exists():
        output_md_path.parent.mkdir(parents=True, exist_ok=True)
    with open(json_path, "r", encoding="utf-8") as f:
        test_results = json.load(f)

    statuses = [v["test_status"] for v in test_results.values()]
    counts = Counter(statuses)

    total = len(statuses)
    passed = counts.get("passed", 0)
    failed = counts.get("failed", 0)
    skipped = counts.get("skipped", 0)
    success_rate = (passed / total * 100) if total else 0

    summary_lines = [
        f"# Test Summary for commit hash: {commit_hash}\n\n"
        "---\n",
        f"📊 **Success rate:** {success_rate:.2f}%",
        f"🧪 **Total tests:** {total} <br>"
        "\n\n---\n",

        f"**Test Results:**",
        f" - ✅ **Passed:** {passed}",
        f" - ❌ **Failed:** {failed}",
        f" - ⏭️ **Skipped:** {skipped}"
        f"\n---\n",
    ]

    for line in summary_lines:
        logger.info(line)

    with open(output_md_path, "w", encoding="utf-8") as out:
        out.write("\n".join(summary_lines))


def main():
    commit_hash = sys.argv[1] if len(sys.argv) > 1 else None
    logger.info(f"Commit hash: {commit_hash}")

    summarize_tests(
        json_path="../results_output/test_results.json",
        output_md_path=Path("reports/test_summary.md"),
        commit_hash=commit_hash
    )


if __name__ == "__main__":
    logger = get_logger(project_name='Automation-Tests-Summary', log_level=logging.DEBUG)

    main()
