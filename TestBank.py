from Test import Test
from typing import Any
from typing_extensions import Self

class TestBank:

    boundInstances: dict[str, Self] = dict()

    def __init__(self, description: str = None):
        
        self.name = None
        self.description: str = description
        self.tests: list[Test] = []

    def __call__(self, cls: Any) -> Self:
        
        # Verify that no bound TestBank instance has the same name.
        if cls.__name__ in self.boundInstances:
            raise ValueError(f"TestBank with name [{cls.__name__}] already exists.")

        # Set the name of the testbank to the name of the class
        self.name = cls.__name__

        # Add this TestBank instance to the list of bound testBanks.
        self.boundInstances[cls.__name__] = self

        # For every attribute and method inside the class
        for attribute in dir(cls): 

            # Retrieve the attribute or method
            possibleTest: Any = getattr(cls, attribute)

            # Check if it is a Test
            if isinstance(possibleTest, Test):

                # If so, add it to the list of tests inside this TestBank.
                self.tests.append(possibleTest)

        # Guarantee the TestBank object can be bound only once.
        self.__call__ = None

        # Return the TestBank instance.
        return self

    def enableNonCritical(self) -> None:
        for test in self.tests:
            if not test.critical:
                test.enabled = True

    def disableNonCritical(self) -> None:
        for test in self.tests:
            if not test.critical:
                test.enabled = False


