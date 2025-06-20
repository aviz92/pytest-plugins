import logging

from _pytest.config import Config
from _pytest.python import Function

logger = logging.getLogger()


def flag_is_enabled(config: Config, flag_name: str) -> bool:
    return config.getoption(flag_name)


def get_test_name_without_parameters(item: Function) -> str:
    """Get the test name without parameters."""
    return item.nodeid.split('[')[0]


def get_test_full_name(item: Function) -> str:
    """Get the full name of the test, including parameters if available."""
    test_name = get_test_name_without_parameters(item=item)
    return f"{test_name}[{item.callspec.indices}]" if getattr(item, 'callspec', None) else test_name
