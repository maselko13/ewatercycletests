"""
This module defines the 'TestSuite' class,
a singleton responsible for managing and running a suite of tests.
It provides functionality to enable/disable tests,
run tests on separate threads, and handle critical tests separately.
"""
#pylint:disable=no-member

import os
import shutil
from pathlib import Path
import threading

import scenarios_util
import mocks
from test import Test, TestType
from concurrent.futures import ThreadPoolExecutor
import ewatercycle #pylint:disable=import-error
from test_bank import TestBank
from run_model_util import RunModelUtil
import constants as c
import spec_tests # pylint: disable=unused-import
import bmi_spec_tests # pylint: disable=unused-import
import metric_tests # pylint: disable=unused-import
import error_tests # pylint: disable=unused-import
import scenario_tests # pylint: disable=unused-import


class TestSuite:
    """
    A singleton class to manage and run all created tests and test banks.

    Attributes:
        __instance (TestSuite): Singleton instance of the class.
        version (str): Version of the test suite.
        tests (dict): Dictionary of all bound Test instances.
        test_banks (dict): Dictionary of all bound TestBank instances.
    """

    __instance = None

    def __new__(cls):
        """Ensures that only one instance of TestSuite is created (Singleton pattern).

        Returns:
            TestSuite: The singleton instance of the TestSuite class.
        """
        if cls.__instance is None:
            cls.__instance = super(TestSuite, cls).__new__(cls)
            cls.__instance.version = c.VERSION
            cls.__instance.tests = Test.boundInstances
            cls.__instance.test_banks = TestBank.boundInstances
        return cls.__instance

    def get_test(self, name: str) -> Test:
        """
        Retrieves a test by its name.

        Args:
            name (str): The name of the test to retrieve.

        Returns:
            Test: The test instance if found, None otherwise.
        """
        return self.tests.get(name)

    def get_test_bank(self, name: str) -> TestBank:
        """
        Retrieves a test bank by its name.

        Args:
            name (str): The name of the test bank to retrieve.

        Returns:
            TestBank: The test bank instance if found, None otherwise.
        """
        return self.test_banks.get(name)

    def enable_critical(self) -> None:
        """Enables all critical tests."""
        for test in self.tests.values():
            if test.critical:
                test.enabled = True

    def disable_critical(self) -> None:
        """Disables all critical tests."""
        for test in self.tests.values():
            if test.critical:
                test.enabled = False

    def enable_all(self) -> None:
        """Enables all tests."""
        for test in self.tests.values():
            test.enabled = True

    def disable_all(self) -> None:
        """Disables all tests."""
        for test in self.tests.values():
            test.enabled = False

    # """
    # Runs a test on a single thread, as tests are isolated and new directories
    # made are based on thread id they will not interfere with each other.
    # @param model_name: Name of the model
    # @param forcing: forcing data to be used by the model
    # @param parameter_set: Optional parameter_set for a model
    # @param output_variable_name: The name of the output variable for discharge
    # @param test: The test this thread will run
    # @param result: A dict that keeps track of test info per test
    # @param paths: The path of the new thread_(thread_id) directory made by refreshing a model
    # @param setup_variables: Optional extra necessary setup variables for a model
    # """
    def run_test_thread(self, model_name, forcing, parameter_set, output_variable_name, test, result, setup_variables):
        """
        runs a single test in a tread on a specific model instance
        """
        try:
            if parameter_set is None:
                model_instance = ewatercycle.models.sources[model_name](forcing=forcing)
            else:
                model_instance = ewatercycle.models.sources[model_name](parameter_set=parameter_set, forcing=forcing)
        except:
            # Used for testing.
            model_instance = {
                "basicbmimock": mocks.BasicModelMockWithBmi(),
                "basicmock": mocks.BasicModelMock(),
                "worstmock": mocks.worstModelMock(),
                "faultyinitmock": mocks.FaultyInitMock(),
                "faultytimemock": mocks.FaultyTimeMock(),
                "badvarmock": mocks.BadVariablesMock(),
                "wrongunitsmock": mocks.WrongUnitsBmiMock(),
            }[model_name]

        thread_dir = os.path.join(os.getcwd(), "thread_" + str(threading.get_ident())) + test.name
        try:
            cfg_file, cfg_dir = model_instance.setup(end_time=forcing.end_time, cfg_dir=(thread_dir), **setup_variables)
            model_instance.initialize(cfg_file)
            result[test.name] = test.start(model_instance, output_variable_name)
            # attempt to finalize model if it hasn't been already
            model_instance.finalize()
        finally:
            # remove the created thread directory if it exists.
            shutil.rmtree(thread_dir)

    def run_all(self, model_name, model_type, output_variable_name, parameter_set = None, setup_variables = {}, custom_forcing_name = None, custom_forcing_variables = None) -> dict:
        """
        runs all tests in the test suite on the model
        """

        # Retrieve proper forcing.
        shape = Path(ewatercycle.__file__).parent / "testing/data/Rhine/Rhine.shp"
        if not custom_forcing_name:
            if model_type == 'Lumped':
                forcing = RunModelUtil.get_lumped_forcing(parameter_set, shape)
            else:
                forcing = RunModelUtil.get_distributed_forcing(parameter_set, shape)
        else:
            forcing = RunModelUtil.get_custom_forcing(shape, custom_forcing_name, custom_forcing_variables)

        #ScenarioTest Testbank needs to be first for the setup.
        if "ScenarioTests" in self.test_banks.keys():
            temp = {'ScenarioTests': self.test_banks["ScenarioTests"]}
        else:
            temp = {}
        for (test_bank_name, values) in self.test_banks.items():
            temp[test_bank_name] = values

        # Create and run threads.
        result = {}
        with ThreadPoolExecutor(max_workers=4) as executor:
            for (testbank_name, values) in temp.items():
                if (testbank_name == "ScenarioTests"):
                    if custom_forcing_name is None:
                        forcings = {}
                        for test in values.tests:
                            enum = test.type
                            if ((enum == TestType.BOTH
                                 or (model_type == 'Lumped' and enum == TestType.LUMPED)
                                 or (model_type == 'Distributed' and enum == TestType.DISTRIBUTED))
                                    and test.enabled):
                                if model_type == 'Lumped':
                                    forcings[test.name] = scenarios_util.get_correct_forcing_lumped(test.name)
                                else:
                                    forcings[test.name] = scenarios_util.get_correct_forcing_distributed(test.name)
                        for test in values.tests:
                            enum = test.type
                            if ((enum == TestType.BOTH
                                 or (model_type == 'Lumped' and enum == TestType.LUMPED)
                                 or (model_type == 'Distributed' and enum == TestType.DISTRIBUTED))
                                    and test.enabled):
                                executor.submit(self.run_test_thread, model_name, forcings[test.name], parameter_set, output_variable_name, test, result, setup_variables)

                else:
                    for test in values.tests:
                        enum = test.type
                        if ((enum == TestType.BOTH
                                or (model_type == 'Lumped' and enum == TestType.LUMPED)
                                or (model_type == 'Distributed' and enum == TestType.DISTRIBUTED))
                                and test.enabled):
                            executor.submit(self.run_test_thread, model_name, forcing, parameter_set, output_variable_name, test, result, setup_variables)

        # Checks if tests passed or not
        passed = True
        for test in self.tests.values():
            if test.enabled and test.test_result is not None:
                if test.critical and not test.test_result.passed:
                    passed = False

        result[c.SUITE_PASSED_ATTRIBUTE] = passed
        return result

    def __str__(self):
        return "[TestSuite]\n" + "\n\n".join(str(bank) for bank in self.test_banks.values())