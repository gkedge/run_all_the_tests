import pytest

from run_all_the_tests import TestType


@pytest.mark.dependency()
def test_all_test_types():
    assert TestType.all_test_types == frozenset(TestType)


def test_is_pytest():
    assert TestType.PYTEST.is_pytest
    assert TestType.PYTHON_PYTEST.is_pytest
    assert not TestType.PYTHON.is_pytest


def test_is_python():
    assert not TestType.PYTEST.is_python
    assert not TestType.PYTHON_PYTEST.is_python
    assert TestType.PYTHON.is_python


def test_python_command():
    assert TestType.PYTEST.python_command != TestType.PYTHON_PYTEST.python_command
    assert TestType.PYTEST.python_command != TestType.PYTHON.python_command
    assert TestType.PYTHON_PYTEST.python_command != TestType.PYTEST.python_command
    assert TestType.PYTHON_PYTEST.python_command != TestType.PYTHON.python_command
    assert TestType.PYTHON.python_command != TestType.PYTEST.python_command
    assert TestType.PYTHON.python_command != TestType.PYTHON_PYTEST.python_command


@pytest.mark.dependency(depends=["test_all_test_types"])
def test_only_pytest_types():
    pytest_types = TestType.only_pytest_types(TestType.all_test_types)
    assert TestType.PYTEST in pytest_types
    assert TestType.PYTHON_PYTEST in pytest_types
    assert TestType.PYTHON not in pytest_types


@pytest.mark.dependency(depends=["test_all_test_types"])
def test_only_script_types():
    script_types = TestType.only_script_types(TestType.all_test_types)
    assert TestType.PYTEST not in script_types
    assert TestType.PYTHON_PYTEST not in script_types
    assert TestType.PYTHON in script_types


@pytest.mark.dependency(depends=["test_all_test_types", "test_only_pytest_types"])
def test_is_only_pytest_types():
    assert not TestType.is_only_pytest_types(TestType.all_test_types)
    assert TestType.is_only_pytest_types(TestType.only_pytest_types(TestType.all_test_types))
