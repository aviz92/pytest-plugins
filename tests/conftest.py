from custom_python_logger import build_logger

from pytest_plugins import LOGGER_NAME

pytest_plugins = ["pytester"]

logger = build_logger(project_name=LOGGER_NAME, log_file=True)
