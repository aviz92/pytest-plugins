import logging
import pytest
from _pytest.config import Config, Parser
from _pytest.main import Session
from _pytest.python import Function
from _pytest.reports import TestReport

from pytest_plugins.add_better_report import test_results
from pytest_plugins.models import ExecutionStatus
from pytest_plugins.pytest_helper import get_test_full_name, flag_is_enabled

logger = logging.getLogger('pytest_plugins.add_better_report')
global_interface = {}


def pytest_addoption(parser: Parser):
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
        help="Maximum consecutive test failures before stopping execution"
    )  # for using maxfail not streak, you can use the built-in pytest option `--maxfail`


def pytest_configure(config: Config):
    if flag_is_enabled(config=config, flag_name="--maxfail-streak-enable"):
        config._max_fail_streak_enabled = True
    else:
        config._max_fail_streak_enabled = False


def pytest_sessionstart(session: Session) -> None:
    """Called before the test session starts."""
    _max_fail_streak = session.config.getoption("--maxfail-streak")
    global_interface['max_fail_streak'] = int(_max_fail_streak) if _max_fail_streak else None
    global_interface['fail_streak'] = 0


def pytest_runtest_setup(item: Function) -> None:
    """This runs before each test."""
    if (
            global_interface['max_fail_streak'] and
            global_interface['fail_streak'] >= global_interface['max_fail_streak']
    ):
        _skip_message = 'Skipping test due to maximum consecutive failures reached.'

        test_results[get_test_full_name(item=item)].test_status = ExecutionStatus.SKIPPED
        test_results[get_test_full_name(item=item)].exception_message = {
            "exception_type": "MaxFailStreakReached",
            "message": _skip_message,
        }
        pytest.skip(_skip_message)

    if getattr(item.cls, 'component', None):
        logger.debug(f"Test class {item.cls.__name__} has parameter 'component' with value: {item.cls.component}")


def pytest_runtest_logreport(report: TestReport):
    if report.when == "call":
        global_interface['fail_streak'] = global_interface['fail_streak'] + 1 if report.failed else 0

        if (
                global_interface['max_fail_streak'] and
                global_interface['fail_streak'] >= global_interface['max_fail_streak']
        ):
            logger.error(
                f'Maximum consecutive test failures reached: {global_interface["max_fail_streak"]}. Stopping execution.'
            )
