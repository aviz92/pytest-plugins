import pytest


class TestRequireTests:
    def test_exits_with_default_code_when_no_tests_collected(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile("")
        result = pytester.runpytest_subprocess("--require-tests")
        assert result.ret == pytest.ExitCode.NO_TESTS_COLLECTED, (
            f"Expected {pytest.ExitCode.NO_TESTS_COLLECTED}, got {result.ret}"
        )

    def test_exits_with_custom_code_when_no_tests_collected(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile("")
        result = pytester.runpytest_subprocess("--require-tests", "--require-tests-status-code=1")
        assert result.ret == 1, f"Expected 1, got {result.ret}"

    def test_passes_when_tests_are_collected(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile("""
            def test_foo():
                assert True
        """)
        result = pytester.runpytest_subprocess("--require-tests")
        assert result.ret == pytest.ExitCode.OK, f"Expected OK, got {result.ret}"

    def test_without_flag_no_tests_uses_default_exit_code(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile("")
        result = pytester.runpytest_subprocess()
        assert result.ret == pytest.ExitCode.NO_TESTS_COLLECTED, (
            f"Expected {pytest.ExitCode.NO_TESTS_COLLECTED}, got {result.ret}"
        )

    def test_custom_exit_code_unused_when_tests_are_collected(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile("""
            def test_foo():
                assert True
        """)
        result = pytester.runpytest_subprocess("--require-tests", "--require-tests-status-code=3")
        assert result.ret == pytest.ExitCode.OK, (
            f"Expected OK when tests collected (custom code unused), got {result.ret}"
        )
