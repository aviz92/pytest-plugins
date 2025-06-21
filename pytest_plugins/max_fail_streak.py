import logging
import pytest
from _pytest.config import Config, Parser
from _pytest.python import Function
from _pytest.reports import TestReport

from pytest_plugins.better_report import test_results
from pytest_plugins.models import ExecutionStatus
from pytest_plugins.pytest_helper import get_test_full_name

logger = logging.getLogger('pytest_plugins.max_fail_streak')
global_interface = {}


def pytest_addoption(parser: Parser) -> None:
    parser.addoption(
        "--maxfail-streak-enable",
        action="store_true",
        default=False,
        help="Enable the pytest-max-fail-streak plugin",
    )
    parser.addoption(
        "--maxfail-streak",
        action="store",
        default=None,
        help="Maximum consecutive test failures before stopping execution. "
             "for using maxfail not streak use the built-in pytest option `--maxfail`",
    )


def pytest_configure(config: Config) -> None:
    config._max_fail_streak_enabled = config.getoption("--maxfail-streak-enable")
    _max_fail_streak = config.getoption("--maxfail-streak")
    global_interface['max_fail_streak'] = int(_max_fail_streak) if _max_fail_streak else None
    global_interface['fail_streak'] = 0


def pytest_runtest_setup(item: Function) -> None:
    max_streak = global_interface['max_fail_streak']
    fail_streak = global_interface['fail_streak']
    if max_streak and fail_streak >= max_streak:
        _skip_message = 'Skipping test due to maximum consecutive failures reached.'

        test_name = get_test_full_name(item=item)
        test_results[test_name].test_status = ExecutionStatus.SKIPPED
        test_results[test_name].exception_message = {
            "exception_type": "MaxFailStreakReached",
            "message": _skip_message,
        }
        logger.info(f"Skipping test {test_name} because fail streak {fail_streak} reached max {max_streak}")
        pytest.skip(_skip_message)


def pytest_runtest_logreport(report: TestReport) -> None:
    if report.when == "call":
        global_interface['fail_streak'] = global_interface['fail_streak'] + 1 if report.failed else 0

        max_streak = global_interface['max_fail_streak']
        fail_streak = global_interface['fail_streak']
        if max_streak and fail_streak >= max_streak:
            logger.error(
                f'Maximum consecutive test failures reached: {global_interface["max_fail_streak"]}. '
                f'Stopping execution.'
            )
