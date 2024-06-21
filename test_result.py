"""
Module for managing test results.

This module provides a `TestResult` data class to represent the outcome of tests.
"""

from dataclasses import dataclass
import constants as c


@dataclass(frozen=True)
class TestResult:
    """
    A class to represent the result of a test.

    Attributes:
        passed (bool): Indicates whether the test passed.
        reason (str): The reason or message associated with the test result.
            Defaults to c.PASS_MESSAGE.

    Args:
        passed (bool): Whether the test passed.
        reason (str, optional): The reason for the test result.
            Defaults to c.PASS_MESSAGE.
    """
    passed: bool
    reason: str = c.PASS_MESSAGE
