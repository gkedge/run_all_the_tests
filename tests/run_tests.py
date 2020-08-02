from pathlib import PurePath, Path
import sys
from typing import Tuple

PROJECT_PATH = Path(__file__).parent.parent.absolute()
assert str(PROJECT_PATH / "src") not in sys.path
sys.path.append(str(PROJECT_PATH / "src"))

from run_all_the_tests import TestCasePath, TestCase, run_all_tests

if __name__ == "__main__":
    project_path: PurePath = Path(__file__).parent.parent.absolute()

    def gen_test_case_path(test_case: str) -> TestCasePath:
        return TestCasePath(project_path, PurePath(test_case))

    all_test_cases: Tuple[TestCase, ...] = (
        TestCase.gen_test_case(gen_test_case_path("tests/test_case/test_test_type.py")),
        TestCase.gen_test_case(gen_test_case_path("tests/test_case/test_test_path.py")),
        TestCase.gen_test_case(gen_test_case_path("tests/test_case/test_test_case.py")),
        TestCase.gen_test_case(gen_test_case_path("tests/test_case")),
        TestCase.gen_test_case(gen_test_case_path("tests/test_test_runner.py")),
        TestCase.gen_test_case(gen_test_case_path("tests")),
    )

    run_all_tests(all_test_cases)
