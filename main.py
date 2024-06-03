from RunModelUtil import RunModelUtil
from Test import Test
from TestSuite import TestSuite
from TestResult import TestResult
from TestReportMaker import GenerateReport
import SpecTests
import Mocks
import os.path
import yaml
import constants as c

def main():

    testSuite: TestSuite = TestSuite()

    # model = Mocks.BasicModelMock()
    # model = Mocks.worstModelMock()
    #model = RunModelUtil.getwflowmodel() # Temporary for validating tests
    model = RunModelUtil.getleakymodel()  # Temporary for validating tests

    result: dict = testSuite.runAll(model)
    if result[c.SUITE_PASSED_ATTRIBUTE]:
        # some sort of verification that lets the system know that the branch is tested and can be removed from db
        print("tests passed!")
    else:
        print("tests failed!")

  #  print(result)
    # you can add a filename as extra argument, otherwise filename will be testReport
   # print("Generating Yaml")
    GenerateReport.generateReportYaml(yaml.dump(result), os.path.join(os.getcwd(),  'output'))
   # print("Generating MarkDown")
    GenerateReport.generateMarkDown(result, "output.md", "MockModel v1")

if __name__ == "__main__":
    main()