import pytest


class TestRequireTests:
    def test_exits_with_usage_error_when_no_tests_collected(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile("")
        result = pytester.runpytest_subprocess("--require-tests")
        assert (
            result.ret == pytest.ExitCode.USAGE_ERROR
        ), f"Expected {pytest.ExitCode.USAGE_ERROR}, got {result.ret}"

    def test_passes_when_tests_are_collected(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile(
            """
            def test_foo():
                assert True
        """
        )
        result = pytester.runpytest_subprocess("--require-tests")
        assert result.ret == pytest.ExitCode.OK, f"Expected OK, got {result.ret}"

    def test_without_flag_no_tests_uses_default_exit_code(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile("")
        result = pytester.runpytest_subprocess()
        assert (
            result.ret == pytest.ExitCode.NO_TESTS_COLLECTED
        ), f"Expected {pytest.ExitCode.NO_TESTS_COLLECTED}, got {result.ret}"
