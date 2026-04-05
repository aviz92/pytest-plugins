from custom_python_logger import build_logger

pytest_plugins = ["pytester"]

logger = build_logger(project_name="pytest-plugins", log_file=True)
