from ewatercycle.base.model import eWaterCycleModel

from TestResult import TestResult
from typing import Callable, Any
from typing_extensions import Self
import constants as c


"""
Decorators are easy. 
Essentially: 

    @decorator
    def function():
        ...

Is equivalent to:

    def function():
        ...

    function = decorator(function)

Thats it.
"""

class Test:

    # Class attribute, contains all Test instances that are bound to a function.
    boundInstances: dict[str, Self] = dict()

    def __init__(self, name: str = None, description: str = None, critical: bool = None, enabled: bool = None):
        
        if name is not None:
            print("DEPRECATED: setting test name manually. Test name is set to the name of the method automatically, so this step is obsolete.")
        
        self.name: str = name
        self.description: str = description             
        self.critical: bool = critical
        self.enabled: bool = enabled
        self._run: Callable[[eWaterCycleModel], TestResult] = None
        self.testResult: TestResult = None

    @property
    def run(self) -> Callable[[eWaterCycleModel], TestResult]:
        print("DEPRECATED: reading run attribute value. This should never be done externally, call the start method instead.")
        return self._run

    @run.setter
    def run(self, function: Callable[[eWaterCycleModel], TestResult]) -> None:
        print("DEPRECATED: setting run method manually. Please use decorator instead.")
        self.__call__(function)

    def __call__(self, function: Callable[[eWaterCycleModel], TestResult]) -> Self:

        # Verify that no bound Test instance has the same name.
        if function.__name__ in self.boundInstances:
            raise ValueError(f"Test with name [{function.__name__}] already exists.")
        
        # Verify that the Test name is not banned.
        if function.__name__ in c.FORBIDDEN_TEST_NAMES:
            raise ValueError("Tests cannot have the following names: \"" + "\", \"".join(c.FORBIDDEN_TEST_NAMES) + "\"")

        # Set the name of the test to the name of the function. 
        self.name = function.__name__

        # Set the private run method to the function.
        self._run = function

        # Add this Test instance to the list of bound tests.
        self.boundInstances[self.name] = self

        # Guarantee the Test object can be bound only once.
        self.__call__ = None

        # Return the bound Test instance.
        return self

    def start(self, model) -> dict:

        # Verify that the test is bound to a function.
        if self._run is None:
            raise ValueError("Test must be bound to a function before calling .start")

        # Retrieve the test result using the bound function.
        self.testResult = self._run(model)

        return {
            "name": self.name,
            "description": self.description,
            "critical": self.critical,
            "enabled": self.enabled,
            "passed": self.testResult.passed,
            "reason": self.testResult.reason,
        }

