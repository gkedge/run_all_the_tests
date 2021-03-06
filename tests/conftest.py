from pathlib import Path, PurePath
import sys

import pytest

PROJECT_PATH = Path(__file__).parent.parent.absolute()
PROJECT_PATH_SRC = PROJECT_PATH / "src"
# Totally unexpected that this project's `src` path would ever be in `sys.path` at this point!
# But, poetry is indeed adding it, surprisingly:
# https://github.com/python-poetry/poetry/issues/1729
# assert str(PROJECT_PATH / "src") not in sys.path, f"{sys.path}"
if PROJECT_PATH_SRC.is_dir() and str(PROJECT_PATH_SRC) not in sys.path:
    sys.path.append(str(PROJECT_PATH_SRC))

# pylint: disable=wrong-import-position
from run_all_the_tests import TestCasePath, TestCase

# pylint: enable=wrong-import-position

sys.dont_write_bytecode = True

TEST_PATH = PurePath("tests/test_case/test_test_type.py")

SCRIPT = PurePath("tests/test_case/run_test_case.py")


@pytest.fixture(scope="session", name="project_path")
def project_path_fixture() -> PurePath:
    return PROJECT_PATH


@pytest.fixture(scope="session", name="test_path")
def test_path_fixture() -> PurePath:
    return TEST_PATH


@pytest.fixture(scope="session", name="test_case_path")
def test_case_path_fixture(project_path, test_path) -> TestCasePath:
    return TestCasePath(project_path, test_path)


@pytest.fixture(scope="session")
def test_case_dir_path(project_path, test_path) -> TestCasePath:
    return TestCasePath(project_path, test_path.parent)


@pytest.fixture(scope="session", name="test_case_script_path")
def test_case_script_path_fixture(project_path) -> TestCasePath:
    return TestCasePath(project_path, SCRIPT)


@pytest.fixture()
def test_case(test_case_path: TestCasePath) -> TestCase:
    return TestCase.gen_test_case(test_case_path)


@pytest.fixture()
def test_script_case(test_case_script_path: TestCasePath) -> TestCase:
    return TestCase.gen_test_case(test_case_script_path)
