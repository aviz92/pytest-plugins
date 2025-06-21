import json
import logging
from collections import Counter

from custom_python_logger import get_logger


def summarize_tests(json_path: str):
    with open(json_path, "r", encoding="utf-8") as f:
        test_results = json.load(f)

    statuses = [v["test_status"] for v in test_results.values()]
    counts = Counter(statuses)

    logger.info(f"Filed tests == {True if counts.get('failed', 0) else False}")
    if counts.get("failed", 0):
        exit(1)


if __name__ == "__main__":
    logger = get_logger(project_name='Automation-Tests-Check-Status', log_level=logging.DEBUG)
    summarize_tests(json_path="../tests/results_output/test_results.json")
