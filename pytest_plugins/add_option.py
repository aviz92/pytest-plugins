def pytest_addoption(parser):
    parser.addoption(
        "--better-report",
        action="store_true",
        default=False,
        help="Enable the pytest-better-report plugin",
    )
    parser.addoption(
        "--maxfail-streak",
        action="store_true",
        default=False,
        help="Enable the pytest-max-fail-streak plugin ; Maximum consecutive test failures before stopping execution",
    )
