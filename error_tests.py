"""
A module that includes a test bank for error testing.
"""
from test import Test, TestType
import numpy as np
from test_result import TestResult
from test_bank import TestBank

#pylint:disable=bare-except

@TestBank(description="Tests if errors are thrown when incorrect variables are called")
class ErrorTests:
    """
    A test bank with tests for testing errors if errors are thrown at the correct time
    """

    @staticmethod
    @Test(description="checks if error is thrown when incorrect variable is called",
          critical=True, enabled=True)
    def incorrect_var_name_condition(model, _):
        """
        Test to see if error is thrown when an incorrect variable is called

        Args:
        model: the hydrological model to be tested.
        """
        try:
            var_names = model.output_var_names
            model.get_value(var_names[0] + "averylongnamethatisnotonthelist")
            return TestResult(False,
                              "Error should have been thrown on incorrect variable")
        except:
            return TestResult(True)

    @staticmethod
    @Test(description="checks if error is thrown when incorrect variable is called",
          critical=True, enabled=True)
    def incorrect_var_name_condition_bmi(model, _):
        """
        Test to see if error is thrown when incorrect variable is called

        Args:
        model: the hydrological model to be tested.
        """
        try:
            var_names = model.output_var_names
            model._bmi.get_value(var_names[0] + "averylongnamethatisnotonthelist")
            return TestResult(False,
                              "Error should have been thrown on incorrect variable")
        except:
            return TestResult(True)

    @staticmethod
    @Test(description="checks if error is thrown when incorrect variable is called",
          critical=True, enabled=True)
    def incorrect_var_name_xarray_condition(model, _):
        """
        Test to see if error is thrown when incorrect variable is called

        Args:
        model: the hydrological model to be tested.
        """
        try:
            var_names = model.output_var_names
            model.get_value_as_xarray(
                var_names[0] + "averylongnamethatisnotonthelist")
            return TestResult(False,
                              "Error should have been thrown on incorrect variable")
        except:
            return TestResult(True)

    @staticmethod
    @Test(description="tests if the model can run from start to " +
          "end without throwing an error",
          critical=True, enabled=True)
    def model_runs_to_completion(model, discharge_name):
        """
        Test that looks if no errors are thrown when running model in
        its entirety

        Args:
        model: the hydrological model to be tested.
        discharge_name: variable that denotes model output name
        """
        try:
            while model.time < model.end_time:
                model.update()

            return TestResult(True)
        except Exception as e:
            return TestResult(False, "While running model threw error " + str(e))

    @staticmethod
    @Test(description="Test that checks if error is thrown " +
          "when calling value outside of the array",
          critical=True, enabled=True, test_type=TestType.DISTRIBUTED)
    def num_outside_array_condition(model, discharge_name):
        """
        Test that looks if errors are thrown when calling for
        value outside of shape

        Args:
        model: the hydrological model to be tested.
        discharge_name: variable that denotes model output name
        """
        try:
            lat, lon, shape = model.get_latlon_grid(discharge_name)
            model.get_value_at_coords(discharge_name,
                                      lat=[lat[shape[0]+3]], lon=[lon[shape[1]+3]])
            return TestResult(False,
                              "Model should fail if value outside array is called")
        except:
            return TestResult(True)

    @staticmethod
    @Test(description="Test that checks if error is thrown " +
                      "when calling latlon grid for variable not in model",
                      critical=True, enabled=True, test_type=TestType.DISTRIBUTED)
    def incorrect_var_name_latlon_condition(model, _):
        """
        Test that looks if errors are thrown when calling for
        variable not in model for .get_latlon_grid

        Args:
        model: the hydrological model to be tested.
        """
        try:
            var_names = model.output_var_names
            model.get_latlon_grid(var_names[0]+"averylongnamethatisnotonthelist")
            return TestResult(False,
                              "Error should have been thrown on incorrect variable")
        except:
            return TestResult(True)

    @staticmethod
    @Test(description="Test that checks if error is thrown " +
                      "when incorrect variable is called",
          critical=True, enabled=True)
    def incorrect_var_name_val_indices_condition_bmi(model, _):
        """
        Test that looks if errors are thrown when calling for
        variable not in model for .bmi.get_value_at_indices

        Args:
        model: the hydrological model to be tested.
        """
        try:
            var_names = model.output_var_names
            model.bmi.get_value_at_indices(var_names[0]+
                                           "averylongnamethatisnotonthelist",
                                           np.array([0,0]))
            return TestResult(False,
                              "Error should have been thrown on incorrect variable")
        except:
            return TestResult(True)

    @staticmethod
    @Test(description="Test that checks if error is thrown " +
                      "when incorrect variable is called",
          critical=True, enabled=True, test_type=TestType.DISTRIBUTED)
    def incorrect_var_name_itemsize_condition_bmi(model, _):
        """
        Test that looks if errors are thrown when calling for
        variable not in model for .bmi.get_var_itemsize

        Args:
        model: the hydrological model to be tested.
        """
        try:
            var_names = model.output_var_names
            model.bmi.get_var_itemsize(var_names[0]+"averylongnamethatisnotonthelist")
            return TestResult(False,
                              "Error should have been thrown on incorrect variable")
        except:
            return TestResult(True)

    @staticmethod
    @Test(description="Test if error is thrown " +
                      "on .get_var_nbytes for incorrect variable",
          critical=True, enabled=True, test_type=TestType.DISTRIBUTED)
    def incorrect_var_name_nbytes_condition_bmi(model, _):
        """
        Test that looks if errors are thrown when calling for
        variable not in model for .bmi.get_var_nbytes

        Args:
        model: the hydrological model to be tested.
        """
        try:
            var_names = model.output_var_names
            model.bmi.get_var_nbytes(var_names[0]+"averylongnamethatisnotonthelist")
            return TestResult(False,
                              "Error should have been thrown on incorrect variable")
        except:
            return TestResult(True)
