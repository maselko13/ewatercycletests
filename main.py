from RunModelUtil import RunModelUtil
from Test import Test
from TestSuite import TestSuite
from TestResult import TestResult
from TestReportMaker import GenerateReport
import SpecTests
from Mocks import BasicModelMock
import os.path
import yaml


def main():
    test1 = Test(name="TestGetFlow", description="tests if the method getFlow exists", critical=True, enabled=True)
    test1.run = lambda _: TestResult(True)
    test2 = Test(name="MeasureFlow", description="tests if the flow is large enough", critical=False, enabled=True)
    test2.run = lambda _: TestResult(False, "The flow was equal to [8.0] which is lower than [9.0] so the test failed.")
    testSuite = TestSuite()
    SpecTests.addSpecTests(testSuite)
    # model = BasicModelMock()
    # model = RunModelUtil.getwflowmodel() # Temporary for validating tests
    model = RunModelUtil.getleakymodel()  # Temporary for validating tests

    #Simple Test for LeakyBucket
    test3 = Test(name="TestHasAllNonZero", description="tests if the output at each point in the model is not 0", critical=True, enabled=True)
    test3.run = lambda modelx: TestResult(RunModelUtil.neverzero(RunModelUtil.runxarraymodel(modelx, 0, 0.15)), "The output was 0 at some point")
    testSuite.addTest(test3)

    #Simple Test for LeakyBucket
    test4 = Test(name="TestHasTotalNonZero", description="tests if the total output is not 0", critical=True, enabled=True)
    test4.run = lambda modelx: TestResult(RunModelUtil.sum(RunModelUtil.runxarraymodel(modelx, 0, 0.01)), "The total output was 0")
    testSuite.addTest(test4)

    result: list[dict] = testSuite.runAll(model)
    # for now checking if tests are correct is in main, subject to debate though
    passed = True
    for i in result:
        if(result.get(i).get('critical') == True):
            if(result.get(i).get('passed') == False):
                passed = False
    if passed:
        # some sort of verification that lets the system know that the branch is tested and can be removed from db
        print("tests passed!")
    else:
        print("tests not passed!")
    # you can add a filename as extra argument, otherwise filename will be testReport
    GenerateReport.generateReportYaml(yaml.dump(result), os.path.join(os.getcwd(),  'output'))

if __name__ == "__main__":
    main()