"""
Module for defining and running tests on eWaterCycle models.

This module provides a `Test` class to represent individual tests.
Each test can be named, described, critical, enabled or disabled, and bound to a function.
The results of the test are stored in a `TestResult` instance.
"""
#pylint:disable=import-error
from typing import Callable
from typing_extensions import Self
from ewatercycle.base.model import eWaterCycleModel
import constants as c
from test_result import TestResult
from enum import Enum

class TestException(Exception):
    """Base exception for all test-related errors."""

class NoneNameTestException(TestException):
    """Raised when a test name is set to None."""
    def __init__(self) -> None:
        super().__init__("Test name cannot be assigned to None.")

class FinalNameTestException(TestException):
    """Raised when trying to change the name of a test that is already named."""
    def __init__(self):
        super().__init__("Test name can only be assigned once.")

class ForbiddenNameTestException(TestException):
    """Raised when a test name is forbidden."""
    def __init__(self, name: str):
        super().__init__("Tests cannot have the following names: \""
                         "\", \"".join(c.FORBIDDEN_TEST_NAMES) + f"\". Test name was: {name}")

class DuplicateNameTestException(TestException):
    """Raised when a test name is a duplicate."""
    def __init__(self, name: str) -> None:
        super().__init__(f"Test with name [{name}] already exists.")

class FinalRunTestException(TestException):
    """Raised when trying to change the run function of a test that already has one."""
    def __init__(self) -> None:
        super().__init__("Test run can only be assigned once.")

class NoneRunTestException(TestException):
    """Raised when the run function of a test is set to None."""
    def __init__(self):
        super().__init__("Test name cannot be assigned to None.")

class UnboundTestException(TestException):
    """Raised when a test is started without a bound function."""
    def __init__(self, name: str):
        super().__init__(f"Test with name [{name}] must be bound to a function, before "
                         "calling .start")

class TestType(Enum):
    LUMPED = 1
    DISTRIBUTED = 2
    BOTH = 3

class Test:
    """A class to represent a test.

    Attributes:
        boundInstances (dict): Class attribute, contains all Test instances that are
            bound to a function.
        existingTestNames (set): Class attribute, contains all names of test instances.

    Args:
        name (str, optional): Name of the test. Defaults to None.
        description (str, optional): Description of the test. Defaults to None.
        critical (bool, optional): Indicates if the test is critical. Defaults to False.
        enabled (bool, optional): Indicates if the test is enabled. Defaults to True.
        run (Callable, optional): Function to run the test. Defaults to None.
    """

    boundInstances: dict[str, Self] = {}
    existingTestNames: set[str] = set()

    def __init__(self,
            name: str | None = None,
            description: str | None = None,
            critical: bool = False,
            enabled: bool = True,
            run: Callable[[eWaterCycleModel, str], TestResult] | None = None,
            location: str = "ReesGermany",
            test_type: TestType = TestType.BOTH

        ):
        """Initializes the Test instance with optional parameters."""
        self._name: str | None = None
        self._run: Callable[[eWaterCycleModel, str], TestResult] | None = None

        if name:
            self.name = name
        if run:
            self.run = run

        self.description: str | None = description
        self.critical: bool = critical
        self.enabled: bool = enabled
        self.location = location
        self.test_result: TestResult | None = None
        self.type: TestType = test_type

    @property
    def name(self) -> str | None:
        """Gets the name of the test.

        Returns:
            str or None: The name of the test.
        """
        return self._name

    @name.setter
    def name(self, name) -> None:
        """Sets the name of the test.

        Args:
            name: The name to set.

        Raises:
            NoneNameTestException: If the name is None.
            FinalNameTestException: If the test already has a name.
            ForbiddenNameTestException: If the name is forbidden.
            DuplicateNameTestException: If a test with the name already exists.
        """
        if name is None:
            raise NoneNameTestException()

        if self._name is not None:
            raise FinalNameTestException()

        if name in c.FORBIDDEN_TEST_NAMES:
            raise ForbiddenNameTestException(name)

        if name in self.existingTestNames:
            raise DuplicateNameTestException(name)

        self._name = name
        self.existingTestNames.add(name)

    @property
    def run(self) -> Callable[[eWaterCycleModel], TestResult] | None:
        """Gets the function that runs the test.

        Returns:
            Callable | None: The function that runs the test.
        """
        return self._run

    @run.setter
    def run(self, function):
        """Binds the test to a function. Also sets the test name to that of the function if it was previously undefined.

        Args:
            function: The function to set.

        Raises:
            FinalRunTestException: If the run function is already set.
            NoneRunTestException: If the function is None.
        """
        if self._run is not None:
            raise FinalRunTestException()

        if function is None:
            raise NoneRunTestException()

        self._run = function

        if not self.name:
            self.name = function.__name__

        self.boundInstances[self.name] = self

    def __call__(self, function):
        """Makes the Test instance callable.

        Args:
            function: The function to set as the run method.

        Returns:
            Self: The Test instance.
        """
        self.run = function
        return self

    def start(self, model, discharge_name) -> dict:
        """Runs the test on the provided model, stores the result in .testResult, and returns a complete test result as a dict.

        Args:
            model: The model to test.

        Returns:
            dict: The result of the test. With values for the keys: name, description,
                critical, enabled, passed, and reason.

        Raises:
            UnboundTestException: If the test is not bound to a function.
        """
        # Verify that the test is bound to a function.
        if self._run is None:
            raise UnboundTestException(self.name)

        # Retrieve the test result using the bound function.
        self.test_result = self._run(model, discharge_name)

        return {
            "name": self.name,
            "description": self.description,
            "critical": self.critical,
            "enabled": self.enabled,
            "passed": self.test_result.passed,
            "reason": self.test_result.reason,
        }

    def __str__(self):
        return f"Test(name={self.name}, critical={self.critical}, enabled={self.enabled}, test_type={self.type})"

