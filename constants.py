"""
A module that includes constants used in the package.
"""

PASS_MESSAGE: str = "The test passed successfully"
VERSION: str = "0.0"
SUITE_PASSED_ATTRIBUTE: str = "passed"
SUITE_VERSION_ATTRIBUTE: str = "suite-version"
FORBIDDEN_TEST_NAMES: list[str] = [SUITE_PASSED_ATTRIBUTE, SUITE_VERSION_ATTRIBUTE]
