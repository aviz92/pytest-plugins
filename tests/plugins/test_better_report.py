import json

import pytest

from pytest_plugins.better_report import EXECUTION_RESULTS_FILENAME, TEST_RESULTS_FILENAME


class TestBetterReport:
    def test_output_files_created_when_enabled(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile("""
            def test_foo() -> None:
                assert True
        """)
        result = pytester.runpytest_subprocess("--better-report")
        assert result.ret == pytest.ExitCode.OK, f"Expected OK, got {result.ret}"
        output_dir = pytester.path / "results_output"
        assert (output_dir / EXECUTION_RESULTS_FILENAME).exists(), f"Expected {EXECUTION_RESULTS_FILENAME} to be created"
        assert (output_dir / TEST_RESULTS_FILENAME).exists(), f"Expected {TEST_RESULTS_FILENAME} to be created"

    def test_no_output_files_without_flag(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile("""
            def test_foo() -> None:
                assert True
        """)
        result = pytester.runpytest_subprocess()
        assert result.ret == pytest.ExitCode.OK, f"Expected OK, got {result.ret}"
        output_dir = pytester.path / "results_output"
        assert not output_dir.exists(), "Expected no output dir when plugin disabled"

    def test_execution_status_passed_on_passing_tests(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile("""
            def test_foo() -> None:
                assert True
        """)
        result = pytester.runpytest_subprocess("--better-report")
        assert result.ret == pytest.ExitCode.OK, f"Expected OK, got {result.ret}"
        execution_file = pytester.path / "results_output" / EXECUTION_RESULTS_FILENAME
        data = json.loads(execution_file.read_text())
        assert data["execution_info"]["execution_status"] == "passed", (
            f"Expected 'passed', got {data['execution_info']['execution_status']}"
        )

    def test_execution_status_failed_on_failing_tests(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile("""
            def test_foo() -> None:
                assert False
        """)
        result = pytester.runpytest_subprocess("--better-report")
        assert result.ret == pytest.ExitCode.TESTS_FAILED, f"Expected TESTS_FAILED, got {result.ret}"
        execution_file = pytester.path / "results_output" / EXECUTION_RESULTS_FILENAME
        data = json.loads(execution_file.read_text())
        assert data["execution_info"]["execution_status"] == "failed", (
            f"Expected 'failed', got {data['execution_info']['execution_status']}"
        )

    def test_test_results_contains_test_entry(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile("""
            def test_my_test() -> None:
                assert True
        """)
        result = pytester.runpytest_subprocess("--better-report")
        assert result.ret == pytest.ExitCode.OK, f"Expected OK, got {result.ret}"
        test_file = pytester.path / "results_output" / TEST_RESULTS_FILENAME
        data = json.loads(test_file.read_text())
        assert len(data) == 1, f"Expected 1 test entry, got {len(data)}"
        test_entry = next(iter(data.values()))
        assert test_entry["test_status"] == "passed", f"Expected 'passed', got {test_entry['test_status']}"

    def test_custom_output_dir(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile("""
            def test_foo() -> None:
                assert True
        """)
        result = pytester.runpytest_subprocess("--better-report", "--output-dir=custom_dir")
        assert result.ret == pytest.ExitCode.OK, f"Expected OK, got {result.ret}"
        output_dir = pytester.path / "custom_dir" / "results_output"
        assert (output_dir / EXECUTION_RESULTS_FILENAME).exists(), (
            f"Expected {EXECUTION_RESULTS_FILENAME} in custom output dir"
        )

    def test_md_report_generated_with_flag(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile("""
            def test_foo() -> None:
                assert True
        """)
        result = pytester.runpytest_subprocess("--better-report", "--md-report")
        assert result.ret == pytest.ExitCode.OK, f"Expected OK, got {result.ret}"
        output_dir = pytester.path / "results_output"
        assert (output_dir / "test_report.md").exists(), "Expected test_report.md to be created"

    def test_repo_name_stored_in_execution_results(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile("""
            def test_foo() -> None:
                assert True
        """)
        result = pytester.runpytest_subprocess("--better-report", "--repo-name=my-repo")
        assert result.ret == pytest.ExitCode.OK, f"Expected OK, got {result.ret}"
        execution_file = pytester.path / "results_output" / EXECUTION_RESULTS_FILENAME
        data = json.loads(execution_file.read_text())
        assert data["execution_info"]["repo_name"] == "my-repo", (
            f"Expected repo_name 'my-repo', got {data['execution_info']['repo_name']}"
        )

    def test_pr_number_stored_in_execution_results(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile("""
            def test_foo() -> None:
                assert True
        """)
        result = pytester.runpytest_subprocess("--better-report", "--pr-number=42")
        assert result.ret == pytest.ExitCode.OK, f"Expected OK, got {result.ret}"
        execution_file = pytester.path / "results_output" / EXECUTION_RESULTS_FILENAME
        data = json.loads(execution_file.read_text())
        assert data["execution_info"]["pull_request_number"] == "42", (
            f"Expected pull_request_number '42', got {data['execution_info']['pull_request_number']}"
        )

    def test_multiple_tests_all_tracked(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile("""
            def test_first() -> None:
                assert True

            def test_second() -> None:
                assert True

            def test_third() -> None:
                assert True
        """)
        result = pytester.runpytest_subprocess("--better-report")
        assert result.ret == pytest.ExitCode.OK, f"Expected OK, got {result.ret}"
        test_file = pytester.path / "results_output" / TEST_RESULTS_FILENAME
        data = json.loads(test_file.read_text())
        assert len(data) == 3, f"Expected 3 test entries, got {len(data)}"

    def test_skipped_test_does_not_cause_failed_execution_status(self, pytester: pytest.Pytester) -> None:
        pytester.makepyfile("""
            import pytest

            def test_pass() -> None:
                assert True

            @pytest.mark.skip
            def test_skip() -> None:
                assert True
        """)
        result = pytester.runpytest_subprocess("--better-report")
        assert result.ret == pytest.ExitCode.OK, f"Expected OK, got {result.ret}"
        execution_file = pytester.path / "results_output" / EXECUTION_RESULTS_FILENAME
        data = json.loads(execution_file.read_text())
        assert data["execution_info"]["execution_status"] == "passed", (
            f"Expected 'passed' when skipped tests present, got {data['execution_info']['execution_status']}"
        )
