import pytest


class TestVerboseParamIds:
    def test_node_ids_contain_param_dict_with_flag(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile("""
            import pytest

            @pytest.mark.parametrize("x", [1, 2])
            def test_foo(x: int) -> None:
                assert x > 0
        """)
        result = pytester.runpytest_subprocess("--verbose-param-ids", "-v")
        assert result.ret == pytest.ExitCode.OK, f"Expected OK, got {result.ret}"
        result.stdout.fnmatch_lines(["*'x': 1*"])

    def test_default_ids_without_flag(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile("""
            import pytest

            @pytest.mark.parametrize("x", [1, 2])
            def test_foo(x: int) -> None:
                assert x > 0
        """)
        result = pytester.runpytest_subprocess("-v")
        assert result.ret == pytest.ExitCode.OK, f"Expected OK, got {result.ret}"
        # Use str() check since fnmatch treats [1] as a character class
        stdout = result.stdout.str()
        assert "test_foo[1]" in stdout, f"Expected 'test_foo[1]' in output, got:\n{stdout}"
        assert "test_foo[2]" in stdout, f"Expected 'test_foo[2]' in output, got:\n{stdout}"

    def test_non_parametrized_tests_pass_unaffected(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile("""
            def test_simple() -> None:
                assert True
        """)
        result = pytester.runpytest_subprocess("--verbose-param-ids", "-v")
        assert result.ret == pytest.ExitCode.OK, f"Expected OK, got {result.ret}"
        result.assert_outcomes(passed=1)

    def test_all_parametrized_tests_still_run(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile("""
            import pytest

            @pytest.mark.parametrize("x,y", [(1, 2), (3, 4)])
            def test_pairs(x: int, y: int) -> None:
                assert x < y
        """)
        result = pytester.runpytest_subprocess("--verbose-param-ids")
        assert result.ret == pytest.ExitCode.OK, f"Expected OK, got {result.ret}"
        result.assert_outcomes(passed=2)
