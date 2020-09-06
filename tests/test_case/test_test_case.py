import pytest

from run_all_the_tests import TestCase, TestType, TestCasePath


def test_generate_test_case(test_case_path):
    test_case: TestCase = TestCase.gen_test_case(test_case_path)
    assert test_case.test_case_path == test_case_path


def test_working_directories(project_path, test_case):
    assert test_case.working_directories == [
        project_path,
        test_case.test_case_path.full_test_case_path.parent.parent,
        test_case.test_case_path.full_test_case_path.parent,
    ]


# pylint: disable:protected-access
def test__is_script(test_case, test_script_case):
    assert not test_case._is_script
    assert test_script_case._is_script
# pylint: enable:protected-access


@pytest.mark.parametrize(
    "test_type", TestType.only_pytest_types(TestType.all_test_types)
)
def test_python_command_for_pytests(test_type, test_case):
    assert test_case.python_command(test_type) == test_type.python_command


@pytest.mark.parametrize(
    "test_type", TestType.only_script_types(TestType.all_test_types)
)
def test_python_command_for_scripts(test_type, test_script_case):
    assert test_script_case.python_command(test_type) == test_type.python_command


def test_test_case_relative_to_cwd(test_case):
    test_case_path: TestCasePath = test_case.test_case_path
    for working_dir in test_case.test_case_path.working_directories:
        expected_path = test_case_path.test_case_relative_to(working_dir)
        assert test_case.test_case_relative_to_cwd(working_dir) == expected_path


def test_cwd_relative_to_project(test_case):
    test_case_path: TestCasePath = test_case.test_case_path
    for working_dir in test_case.test_case_path.working_directories:
        expected_path = test_case_path.test_case_relative_to_project(working_dir)
        assert test_case.cwd_relative_to_project(working_dir) == expected_path
