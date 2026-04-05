import pytest


class TestAddConfigParameters:
    def test_config_path_option_registered(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile("""
            def test_foo() -> None:
                assert True
        """)
        result = pytester.runpytest_subprocess("--help")
        assert result.ret == pytest.ExitCode.OK, f"Expected OK, got {result.ret}"
        result.stdout.fnmatch_lines(["*--config-path*"])

    def test_runs_normally_without_flag(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile("""
            def test_foo() -> None:
                assert True
        """)
        result = pytester.runpytest_subprocess()
        assert result.ret == pytest.ExitCode.OK, f"Expected OK, got {result.ret}"
        result.assert_outcomes(passed=1)

    def test_flag_accepted_without_error(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile("""
            def test_foo() -> None:
                assert True
        """)
        result = pytester.runpytest_subprocess("--config-path")
        assert result.ret == pytest.ExitCode.OK, f"Expected OK, got {result.ret}"
