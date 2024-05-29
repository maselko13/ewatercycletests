from Test import Test
from TestResult import TestResult
import constants as c

class TestSuite:

    __instance = None

    def __new__(cls):
        if (cls.__instance is None):
            cls.__instance = super(TestSuite, cls).__new__(cls)
            cls.__instance.version = c.TEST_SUITE_VERSION
            cls.__instance.tests = list()
        return cls.__instance
    
    def getTest(self, name: str) -> Test:
        for test in self.tests:
            if test.name == name:
                return test
        return None

    def addTest(self, newTest: Test) -> None:
        test = self.getTest(newTest.name)
        if test is not None:
            raise ValueError("Test with name already exists.")
        self.tests.append(newTest)

    def removeTest(self, name: str) -> None:
        test: Test = self.getTest(name)
        if test is None:
            raise ValueError("Test with name does not exist.")
        self.tests.remove(test)

    def enableTest(self, name: str) -> None:
        test: Test = self.getTest(name)
        if test is None:
            raise ValueError("Test with name does not exist.")
        if test.critical:
            raise ValueError("You cannot enable a critical test.")
        test.enabled = True

    def disableTest(self, name: str) -> None:
        test: Test = self.getTest(name)
        if test is None:
            raise ValueError("Test with name does not exist.")
        if test.critical:
            raise ValueError("You cannot disable a critical test.")
        test.enabled = False

    def runAll(self, model) -> list[dict]:
        result = {}
        for test in self.tests:
            if test.enabled:
                result[test.name] = test.start(model)
        return result
