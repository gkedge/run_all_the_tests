from pathlib import PurePath, Path

import pytest

from run_all_the_tests import TestCasePath

PROJECT_PATH: PurePath = Path(__file__).parent.parent.parent.absolute()

TEST_CASE = PurePath("tests/test_case/test_test_type.py")

SCRIPT = PurePath("tests/test_case/run_test_case.py")


@pytest.fixture(scope="session")
def test_case_path() -> TestCasePath:
    return TestCasePath(PROJECT_PATH, TEST_CASE)


@pytest.fixture(scope="session")
def test_case_dir_path() -> TestCasePath:
    return TestCasePath(PROJECT_PATH, TEST_CASE.parent)


@pytest.fixture(scope="session")
def test_case_script_path() -> TestCasePath:
    return TestCasePath(PROJECT_PATH, SCRIPT)
