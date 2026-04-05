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


def pytest_collection_finish(session: Session) -> None:
    if session.config.option.require_tests and not session.items:
        raise pytest.UsageError("--require-tests: No tests collected.")
