import pytest
import TestSuite
from TestReportMaker import GenerateReport
import os
import pathlib
from RunModelUtil import RunModelUtil
from Test import Test
from TestSuite import TestSuite
from TestResult import TestResult
from TestReportMaker import GenerateReport
import SpecTests
import Mocks
import constants as c

@pytest.mark.skip(reason="eWaterCycle cannot import on pipeline")
# Run a model that implements NOTHING and see if it fails everything, if it somehow succeeds something
# that test does not properly test for anything
def test_FailAllAlways():
    testSuite: TestSuite = TestSuite()
    model = Mocks.worstModelMock()
    result: dict = testSuite.runAll(model)
    if result[c.SUITE_PASSED_ATTRIBUTE]:
        assert False
    else:
        assert True

@pytest.mark.skip(reason="eWaterCycle cannot import on pipeline")
#Runs Wflow model that implements everything correctly
def test_Wflow():
    testSuite: TestSuite = TestSuite()
    model = RunModelUtil.getwflowmodel()
    result: dict = testSuite.runAll(model)
    if result[c.SUITE_PASSED_ATTRIBUTE]:
        assert True
    else:
        assert False

@pytest.mark.skip(reason="eWaterCycle cannot import on pipeline")
#Runs LeakyBucket model that implements everything correctly
def test_LeakyBucket():
    testSuite: TestSuite = TestSuite()
    model = RunModelUtil.getleakymodel()
    result: dict = testSuite.runAll(model)
    if result[c.SUITE_PASSED_ATTRIBUTE]:
        assert True
    else:
        assert False
        