import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Generator

import pytest
from _pytest.fixtures import FixtureRequest
from _pytest.main import Session
from _pytest.python import Function

from pytest_plugins.helper import save_as_json, serialize_data
from pytest_plugins.models import ExecutionData, ExecutionStatus, TestData
from pytest_plugins.pytest_helper import get_test_full_name, get_test_name_without_parameters

global_interface = {}  # This variable is used to store the global interface object, if needed
execution_results = {}
test_results = {}
logger = logging.getLogger('pytest_plugins.add_better_report')


def pytest_addoption(parser):
    parser.addoption(
        "--better-report-enable",
        action="store_true",
        default=False,
        help="Enable the pytest-better-report plugin",
    )


def _is_enabled(config):
    return config.getoption("--better-report-enable")


def pytest_configure(config):
    if _is_enabled(config):
        config._better_report_enabled = True
    else:
        config._better_report_enabled = False


def pytest_sessionstart(session: Session) -> None:
    """Called before the test session starts."""
    global_interface['session'] = session  # Store the session object in the global interface

    execution_results["execution_info"] = ExecutionData(
        pull_request_number=session.config.getoption("--pr-number", None),
        execution_status=ExecutionStatus.STARTED,
        execution_start_time=datetime.now(timezone.utc).isoformat(),
    )


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(items: list[Function]) -> None:
    """ This hook is called after the collection has been performed, but before the tests are executed """

    for item in items:
        test_name = get_test_name_without_parameters(item=item)
        test_full_name = get_test_full_name(item=item)
        test_results[test_full_name] = TestData(
            class_test_name=item.cls.__name__ if item.cls else None,
            test_name=test_name,
            test_full_name=test_full_name,
            test_file_name=item.fspath.basename,
            test_markers=[marker.name for marker in item.iter_markers() if not marker.args],
            test_status=ExecutionStatus.COLLECTED,
            test_start_time=datetime.now(timezone.utc).isoformat(),
        )
    logger.debug(f'Tests to be executed: \n{json.dumps(list(test_results.keys()), indent=4, default=serialize_data)}')
    time.sleep(0.3)  # Sleep to ensure the debug log is printed before the tests start


@pytest.fixture(scope="session", autouse=True)
def session_setup_teardown() -> Generator[None, Any, None]:
    yield

    # update execution end time
    execution_results["execution_info"].execution_end_time = datetime.now(timezone.utc).isoformat()

    # update execution duration time
    execution_start_time_obj = datetime.fromisoformat(execution_results["execution_info"].execution_start_time)
    execution_end_time_obj = datetime.fromisoformat(execution_results["execution_info"].execution_end_time)
    execution_results["execution_info"].execution_duration_sec = \
        (execution_end_time_obj - execution_start_time_obj).total_seconds()

    # update execution status
    _execution_status = all(test.test_status == ExecutionStatus.PASSED for test in test_results.values())
    execution_results["execution_info"].execution_status = \
        ExecutionStatus.PASSED if _execution_status else ExecutionStatus.FAILED

    execution_results["execution_info"].test_list = list(test_results.keys())

    save_as_json(path=Path('results_output/execution_results.json'), data=execution_results, default=serialize_data)
    save_as_json(path=Path('results_output/test_results.json'), data=test_results, default=serialize_data)


@pytest.fixture(autouse=True)
def report_test_results_to_automation_db(request: FixtureRequest) -> None:
    test_item = request.node

    # log the test results after each test.
    test_full_name = get_test_full_name(item=test_item)
    logger.debug(f'Test Results: \n{json.dumps(test_results[test_full_name], indent=4, default=serialize_data)}')


def pytest_runtest_teardown(item: Function) -> None:
    """This runs after each test."""

    test_full_name = get_test_full_name(item=item)
    test_item = test_results[test_full_name]

    test_item.test_end_time = datetime.now(timezone.utc).isoformat()
    if test_item.test_start_time:  # Add test duration only if start time is set
        test_start_time_obj = datetime.fromisoformat(test_item.test_start_time)
        test_end_time_obj = datetime.fromisoformat(test_item.test_end_time)
        test_item.test_duration_sec = (test_end_time_obj - test_start_time_obj).total_seconds()


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item: Function, call: Any) -> None:
    """ This hook is called after each test is run """

    if call.when == "call":
        test_item = test_results[get_test_full_name(item=item)]

        test_item.test_status = ExecutionStatus.PASSED if call.excinfo is None else ExecutionStatus.FAILED

        if call.excinfo:
            exception_message = str(call.excinfo.value).split('\nassert')[0]
            try:
                test_item.exception_message = json.loads(exception_message)
            except json.JSONDecodeError:
                test_item.exception_message = {
                    'exception_type': call.excinfo.typename if call.excinfo else None,
                    'message': exception_message if call.excinfo else None,
                }
        else:
            test_item.exception_message = None


def pytest_sessionfinish(session: Session) -> None:
    """Called after the whole test session finishes."""

    exit_status_code = session.session.exitstatus
    logger.info(f'Test session finished with exit status: {exit_status_code}')
    if exit_status_code != 0:
        failed_tests = [v for k, v in test_results.items() if v.test_status == ExecutionStatus.FAILED]
        logger.debug(f'Failed tests: {json.dumps(failed_tests, indent=4, default=serialize_data)}')
