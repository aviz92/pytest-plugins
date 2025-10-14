import json
import logging
import sys
from collections import Counter

from custom_python_logger import build_logger

logger = build_logger(project_name="Automation-Tests-Check-Status", log_level=logging.DEBUG)


def summarize_tests(json_path: str) -> None:
    with open(json_path, encoding="utf-8") as f:
        test_results = json.load(f)

    statuses = [v["test_status"] for v in test_results.values()]
    counts = Counter(statuses)

    if counts.get("failed", 0):
        logger.info("Filed tests == True")
        sys.exit(1)
    logger.info("Filed tests == False")


def main() -> None:
    summarize_tests(json_path="../results_output/test_results.json")


if __name__ == "__main__":
    main()
