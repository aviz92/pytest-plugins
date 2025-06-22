import pytest


class TestDummy:
    @pytest.mark.test_pass
    def test_pass(self):
        assert True

    def test_false(self):
        assert False, {"message": "This test is expected to fail."}

    @pytest.mark.fail2skip
    @pytest.mark.parametrize("param1, param2", [("A", "A"), (2, 2), (3, 3), (4, 5)])
    def test_with_parameters_1(self, param1, param2):
        assert param1 != param2

    @pytest.mark.parametrize("param1, param2", [(1, 1), (2, 2), (3, 3), (4, 5)])
    def test_with_parameters_2(self, param1, param2):
        assert param1 != param2
