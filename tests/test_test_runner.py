from pathlib import Path

from run_all_the_tests import Group, TestType
from run_all_the_tests.test_runner import (
    _get_group_tests,  # noqa
    _run_test,  # noqa
    _RunningTestCase,  # noqa
)


def test__get_group_tests(test_case, test_script_case):
    test_cases = tuple([test_case, test_script_case])
    assert _get_group_tests(test_cases, Group.ONE) == test_cases
    assert _get_group_tests(test_cases, Group.TWO) == tuple()


def test__run_test(project_path, test_case):
    running_test_case: _RunningTestCase = _run_test(TestType.PYTEST, Path.cwd(), test_case)
    assert running_test_case.group == Group.ONE
    assert running_test_case.test_type == TestType.PYTEST
    assert running_test_case.cwd.relative_to(project_path)
    assert running_test_case.process
