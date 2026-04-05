import pytest


class TestMaxFailStreak:
    def test_skips_tests_after_streak_reached(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile("""
            def test_fail_1(): assert False
            def test_fail_2(): assert False
            def test_fail_3(): assert False
            def test_should_be_skipped(): assert True
        """)
        result = pytester.runpytest_subprocess("--maxfail-streak=3")
        result.assert_outcomes(failed=3, skipped=1)

    def test_streak_resets_after_passing_test(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile("""
            def test_fail_1(): assert False
            def test_fail_2(): assert False
            def test_pass(): assert True
            def test_fail_3(): assert False
            def test_fail_4(): assert False
            def test_fail_5(): assert False
            def test_should_be_skipped(): assert True
        """)
        result = pytester.runpytest_subprocess("--maxfail-streak=3")
        result.assert_outcomes(failed=5, passed=1, skipped=1)

    def test_without_flag_all_tests_run(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile("""
            def test_fail_1(): assert False
            def test_fail_2(): assert False
            def test_fail_3(): assert False
            def test_fail_4(): assert False
        """)
        result = pytester.runpytest_subprocess()
        result.assert_outcomes(failed=4)

    def test_streak_below_max_runs_all_tests(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile("""
            def test_fail_1(): assert False
            def test_pass_1(): assert True
            def test_fail_2(): assert False
        """)
        result = pytester.runpytest_subprocess("--maxfail-streak=3")
        result.assert_outcomes(failed=2, passed=1)

    def test_all_passing_tests_unaffected(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile("""
            def test_pass_1(): assert True
            def test_pass_2(): assert True
            def test_pass_3(): assert True
        """)
        result = pytester.runpytest_subprocess("--maxfail-streak=2")
        assert result.ret == pytest.ExitCode.OK, f"Expected OK, got {result.ret}"
        result.assert_outcomes(passed=3)
