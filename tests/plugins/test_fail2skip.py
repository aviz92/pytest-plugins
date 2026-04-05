import pytest


class TestFail2Skip:
    def test_failing_marked_test_becomes_skipped(self, pytester: pytest.Pytester) -> None:
        pytester.makeini(
            """
            [pytest]
            markers = fail2skip: Convert failures to skips
        """
        )
        pytester.makepyfile(
            """
            import pytest

            @pytest.mark.fail2skip
            def test_should_skip():
                assert False
        """
        )
        result = pytester.runpytest_subprocess("--fail2skip")
        assert result.ret == pytest.ExitCode.OK, f"Expected OK, got {result.ret}"
        # Plugin sets report.wasxfail which pytest counts as xfailed, not skipped
        result.assert_outcomes(xfailed=1)

    def test_passing_marked_test_remains_passed(self, pytester: pytest.Pytester) -> None:
        pytester.makeini(
            """
            [pytest]
            markers = fail2skip: Convert failures to skips
        """
        )
        pytester.makepyfile(
            """
            import pytest

            @pytest.mark.fail2skip
            def test_should_pass():
                assert True
        """
        )
        result = pytester.runpytest_subprocess("--fail2skip")
        assert result.ret == pytest.ExitCode.OK, f"Expected OK, got {result.ret}"
        result.assert_outcomes(passed=1)

    def test_without_flag_failure_remains_failure(self, pytester: pytest.Pytester) -> None:
        pytester.makeini(
            """
            [pytest]
            markers = fail2skip: Convert failures to skips
        """
        )
        pytester.makepyfile(
            """
            import pytest

            @pytest.mark.fail2skip
            def test_should_fail():
                assert False
        """
        )
        result = pytester.runpytest_subprocess()
        assert result.ret == pytest.ExitCode.TESTS_FAILED, f"Expected TESTS_FAILED, got {result.ret}"
        result.assert_outcomes(failed=1)

    def test_unmarked_failing_test_unaffected_by_flag(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile(
            """
            def test_should_fail():
                assert False
        """
        )
        result = pytester.runpytest_subprocess("--fail2skip")
        assert result.ret == pytest.ExitCode.TESTS_FAILED, f"Expected TESTS_FAILED, got {result.ret}"
        result.assert_outcomes(failed=1)

    def test_multiple_marked_tests_all_become_skipped(self, pytester: pytest.Pytester) -> None:
        pytester.makeini(
            """
            [pytest]
            markers = fail2skip: Convert failures to skips
        """
        )
        pytester.makepyfile(
            """
            import pytest

            @pytest.mark.fail2skip
            def test_fail_1():
                assert False

            @pytest.mark.fail2skip
            def test_fail_2():
                assert False

            def test_pass():
                assert True
        """
        )
        result = pytester.runpytest_subprocess("--fail2skip")
        assert result.ret == pytest.ExitCode.OK, f"Expected OK, got {result.ret}"
        # Plugin sets report.wasxfail which pytest counts as xfailed, not skipped
        result.assert_outcomes(xfailed=2, passed=1)
