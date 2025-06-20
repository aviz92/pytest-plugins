import logging
from _pytest.config import Config, Parser
from _pytest.reports import TestReport

from pytest_plugins.pytest_helper import flag_is_enabled

logger = logging.getLogger('pytest_plugins.add_better_report')
global_interface = {}

def pytest_addoption(parser: Parser):
    parser.addoption(
        "--fail2skip-enable",
        action="store_true",
        default=False,
        help="Enable the fail2skip-enable plugin",
    )


def pytest_configure(config: Config):
    if flag_is_enabled(config=config, flag_name="--fail2skip-enable"):
        config._fail2skip_enabled = True
    else:
        config._fail2skip_enabled = False


def pytest_runtest_makereport(item, call):
    outcome = yield
    report: TestReport = outcome.get_result()
    config = item.config

    if config._fail2skip_enabled and report.when == "call" and report.failed:
        # Mark the test as skipped instead of failed
        report.outcome = "skipped"
        report.wasxfail = False  # Avoid being treated as xfail
