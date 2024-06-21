"""
A module that contains a test bank to test if all bmi methods are implemented
"""
#pylint:disable=import-error
#pylint:disable=no-member
from test import Test
import grpc
import numpy as np
import exceptions
from test_result import TestResult
from test_bank import TestBank

@TestBank(description=None)
class BmiSpecTests:
    """
    A test bank that tests if all the bmi methods are implemented correctly
    """

    @staticmethod
    @Test(description="Tests if the bmi method initialize() works with a correct file.",
          critical=True,
          enabled=False)
    def initialize_wrong_config_condition(model, _):
        """
        Tests if the bmi method initialize() works with a correct file.
        """
        # only path2 results in an actual initialization
        # whats path2? the cfg file?
        # this is just wrong in my opinion, the setup of the model is neither a
        # bmi function nor does it have standarized variables
        # it shouldn't be tested beyond checking if it exists
        # will not change this though, commenters might disagree here
        path = "this is not a path"
        try:
            cfg_file, _ = model.setup(leakiness=1)
        except:
            return TestResult(False, "The model does not have a setup function.")
        correct = False

        try:
            model.bmi.initialize(path)
        except:
            correct = True
        if not correct:
            return TestResult(False,
                          "The bmi method initialize() worked without a correct path.")

        try:
            model.bmi.initialize(cfg_file)
        except:
            return TestResult(False,
                        "The bmi method initialize() didn't work with a correct path.")
        return TestResult(True)

    @staticmethod
    @Test(description="Tests if the model has all required methods.",
          critical=True,
          enabled=True)
    def has_required_methods_condition(model, _):
        """
        Tests if the model has all required methods.
        """
        # list of the methods that the ewatercycle library calls
        # and were specified to need implementation.
        try:
            required_methods = [
                "initialize",
                "finalize",
                "update",
                "get_current_time",
                "get_end_time",
                "get_grid_type",
                "get_grid_rank",
                "get_grid_shape",
                "get_grid_size",
                "get_grid_x",
                "get_grid_y",
                "get_output_var_names",
                "get_start_time",
                "get_time_step",
                "get_time_units",
                "get_value_at_indices",
                "get_value",
                "get_var_grid",
                "get_var_itemsize",
                "get_var_nbytes",
                "get_var_type",
                "set_value_at_indices",
                "set_value"
            ]

            for func_name in required_methods:
                if not (hasattr(model.bmi, func_name)
                        and callable(getattr(model.bmi, func_name))):
                    return TestResult(False,
                                      "The model does not have all required methods.")

            return TestResult(True)
        except:
            return TestResult(False,
                      "The model gives an error for checking if all bmi methods exist!")

    @staticmethod
    @Test(description="Tests if the bmi method get_start_time() gets the correct start time.",
          critical=True,
          enabled=True)
    def correct_start_time_condition(model, _):
        """
        Tests if the bmi method get_start_time() gets the correct start time.
        """
        try:
            x = model.bmi.get_start_time()
            if not isinstance(x, (int, float, complex)):
                return TestResult(False,
                            "The bmi method get_start_time() does not return a number.")
            return TestResult(True)
        except:
            return TestResult(False,
                        "The bmi method get_start_time() throws an unexpected error!")

    @staticmethod
    @Test(description="Tests if the bmi method get_current_time() gets the correct time at the start.",
          critical=True,
          enabled=True)
    def correct_time_condition(model, _):
        """
        Tests if the bmi method get_current_time() gets the correct time at the start.
        """
        try:
            x = model.bmi.get_current_time()
            if not isinstance(x, (int, float, complex)):
                return TestResult(False,
                          "The bmi method get_current_time() does not return a number.")
            return TestResult(True)
        except:
            return TestResult(False,
                      "The bmi method get_current_time() throws an unexpected error!")

    @staticmethod
    @Test(description="Tests if the bmi method get_end_time() gets the correct end time.",
          critical=True,
          enabled=True)
    def correct_end_time_condition(model, _):
        """
        Tests if the bmi method get_end_time() gets the correct end time.
        """
        try:
            x = model.bmi.get_end_time()
            if not isinstance(x, (int, float, complex)):
                return TestResult(False,
                              "The bmi method get_end_time() does not return a number.")
            return TestResult(True)
        except:
            return TestResult(False,
                            "The bmi method get_end_time() throws an unexpected error!")

    @staticmethod
    @Test(description="Tests if the bmi method get_current_time() updates correctly after an update() call.",
          critical=True,
          enabled=True)
    def time_passage_condition(model, _):
        """
        Tests if the bmi method get_current_time() updates correctly after an update() call.
        """
        try:
            number = model.bmi.get_current_time()
            model.bmi.update()
            x = model.bmi.get_current_time()
            if not isinstance(x, (int, float, complex)):
                return TestResult(False,
                                  "The bmi method get_current_time() does not return a number after an update() call.")
            if x == number + model.bmi.get_time_step():
                return TestResult(True)
            return TestResult(False,
                              "The bmi method get_current_time() gets the wrong time after an update() call.")
        except:
            return TestResult(False,
                              "The bmi methods get_current_time() or update() throw an unexpected error!")

    @staticmethod
    @Test(description="Tests if the bmi method get_grid_type() gets a valid type.",
          critical=True,
          enabled=True)
    def invalid_grid_type_condition(model, _):
        """
        Tests if the bmi method get_grid_type() gets a valid type.
        """
        # list of all correct grid types as per the BMI specification
        valid_types = ['scalar', 'points', 'vector', 'unstructured',
                       'structured_quadrilateral', 'rectilinear',
                       'uniform_rectilinear']
        temp = 0
        while True:
            if temp == 1000:
                return TestResult(True)
            try:
                grid_type = model.bmi.get_grid_type(temp)
                if grid_type not in valid_types:
                    return TestResult(False,
                                "The bmi method get_grid_type() gives an invalid type.")
                temp += 1
            except Exception as e:
                if isinstance(e, exceptions.VarDoesntExistException):
                    return TestResult(True)
                if isinstance(e, grpc.RpcError) and e.code() == grpc.StatusCode.UNKNOWN:
                    temp += 1
                    continue
                return TestResult(False,
                              "The method get_grid_type() throws an unexpected error!")

    @staticmethod
    @Test(description="Tests if the bmi method get_grid_rank() gets a valid rank.",
          critical=True,
          enabled=True)
    def invalid_grid_rank_condition(model, _):
        """
        Tests if the bmi method get_grid_rank() gets a valid rank.
        """
        temp = 0
        while True:
            if temp == 1000:
                return TestResult(True)
            try:
                rank = model.bmi.get_grid_rank(temp)
                if not isinstance(rank, (int, float, complex)):
                    return TestResult(False,
                             "The bmi method get_grid_rank() does not return a number.")
                # you can't have 4 or more dimensional models
                if rank not in (0, 1, 2, 3):
                    return TestResult(False,
                             "The bmi method get_grid_rank() gives an invalid rank.")
                temp += 1
            except Exception as e:
                if isinstance(e, exceptions.VarDoesntExistException):
                    return TestResult(True)
                if isinstance(e, grpc.RpcError) and e.code() == grpc.StatusCode.UNKNOWN:
                    temp += 1
                    continue
                return TestResult(False,
                              "The method get_grid_rank() throws an unexpected error!")

    @staticmethod
    @Test(description="Tests if the bmi methods get_grid_type() and get_grid_rank() give fitting responses.",
          critical=True,
          enabled=True)
    def grid_type_mismatch_condition(model, _):
        """
        Tests if the bmi methods get_grid_type() and get_grid_rank() give fitting responses.
        """
        temp = 0
        while True:
            if temp >= 1000:
                return TestResult(True)
            try:
                grid_type = model.bmi.get_grid_type(temp)
                rank = model.bmi.get_grid_rank(temp)
                # ifs used to check if grid types have correct dimensions
                type_with_rank = {
                    'scalar': 0,
                    'vector': 1,
                    'structured_quadrilateral': 2,
                    'rectilinear': 2,
                    'uniform_rectilinear': 2,
                }
                if not type_with_rank[grid_type] == rank:
                    return TestResult(False,
                              "The bmi methods get_grid_type() and get_grid_rank() responses don't fit together!")
                temp += 1
            except Exception as e:
                if isinstance(e, exceptions.VarDoesntExistException):
                    return TestResult(True)
                if isinstance(e, grpc.RpcError) and e.code() == grpc.StatusCode.UNKNOWN:
                    temp += 1
                    continue
                return TestResult(False,
                        "The method get_grid_type() or get_grid_rank() throws an unexpected error!")

    #check if this is a correct test
    @staticmethod
    @Test(description="Tests if the method get_grid_shape() gets a valid grid shape.",
          critical=True,
          enabled=True)
    def grid_shape_condition(model, _):
        """
        Tests if the method get_grid_shape() gets a valid grid shape.
        """
        temp = 0
        while True:
            if temp >= 1000:
                return TestResult(True)
            try:

                if not isinstance(model.bmi.get_grid_shape(temp),list):
                    return TestResult(False,
                         "The bmi method get_grid_shape() gives an invalid grid shape.")
                if not len(model.bmi.get_grid_shape(temp)) == 2:
                    return TestResult(False,
                         "The bmi method get_grid_shape() gives an invalid grid shape.")
                temp += 1
            except Exception as e:
                if isinstance(e, grpc.RpcError) and e.code() == grpc.StatusCode.UNKNOWN:
                    temp += 1
                    continue
                return TestResult(False,
                                  "The method get_grid_shape() throws an unexpected error!")

    @staticmethod
    @Test(description="Tests if the bmi method get_grid_size() gets a valid response.",
          critical=True,
          enabled=True)
    def grid_size_condition(model, _):
        """
        Tests if the bmi method get_grid_size() gets a valid response.
        """
        temp = 0
        while True:
            if temp >= 1000:
                return TestResult(True)
            try:
                x = model.bmi.get_grid_size(temp)
                if not isinstance(x, (int, float, complex)):
                    return TestResult(False,
                          "The bmi method get_grid_size() does not return a number.")
                temp += 1
            except Exception as e:
                if isinstance(e, grpc.RpcError) and e.code() == grpc.StatusCode.UNKNOWN:
                    temp += 1
                    continue
                return TestResult(False,
                              "The method get_grid_size() throws an unexpected error!")

    @staticmethod
    @Test(description="Tests if the bmi method get_grid_x() gets a valid response.",
          critical=True,
          enabled=True)
    def get_grid_x_condition(model, _):
        """
        Tests if the bmi method get_grid_x() gets a valid response.
        """
        temp = 0
        while True:
            if temp >= 1000:
                return TestResult(True)
            try:
                x = model.bmi.get_grid_x(temp)
                for n in x:
                    if not isinstance(n, (int, float, complex)):
                        return TestResult(False,
                                          "The bmi method get_grid_x() returns a list with items other than numbers")
                temp += 1
            except Exception as e:
                if isinstance(e, grpc.RpcError) and e.code() == grpc.StatusCode.UNKNOWN:
                    temp += 1
                    continue
                return TestResult(False,
                                  "The method get_grid_x() throws an unexpected error!")

    @staticmethod
    @Test(description="Tests if the bmi method get_grid_y() gets a valid response.",
          critical=True,
          enabled=True)
    def get_grid_y_condition(model, _):
        """
        Tests if the bmi method get_grid_y() gets a valid response.
        """
        temp = 0
        while True:
            if temp >= 1000:
                return TestResult(True)
            try:
                x = model.bmi.get_grid_y(temp)
                for n in x:
                    if not isinstance(n, (int, float, complex)):
                        return TestResult(False,
                                      "The bmi method get_grid_y() returns a list with items other than numbers")
                temp += 1
            except Exception as e:
                if isinstance(e, grpc.RpcError) and e.code() == grpc.StatusCode.UNKNOWN:
                    temp += 1
                    continue
                return TestResult(False,
                                  "The method get_grid_y() throws an unexpected error!")

    @staticmethod
    @Test(description="Tests if bmi method get_output_var_names() gets a list of strings.",
          critical=True,
          enabled=True)
    def get_ouput_var_names_condition(model, _):
        """
        Tests if bmi method get_output_var_names() gets a list of strings.
        """
        try:
            names = model.bmi.get_output_var_names()
            if len(names) == 0:
                return TestResult(False,
                          "The bmi method get_output_var_names() gives an empty list.")
            for s in names:
                if not isinstance(s, str):
                    return TestResult(False,
                                      "The bmi method get_output_var_names() returns a list with items other than strings.")
            return TestResult(True)
        except:
            return TestResult(False,
                  "The bmi method get_output_var_names() gives an unexpected error!")

    @staticmethod
    @Test(description="Tests if the bmi method get_time_step() gets a correct time step.",
          critical=True,
          enabled=True)
    def get_time_step_condition(model, _):
        """
        Tests if the bmi method get_time_step() gets a correct time step.
        """
        try:
            x = model.bmi.get_time_step()
            if not isinstance(x, (int, float, complex)):
                return TestResult(False,
                            "The bmi method get_time_step() does not return a number.")
            if x <= 0:
                return TestResult(False,
                      "The bmi method get_time_step() gives a time step of 0 or lower.")
            return TestResult(True)
        except:
            return TestResult(False,
                          "The bmi method get_time_step() throws an unexpected error!")

    @staticmethod
    @Test(description="Tests if the bmi method get_time_units() works correctly.",
          critical=True,
          enabled=True)
    def test_get_time_units(model, _):
        """
        Tests if the bmi method get_time_units() works correctly.
        """
        try:
            x = model.bmi.get_time_units()
            if not isinstance(x, str):
                return TestResult(False,
                            "The bmi method get_time_units() does not return a string.")
            valid_units = ["days", "hours", "minutes", "seconds", "milliseconds", "microseconds"]
            x_split = x.split(" ")
            if x_split[0] not in valid_units:
                return TestResult(False,
                            "The bmi method get_time_units() gives an invalid unit.")
            if len(x_split) < 2:
                return TestResult(False,
                    "The bmi method get_time_units() does not include the word since.")
            if not x_split[1] == "since":
                return TestResult(False,
                    "The bmi method get_time_units() does not include the word since.")
            return TestResult(True)
        except:
            return TestResult(False,
                          "The bmi method get_time_units() throws an unexpected error!")

    @staticmethod
    @Test(description="Tests if the bmi method get_value_at_indices() gets a list of numbers.",
          critical=True,
          enabled=True)
    def test_get_value_at_indices(model, _):
        """
        Tests if the bmi method get_value_at_indices() gets a list of numbers.
        """
        try:
            temp = 0
            temp2 = 0
            while True:
                if temp == 100:
                    return TestResult(True)
                inds = np.array([temp, temp2])
                x = model.bmi.get_value_at_indices(model.bmi.get_output_var_names()[0], inds)
                if not isinstance(x, np.ndarray):
                    return TestResult(False,
                        "The bmi method get_value_at_indices() does not return a numpy array.")
                temp += 1
                temp2 += 1
        except ValueError:
            return TestResult(True)
        except:
            return TestResult(False,
                  "The bmi method get_value_at_indices() throws an unexpected error!")

    @staticmethod
    @Test(description="Tests if the bmi method get_value() gets a list of numbers.",
          critical=True,
          enabled=True)
    def test_get_value(model, _):
        """
        Tests if the bmi method get_value() gets a list of numbers.
        """
        try:
            x = model.bmi.get_value(model.bmi.get_output_var_names()[0])
            if not isinstance(x, np.ndarray):
                return TestResult(False,
                              "The bmi method get_value() does not return a numpy array.")
            return TestResult(True)
        except:
            return TestResult(False,
                              "The bmi method get_value() throws an unexpected error!")

    @staticmethod
    @Test(description="Tests if the bmi method get_var_grid() returns a number.",
          critical=True,
          enabled=True)
    def test_get_var_grid(model, _):
        """
        Tests if the bmi method get_var_grid() returns a number.
        """
        try:
            x = model.bmi.get_var_grid(model.bmi.get_output_var_names()[0])
            if not isinstance(x, (int, float, complex)):
                return TestResult(False,
                              "The bmi method get_var_grid() does not return a number.")
            return TestResult(True)
        except:
            return TestResult(False,
                          "The bmi method get_var_grid() throws an unexpected error!")

    @staticmethod
    @Test(description="Tests if the bmi method get_var_itemsize() returns a number.",
          critical=True,
          enabled=True)
    def test_get_var_itemsize(model, _):
        """
        Tests if the bmi method get_var_itemsize() returns a number.
        """
        try:
            x = model.bmi.get_var_itemsize(model.bmi.get_output_var_names()[0])
            if not isinstance(x, (int, float, complex)):
                return TestResult(False,
                          "The bmi method get_var_itemsize() does not return a number.")
            return TestResult(True)
        except:
            return TestResult(False,
                      "The bmi method get_var_itemsize() throws an unexpected error!")

    @staticmethod
    @Test(description="Tests if the bmi method get_var_nbytes() returns a number.",
          critical=True,
          enabled=True)
    def test_get_var_nbytes(model, _):
        """
        Tests if the bmi method get_var_nbytes() returns a number.
        """
        try:
            x = model.bmi.get_var_nbytes(model.bmi.get_output_var_names()[0])
            if not isinstance(x, (int, float, complex)):
                return TestResult(False,
                          "The bmi method get_var_nbytes() does not return a number.")
            return TestResult(True)
        except:
            return TestResult(False,
                          "The bmi method get_var_nbytes() throws an unexpected error!")

    @staticmethod
    @Test(description="Tests if the bmi method get_var_type() returns a string.",
          critical=True,
          enabled=True)
    def test_get_var_type(model, _):
        """
        Tests if the bmi method get_var_type() returns a string.
        """
        try:
            x = model.bmi.get_var_type(model.bmi.get_output_var_names()[0])
            if not isinstance(x, (str)):
                return TestResult(False,
                              "The bmi method get_var_type() does not return a string.")
            return TestResult(True)
        except:
            return TestResult(False,
                          "The bmi method get_var_type() throws an unexpected error!")

    @staticmethod
    @Test(description="Tests if the bmi method set_value_at_indices() works correctly.",
          critical=False,
          enabled=True)
    def test_set_value_at_indices(model, _):
        """
        Tests if the bmi method set_value_at_indices() works correctly.
        """
        try:
            name = model.bmi.get_output_var_names()[0]
            values = model.bmi.get_value(name)
            indices = np.array([0, len(values)])
            model.bmi.set_value_at_indices(name, indices, values)
            return TestResult(True)
        except:
            return TestResult(False,
                  "The bmi method set_value_at_indices() throws an unexpected error!")

    @staticmethod
    @Test(description="Tests if the bmi method set_value() works correctly.",
          critical=False,
          enabled=True)
    def test_set_value(model, _):
        """
        Tests if the bmi method set_value() works correctly.
        """
        try:
            name = model.bmi.get_output_var_names()[0]
            model.bmi.set_value(name, model.bmi.get_value(name))
            return TestResult(True)
        except:
            return TestResult(False,
                              "The bmi method set_value() throws an unexpected error!")

    @staticmethod
    @Test(description="Tests if the bmi method finalize() doesn't throw any errors.",
          critical=True,
          enabled=True)
    def finalize_model_condition(model, _):
        """
        Tests if the bmi method finalize() doesn't throw any errors.
        """
        try:
            model.bmi.finalize()
            return TestResult(True)
        except:
            return TestResult(False,
                              "The bmi method finalize() throws an unexpected error!")
