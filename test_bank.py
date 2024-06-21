"""
Module for managing test banks and handling test bank-related exceptions.

This module provides a `TestBank` class to group and manage tests, enabling or disabling them collectively.
It also defines a set of exceptions for handling various errors related to test banks.
"""

from typing import Any
from test import Test
from typing_extensions import Self #pylint:disable=import-error


class TestBankException(Exception):
    """Base exception for all test bank-related errors."""

class DuplicateNameTestBankException(TestBankException):
    """Raised when a test bank name is a duplicate."""
    def __init__(self, name: str) -> None:
        super().__init__(f"TestBank with name [{name}] already exists.")

class NoneNameTestBankException(TestBankException):
    """Raised when a test bank name is set to None."""
    def __init__(self) -> None:
        super().__init__("TestBank name cannot be assigned to None.")

class FinalNameTestBankException(TestBankException):
    """Raised when trying to change the name of a test bank that is already named."""
    def __init__(self):
        super().__init__("TestBank name can only be assigned once.")



class TestBank:
    """A class to group and manage tests collectively.

    Attributes:
        boundInstances (dict): Class attribute, contains all TestBank instances that have been assigned a name.

    Args:
        name (str | None, optional): The name of the test bank. Defaults to None.
        description (str | None, optional): The description of the test bank. Defaults to None.
    """

    # Class attribute, contains all TestBank instances that have been assigned a name.
    boundInstances: dict[str, Self] = {}

    def __init__(self, name: str | None=None, description: str | None=None):
        """Initializes the TestBank instance with optional parameters."""
        self._name: str | None = None
        self.tests: list[Test] = []

        if name:
            self.name = name

        self.description: str | None = description

    @property
    def name(self):
        """Gets the name of the test bank.

        Returns:
            str or None: The name of the test bank.
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """Sets the name of the test bank.

        Args:
            name (str): The name to set.

        Raises:
            FinalNameTestBankException: If the test bank already has a name.
            NoneNameTestBankException: If the name is None.
            DuplicateNameTestBankException: If a test bank with the name already exists.
        """
        # Only allow name assignation once.
        if self._name is not None:
            raise FinalNameTestBankException()

        # Prevent name assignation to None
        if name is None:
            raise NoneNameTestBankException()

        # Verify that no other Bank instances have the same name.
        if name in self.boundInstances:
            raise DuplicateNameTestBankException(name)

        # Set the private name attribute to the new name.
        self._name = name
        self.boundInstances[name] = self

    def __call__(self, cls: Any) -> Self:
        """
        Makes the TestBank instance callable to assign tests from a class.
        Also sets the test bank name to that of the class if it was undefined.

        Args:
            cls (Any): The class from which to assign tests.

        Returns:
            Self: The TestBank instance.
        """
        # If undefined, set the name of the TestBank to the name of the class
        if not self.name:
            self.name = cls.__name__

        # For every attribute and method inside the class
        for attribute in dir(cls):

            # Retrieve the attribute or method
            possible_test: Any = getattr(cls, attribute)

            # Check if it is a Test
            if isinstance(possible_test, Test):

                # If so, add it to the list of tests inside this TestBank.
                self.tests.append(possible_test)

        # Return the TestBank instance.
        return self

    def enable_critical(self) -> None:
        """Enables all critical tests in the test bank."""
        for test in self.tests:
            if test.critical:
                test.enabled = True

    def disable_critical(self) -> None:
        """Disables all critical tests in the test bank."""
        for test in self.tests:
            if test.critical:
                test.enabled = False

    def enable_all(self) -> None:
        """Enables all tests in the test bank."""
        for test in self.tests:
            test.enabled = True

    def disable_all(self) -> None:
        """Disables all tests in the test bank."""
        for test in self.tests:
            test.enabled = False

    def __str__(self):
        return f"{self.name}:\n" + "\n".join(str(test) for test in self.tests)