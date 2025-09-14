from custom_python_logger import build_logger

pytest_plugins = [
    "pytest_plugins.better_report",
    "pytest_plugins.max_fail_streak",
    "pytest_plugins.fail2skip",
    "pytest_plugins.add_config_parameters",
    "pytest_plugins.verbose_param_ids",
]

logger = build_logger(
    project_name="pytest-plugins",
    log_file=True
)
