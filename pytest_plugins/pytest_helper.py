import logging

from _pytest.python import Function

logger = logging.getLogger()


def get_test_name_without_parameters(item: Function) -> str:
    """Get the test name without parameters."""
    return item.nodeid.split('[')[0]


def get_test_full_name(item: Function) -> str:
    """Get the full name of the test, including parameters if available."""
    test_name = get_test_name_without_parameters(item=item)
    return f"{test_name}[{item.callspec.indices}]" if getattr(item, 'callspec', None) else test_name
