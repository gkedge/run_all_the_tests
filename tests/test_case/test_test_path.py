from pathlib import PurePath

from tests.conftest import PROJECT_PATH
from tests.test_case.conftest import TEST_CASE


def test_project_root(test_case_path):
    assert test_case_path.project_root == PROJECT_PATH


def test_test_case(test_case_path):
    assert test_case_path.test_case == TEST_CASE


def test_full_test_case_path(test_case_path):
    assert test_case_path.full_test_case_path.relative_to(PROJECT_PATH) == TEST_CASE


def test_test_case_relative_to_project_root(test_case_path):
    assert test_case_path.test_case_relative_to_project_root == TEST_CASE


def test_test_case_relative_to(test_case_path):
    assert test_case_path.test_case_relative_to(PROJECT_PATH / TEST_CASE) == PurePath(
        "."
    )


def test_test_case_relative_to_project(test_case_path):
    assert (
        test_case_path.test_case_relative_to_project(PROJECT_PATH / TEST_CASE)
        == test_case_path.full_test_case_path
    )


def test_is_dir_test_case(test_case_path, test_case_dir_path, test_case_script_path):
    assert not test_case_script_path.is_dir_test_case
    assert not test_case_path.is_dir_test_case
    assert test_case_dir_path.is_dir_test_case


def test_is_test_case(test_case_path, test_case_dir_path, test_case_script_path):
    assert not test_case_script_path.is_test_case
    assert test_case_path.is_test_case
    assert test_case_dir_path.is_dir_test_case


def test_is_script(test_case_path, test_case_dir_path, test_case_script_path):
    assert test_case_script_path.is_script
    assert not test_case_path.is_script
    assert not test_case_dir_path.is_script


def test_working_directories(test_case_path):
    assert test_case_path.working_directories == [
        PROJECT_PATH,
        test_case_path.full_test_case_path.parent.parent,
        test_case_path.full_test_case_path.parent,
    ]
