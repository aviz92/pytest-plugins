import pytest
from _pytest.config import Parser
from _pytest.main import Session


def pytest_addoption(parser: Parser) -> None:
    parser.addoption(
        "--require-tests",
        action="store_true",
        default=False,
        help="Fail the run if zero tests were collected.",
    )
    parser.addoption(
        "--require-tests-status-code",
        action="store",
        type=int,
        default=pytest.ExitCode.NO_TESTS_COLLECTED,
        choices=[e.value for e in pytest.ExitCode],
        help="Exit code returned when no tests are collected (default: 5 = NO_TESTS_COLLECTED).",
    )


def pytest_collection_finish(session: Session) -> None:
    if session.config.option.require_tests and not session.items:
        pytest.exit(
            reason="--require-tests: No tests collected.",
            returncode=session.config.getoption("require_tests_status_code"),
        )
