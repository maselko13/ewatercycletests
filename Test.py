from TestResult import TestResult

class Test:

    def __init__(self, name: str, description: str, critical: bool, enabled: bool):
        self.name = name
        self.description = description
        self.critical = critical
        self.enabled = enabled
        self.testResult: TestResult = None # Stores the most recent testresult.

    def run(self, model) -> TestResult:
        pass

    def start(self, model) -> dict:

        self.testResult = self.run(model)

        return {
            "name": self.name,
            "description": self.description,
            "critical": self.critical,
            #"enabled": self.enabled # should always be true. Since methods should not be started if they are not enabled.
            "passed": self.testResult.passed,
            "reason": self.testResult.reason,
        }

