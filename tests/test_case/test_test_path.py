from pathlib import PurePath


def test_project_root(project_path, test_case_path):
    assert test_case_path.project_root == project_path


def test_test_case(test_case_path, test_path):
    assert test_case_path.test_case == test_path


def test_full_test_case_path(project_path, test_path, test_case_path):
    assert test_case_path.full_test_case_path.relative_to(project_path) == test_path


def test_test_case_relative_to_project_root(test_case_path, test_path):
    assert test_case_path.test_case_relative_to_project_root == test_path


def test_test_case_relative_to(project_path, test_path, test_case_path):
    assert test_case_path.test_case_relative_to(project_path / test_path) == PurePath(
        "."
    )


def test_test_case_relative_to_project(project_path, test_path, test_case_path):
    assert (
        test_case_path.test_case_relative_to_project(project_path / test_path)
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


def test_working_directories(project_path, test_case_path):
    assert test_case_path.working_directories == [
        project_path,
        test_case_path.full_test_case_path.parent.parent,
        test_case_path.full_test_case_path.parent,
    ]
