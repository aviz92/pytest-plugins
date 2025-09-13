import logging

from custom_python_logger import build_logger

logger = build_logger(project_name='pytest-plugins', log_level=logging.DEBUG)
