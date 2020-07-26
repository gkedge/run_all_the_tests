from enum import IntEnum, auto, Enum
from pathlib import PurePath, Path
from typing import List, Optional, Tuple, NamedTuple


class TestCasePath:
    def __init__(self, project_root: PurePath, test_case: PurePath):
        """
        Note: the project_root could be a subproject's root; not necessarily to run of
        the project leveraging this CLI test runner.
        """
        self._project_root: PurePath = project_root
        self._test_case: PurePath = test_case
        self.check_test_case_path()

    @property
    def project_root(self) -> PurePath:
        return self._project_root

    @property
    def test_case(self) -> PurePath:
        return self._test_case

    @property
    def full_test_case_path(self) -> Path:
        project_root: Path = Path(self._project_root).absolute()
        full_test_case_path: Path = (project_root / self._test_case)
        return full_test_case_path

    @property
    def test_case_relative_to_project_root(self) -> PurePath:
        return self.test_case_relative_to(self.project_root)

    def test_case_relative_to(self, path: PurePath) -> PurePath:
        return self.full_test_case_path.relative_to(path)

    def test_case_relative_to_project(self, path: PurePath) -> PurePath:
        if path == self._project_root:
            test_case_relative_to_project = self._project_root
        else:
            test_case_relative_to_project = self._project_root / path.relative_to(
                self._project_root
            )
        return test_case_relative_to_project

    @property
    def is_dir_test_case(self) -> bool:
        return self.full_test_case_path.is_dir()

    def check_test_case_path(self) -> None:
        full_test_case_path: Path = self.full_test_case_path
        if not full_test_case_path.exists():
            raise FileNotFoundError(f"Test case {full_test_case_path} does not exist.")

    @property
    def working_directories(self) -> List[PurePath]:
        """

        :return: list of paths from the project directory to the directory containing the script.
        """
        test_path: PurePath = self.full_test_case_path
        if not self.is_dir_test_case:
            # The last 'part' of the path needs to be a directory, not the script.
            test_path: PurePath = self.full_test_case_path.parent
        # The path fragment between the project_root and the directory containing the script.
        test_path: PurePath = test_path.relative_to(self._project_root)

        # Create a list of full paths for every directory between the project_root and the directory containing the
        # script.
        working_directories: [PurePath] = [self._project_root]
        for next_part in test_path.parts:
            working_directories.append(self._project_root / next_part)
        return working_directories


class Group(IntEnum):
    ONE = auto()
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()


class TestType(Enum):
    """
    TestType enum
    """

    PYTEST = auto()
    PYTHON_PYTEST = auto()
    PYTHON = auto()

    def is_pytest(self) -> bool:
        return self in [TestType.PYTEST, TestType.PYTHON_PYTEST]

    def python_command(self, is_script: bool) -> Optional[str]:
        command: Optional[str] = None
        if self.is_pytest():
            if self == TestType.PYTEST:
                command = "pytest"
            else:
                command = "python -B -m pytest"
        elif is_script:
            command = "python -B"

        return command

    @staticmethod
    def all_test_types() -> Tuple["TestType", ...]:
        return tuple(test_type for test_type in TestType)

    @staticmethod
    def only_pytest_types(
        original_types: Tuple["TestType", ...]
    ) -> Tuple["TestType", ...]:
        return tuple(test_type for test_type in original_types if test_type.is_pytest())

    @staticmethod
    def is_only_pytest_types(original_types: Tuple["TestType", ...]) -> bool:
        for test_type in original_types:
            if not test_type.is_pytest():
                return False

        return True


class TestCase(NamedTuple):
    """
    A Test Case represents a full path to the test script.  The project root directory is used to derive paths from
    the project root to the script.  Those paths are used to determine the working directory to start each test to
    validate that a test script can be run from any directory between the project's root to the script.
    """

    # full_test_case_path can be a file or directory containing test cases
    test_case_path: TestCasePath
    test_types: Tuple[TestType]
    pytest_filter: str
    group: Group

    @classmethod
    def gen_test_case(
        cls,
        test_case_path: TestCasePath,
        group: Group = Group.ONE,
        pytest_filter: str = None,
        test_types: Tuple[TestType, ...] = TestType.all_test_types(),
    ) -> "TestCase":
        """
        This TestCase generator expects the test_case to be a fragment from the project root to the test script.
        The project_root is prepended to the test_case and provided as the 'TestCase.full_test_case_path'
        value. That path is checked to ensure that a file by that 'full_test_case_path' exits.

        :param test_case_path:
        :param group:
        :param pytest_filter: pytest -k string
        :param test_types: for exceptional situations, limit a TestCase to run for limited set of TestType's

        :return: test case paths object

        """

        if test_case_path.is_dir_test_case:
            test_types = TestType.only_pytest_types(test_types)

        if pytest_filter and not TestType.is_only_pytest_types(test_types):
            raise RuntimeError(f"filter {pytest_filter} may only be used for pytests.")

        return TestCase(test_case_path, test_types, pytest_filter, group)

    def __str__(self):
        return (
            f"{self.test_case_path.project_root}::"
            f"{self.test_case_path.test_case_relative_to_project_root}"
        )

    def python_command(self, test_type: TestType) -> Optional[str]:
        command = test_type.python_command(self._is_script)
        if command and test_type.is_pytest() and self.pytest_filter:
            command = f'{command} -k "{self.pytest_filter}"'

        return command

    def test_case_relative_to_cwd(self, working_directory: PurePath) -> PurePath:
        return self.test_case_path.test_case_relative_to(working_directory)

    def cwd_relative_to_project(self, working_directory: PurePath) -> PurePath:
        """
        This method may seem odd, but submodules will have a different project roots
        than the top-level project root.

        :param working_directory: absolute path to cwd
        :return: working directory relative to the test case's project_root
        """

        return self.test_case_path.test_case_relative_to_project(working_directory)

    @property
    def working_directories(self) -> List[PurePath]:
        """

        :return: list of paths from the project directory to the directory containing the script.
        """
        return self.test_case_path.working_directories

    @property
    def _is_script(self) -> bool:
        """
        Determine if the test case is a script that is run (not a pytest).
        A script that is simply run by Python is a file that begins with 'run_' and isn't a directory)
        :return: True/False
        """
        return (
            self.test_case_path.full_test_case_path.stem.startswith("run_")
            and not self.test_case_path.is_dir_test_case
        )