#from ewatercycle.base.model import eWaterCycleModel

from Test import Test
from TestBank import TestBank
import constants as c

class TestSuite:

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(TestSuite, cls).__new__(cls)
            cls.__instance.version = c.VERSION
            cls.__instance.tests = Test.boundInstances
            cls.__instance.testBanks = TestBank.boundInstances
        return cls.__instance

    def getTest(self, name: str) -> Test:
        return self.tests.get(name)

    def getTestBank(self, name: str) -> TestBank:
        return self.testBanks.get(name)

    def addTest(self, test: Test) -> None:
        print("DEPRECATED: by creating and binding a Test object, it is added to the testsuite automatically. So this step is obsolete.")

    def removeTest(self, name: str) -> None:
        print("DEPRECATED: this should never be done.")

    def enableTestBank(self, name: str) -> None:
        testBank: TestBank = self.getTestBank(name)
        if testBank is None:
            raise ValueError("Test with name does not exist.")
        testBank.enableNonCritical()

    def disableTestBank(self, name: str) -> None:
        testBank: TestBank = self.getTestBank(name)
        if testBank is None:
            raise ValueError("Test with name does not exist.")
        testBank.disableNonCritical()

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

    def enableNonCritical(self, name: str) -> None:
        for test in self.tests.values():
            if not test.critical:
                test.enabled = True

    def disableNonCritical(self, name: str) -> None:
        for test in self.tests.values():
            if not test.critical:
                test.enabled = False

    def runAll(self, model) -> dict:
        result = {}
        passed = True
        for test in self.tests.values():
            if test.enabled:
                result[test.name] = test.start(model)
                if test.critical and not test.testResult.passed:
                    passed = False
                if not test.testResult.passed :
                    print("test failed: " + test.name)
        result[c.SUITE_PASSED_ATTRIBUTE] = passed
        return result
