"""
A test bank that tests if all methods for a model are implemented correctly.
"""

import datetime
import re
from test import Test
import numpy as np
import xarray #pylint:disable=E0401
from test_result import TestResult
from test_bank import TestBank


@TestBank(description=None)
class SpecTests:
    """
    The test bank that has all the tests that test methods
    a model must implement.
    """

    @staticmethod
    @Test(description="tests if the model can be initialized without a proper config file path", critical=True, enabled=False)
    def initialize_wrong_config(model, _):
        """
        tests if the model can be initialized without a proper config file path
        """
        # only path4 results in an actual .json file
        path = "this is not a path"
        path2 = "maybe/valid.json"
        path3 = "valid.json"
        path4 = "cfg.json"
        correct = 0
        try:
            model.initialize(model, path)
        except:
            correct = correct + 1
        try:
            model.initialize(model, path2)
        except:
            correct = correct + 1
        try:
            model.initialize(model, path3)
        except:
            correct = correct + 1
        if correct != 3:
            return TestResult(False, "model initialized despite invalid path!")
        try:
            model.initialize(model, path4)
        except:
            return TestResult(False, "model throws exception on valid config file!")
        return TestResult(True)

    @staticmethod
    @Test(description="Checks if the start time of the model is correct",
          critical=True, enabled=True)
    def correct_start_time(model, _):
        """
        Test that checks if the start/end time of the model is correctly implemented and if it starts before it ends
        """
        try:
            if model.start_time < model.end_time:
                return TestResult(True)
            return TestResult(False, "Model start time or end time is incorrect")
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? .start_time, .end_time")

    @staticmethod
    @Test(description="Checks if ._check_parameter_set is implemented",
          critical=True, enabled=True)
    def has_check_parameter_set(model, _):
        """
        checks if _check_parameter_set is implemented
        """
        try:
            model._check_parameter_set()
            return TestResult(True)
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? ._check_parameter_set")

    @staticmethod
    @Test(description="Checks if ._make_bmi_instance is implemented",
          critical=True, enabled=True)
    def has_make_bmi_instance(model, _):
        """
        checks if _make_bmi_instance is implemented
        """
        try:
            model._make_bmi_instance()
            return TestResult(True)
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? ._make_bmi_instance")

    @staticmethod
    @Test(description="Checks if .parameters is implemented",
          critical=True, enabled=True)
    def has_parameters(model, _):
        """
        checks if .parameters is implemented
        """
        try:
            model.parameters
            return TestResult(True)
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? .parameters")

    @staticmethod
    @Test(description="Checks if .__repr_args__ is implemented",
          critical=True, enabled=True)
    def has_repr_args(model, _):
        """
        checks if .__repr_args__ is implemented
        """
        try:
            model.__repr_args__()
            return TestResult(True)
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? .__repr_args")

    @staticmethod
    @Test(description="Checks if _make_cfg_dir is implemented",
          critical=True, enabled=True)
    def has_make_cfg_dir(model, _):
        """
        checks if ._make_cfg_dir is implemented
        """
        try:
            model._make_cfg_dir
            return TestResult(True)
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? ._make_cfg_dir")

    @staticmethod
    @Test(description="Checks if _make_cfg_file is implemented",
          critical=True, enabled=True)
    def has_make_cfg_file(model, _):
        """
        checks if ._make_cfg_file is implemented
        """
        try:
            model._make_cfg_file
            return TestResult(True)
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? ._make_cfg_file")

    @staticmethod
    @Test(description="Checks if .bmi is implemented",
          critical=True, enabled=True)
    def has_bmi(model, _):
        """
        checks if .bmi is implemented
        """
        try:
            model.bmi
            return TestResult(True)
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? .bmi")

    @staticmethod
    @Test(description="Checks if .output_var_names, .get_value is implemented and all variables are reachable and of type ndarray",
          critical=True, enabled=True)
    def has_vars_out_and_gets(model, _):
        """
        checks if .output_var_names, .get_value is implemented and all variables are reachable
        """
        try:
            variables = model.output_var_names
            try:
                for variable in variables:
                    val = model.get_value(variable)
                    if not isinstance(val, np.ndarray):
                        return TestResult(False, "variable <" + str(variable) + "> not of type ndarray")
                return TestResult(True)
            except:
                return TestResult(False, "variable <" + str(variable)+ "> not gettable, are these function implemented properly? .output_var_names, .get_value")
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? .output_var_names")

    @staticmethod
    @Test(description="Checks if .start_time_as_isostr is implemented and has correct format",
          critical=True, enabled=True)
    def has_start_time_as_isostr(model, _):
        """
        checks if .start_time_as_isostr is implemented and has correct format
        """
        try:
            iso = model.start_time_as_isostr
            iso_pattern = re.compile(r"\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ")
            if re.match(iso_pattern, iso):
                return TestResult(True)
            return TestResult(False, "Incorrect format, should be: YYYY-MM-DDTHH:MM:SSZ not : " + iso)
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? .start_time_as_isostr")

    @staticmethod
    @Test(description="Checks if .end_time_as_isostr is implemented and has correct format",
          critical=True, enabled=True)
    def has_end_time_as_isostr(model, _):
        """
        checks if .end_time_as_isostr is implemented and has correct format
        """
        try:
            iso = model.end_time_as_isostr
            iso_pattern = re.compile(r"\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ")
            if re.match(iso_pattern, iso):
                return TestResult(True)
            return TestResult(False, "Incorrect format, should be: YYYY-MM-DDTHH:MM:SSZ not : " + iso)
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? .end_time_as_isostr")

    @staticmethod
    @Test(description="Checks if .time_as_isostr is implemented and has correct format",
          critical=True, enabled=True)
    def has_time_as_isostr(model, _):
        """
        checks if .time_as_isostr is implemented and has correct format
        """
        try:
            iso = model.time_as_isostr
            iso_pattern = re.compile(r"\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ")
            if re.match(iso_pattern, iso):
                return TestResult(True)
            return TestResult(False, "Incorrect format, should be: YYYY-MM-DDTHH:MM:SSZ not : " + iso)
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? .time_as_isostr")

    @staticmethod
    @Test(description="Checks if .start_time_as_datetime is implemented and has correct typing",
          critical=True, enabled=True)
    def has_start_time_as_datetime(model, _):
        """
        checks if .start_time_as_datetime is implemented and has correct typing
        """
        try:
            res = model.start_time_as_datetime
            if isinstance(res, datetime.datetime):
                return TestResult(True)
            return TestResult(False, "Incorrect type, should be: datetime not: " + type(res).__name__)
        except:
            return TestResult(False,
                              "error occurred, are these functions implemented properly? .start_time_as_datetime")

    @staticmethod
    @Test(description="Checks if .end_time_as_datetime is implemented and has correct typing",
          critical=True, enabled=True)
    def has_end_time_as_datetime(model, _):
        """
        checks if .end_time_as_datetime is implemented and has correct typing
        """
        try:
            res = model.end_time_as_datetime
            if isinstance(res, datetime.datetime):
                return TestResult(True)
            return TestResult(False, "Incorrect type, should be: datetime not: " + type(res).__name__)
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? .end_time_as_datetime")

    @staticmethod
    @Test(description="Checks if .time_as_datetime is implemented and has correct typing",
          critical=True, enabled=True)
    def has_time_as_datetime(model, _):
        """
        checks if .time_as_datetime is implemented and has correct typing
        """
        try:
            res = model.time_as_datetime
            if isinstance(res, datetime.datetime):
                return TestResult(True)
            return TestResult(False, "Incorrect type, should be: datetime not: " + type(res).__name__)
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? .time_as_datetime")

    @staticmethod
    @Test(description="Checks if the time step of the model is greater than 0",
          critical=False, enabled=True)
    def positive_time_step(model, _):
        """
        Checks if timestep is positive, gives a warning if it is not
        """
        try:
            if model.time_step > 0:
                return TestResult(True)
            return TestResult(False, "model time step is negative or zero, is this correct?")
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? .time_step")

    @staticmethod
    @Test(description="Checks if the .version method of the model is correctly implemented",
          critical=True, enabled=True)
    def some_version_condition(model, _):
        """
        Test if the model.version method is implemented
        """
        try:
            if model.version.strip() != "":
                return TestResult(True)
            return TestResult(False, "model does not have version")
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? .version")

    @staticmethod
    @Test(description="Checks if the .time_unit method of the model is correctly implemented",
          critical=True, enabled=True)
    def has_time_unit_condition(model, _):
        """
        Checks if .time_units is implemented correctly
        """
        try:
            model.time_units
            return TestResult(True)
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? .time_units")

    @staticmethod
    @Test(description="Checks if the .get_latlon_grid method of the model is correctly implemented",
          critical=True, enabled=True)
    def has_get_lat_lon_grid(model, _):
        """
        checks if .get_latlon_grid is implemented correctly
        """
        try:
            var_names = model.output_var_names
        except:
            return TestResult(False,
                              "error occurred, are these functions implemented properly? .output_var_names")
        for var in var_names:
            try:
                lat, lon, shape = model.get_latlon_grid(var)
            except:
                return TestResult(False, "Could not use method .get_latlon_grid for variable: " + str(var))

            if not (len(lat) == shape[0] and len(lon) == shape[1]):
                return TestResult(False, "incorrect shape, returned shape: " + str(shape) + " actual shape: " + str(
                    [len(lat), len(lon)]))
        return TestResult(True)

    @staticmethod
    @Test(description="Checks if the .get_value_as_xarray method of the model is correctly implemented",
          critical=True, enabled=True)
    def has_get_value_as_x_array(model, _):
        """
        checks if .get_value_as_xarray is implemented correctly
        """
        try:
            var_names = model.output_var_names
        except:
            return TestResult(False,
                              "error occurred, are these functions implemented properly? .get_value_as_xarray, .output_var_names")
        for var in var_names:
            try:
                res = model.get_value_as_xarray(var)
            except:
                return TestResult(False,
                                  ".get_value_as_xarray method does not return DataArray for variable: " + str(var))
            if not isinstance(res, xarray.DataArray):
                return TestResult(False,
                                  ".get_value_as_xarray method does not return DataArray for variable: " + str(var))
        return TestResult(True)

    @staticmethod
    @Test(description="tests if the get_value_at_coords method is implemented properly",
          critical=False, enabled=True)
    def has_get_value_at_coords(model, _):
        """
        check if .get_value_at_coords is implemented properly, does not work for lumped models
        """
        try:
            var_names = model.output_var_names
            lat, lon, _ = model.get_latlon_grid(var_names[0])
            model.get_value_at_coords(var_names[0], lat=[lat[0]], lon=[lon[0]])
            return TestResult(True)
        except:
            return TestResult(False,
                              "error occured, are these functions implemented properly? .get_value_at_coords, .coords_to_indices\n"
                              "DOES NOT NEED TO BE IMPLEMENTED FOR LUMPED MODELS SUCH AS LEAKYBUCKET")

    @staticmethod
    @Test(description="tests if the time passes properly when the model is updated",
          critical=True, enabled=True)
    def proper_time_passage(model, _):
        """
        Test that checks if the time of the model is correctly updated
        """
        try:
            number = model.time
            model.update()
            if model.time == number + model.time_step:
                return TestResult(True)
            return TestResult(False, "the model's time does not update properly")
        except:
            return TestResult(False,
                              "error occurred, are these functions implemented properly? .time, .time_step, .update")

    @staticmethod
    @Test(description="tests if any of the model's grids have an invalid type",
          critical=True, enabled=True)
    def invalid_grid_type(model, _):
        """
        tests if any of the model's grids have an invalid type
        """
        valid_types = ['scalar', 'points', 'vector', 'unstructured', 'structured_quadrilateral', 'rectilinear',
                       'uniform_rectilinear']
        temp = 0
        while True:
            try:
                grid_type = model.get_grid_type(temp)
                if grid_type not in valid_types:
                    return TestResult(False,
                                "The model's grid's type is invalid")
                temp += 1
            except:
                return TestResult(True)

    @staticmethod
    @Test(description="tests if any of the model's grids have are of invalid rank",
          critical=True, enabled=True)
    def invalid_grid_rank(model, _):
        """
        tests if any of the model's grids have are of invalid rank
        """
        temp = 0
        while True:
            try:
                rank = model.get_grid_rank(temp)
                if rank not in (0, 1, 2, 3):
                    return TestResult(False, "the model's grid's rank is invalid")
                temp += 1
            except:
                return TestResult(True)

    @staticmethod
    @Test(description="tests if the rank of the model's grids matches their type",
          critical=True, enabled=True)
    def grid_type_mismatch(model, _):
        """
        tests if the rank of the model's grids matches their type
        """
        temp = 0
        while True:
            try:
                grid_type = model.get_grid_type(temp)
                rank = model.get_grid_rank(temp)
                if grid_type == 'scalar' and rank != 0:
                    return TestResult(False, "the model outputs wrong grid data!")
                if grid_type == 'vector' and rank != 1:
                    return TestResult(False, "the model outputs wrong grid data!")
                if grid_type == 'structured_quadrilateral' and rank != 2:
                    return TestResult(False, "the model outputs wrong grid data!")
                if grid_type == 'rectilinear' and rank != 2:
                    return TestResult(False, "the model outputs wrong grid data!")
                if grid_type == 'uniform_rectilinear' and rank != 2:
                    return TestResult(False, "the model outputs wrong grid data!")
                temp += 1
            except:
                return TestResult(True)

    @staticmethod
    @Test(description="Checks if the .finalize method of the model is correctly implemented",
          critical=True, enabled=True)
    def cannot_update_after_finalized_condition(model, _):
        """
        Test that checks if model can still do stuff after it is finalized
        """
        try:
            model.finalize()
            try:
                model.update()
                return TestResult(False, "model.finalize was unsuccessful in finalising the model")
            except:
                return TestResult(True, "Finalized correctly")
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? .finalize")
