import datetime
import re

import numpy as np
import xarray
from Test import Test
from TestResult import TestResult
from TestBank import TestBank
from pathlib import Path

@TestBank(description=None)
class SpecTests:

    @Test(description="tests if the model can be initialized without a proper config file path", critical=True, enabled=False)
    def initializeWrongConfig(model):

        # only path4 results in an actual .json file
        path = "this is not a path"
        path2 = "maybe/valid.json"
        path3 = "valid.json"
        path4 = "cfg.json"
        correct = 0
        try:
            model.initialize(path)
            model.initialize(path2)
            model.initialize(path3)
        except:
            correct = correct + 1
        if correct == 0 :
            return TestResult(False, "model initialized despite invalid path!")
        try:
            model.initialize(path4)
        except:
            return TestResult(False,"model throws exception on valid config file!")
        return TestResult(True)

    # Test that checks if the start/end time of the model is correctly implemented and if it starts before it ends
    @Test(description="Checks if the start time of the model is correct", critical=True, enabled=True)
    def correctStartTime(model):
        try:
            if model.start_time < model.end_time:
                return TestResult(True)
            else:
                return TestResult(False, "Model start time or end time is incorrect")
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? .start_time, .end_time")

    # checks if _check_parameter_set is implemented
    @Test(description="Checks if ._check_parameter_set is implemented", critical=True, enabled=True)
    def hasCheckParameterSet(model):
        try:
            model._check_parameter_set()
            return TestResult(True)
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? ._check_parameter_set")

    # checks if _make_bmi_instance is implemented
    @Test(description="Checks if ._make_bmi_instance is implemented", critical=True, enabled=True)
    def hasMakeBmiInstance(model):
        try:
            model._make_bmi_instance()
            return TestResult(True)
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? ._make_bmi_instance")

    # checks if .parameters is implemented
    @Test(description="Checks if .parameters is implemented", critical=True, enabled=True)
    def hasParameters(model):
        try:
            model.parameters
            return TestResult(True)
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? .parameters")

    # checks if .__repr_args__ is implemented
    @Test(description="Checks if .__repr_args__ is implemented", critical=True, enabled=True)
    def hasReprArgs(model):
        try:
            model.__repr_args__()
            return TestResult(True)
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? .__repr_args")

    # checks if ._make_cfg_dir is implemented
    @Test(description="Checks if _make_cfg_dir is implemented", critical=True, enabled=True)
    def hasMakeCfgDir(model):
         try:
            model._make_cfg_dir
            return TestResult(True)
         except:
             return TestResult(False, "error occurred, are these functions implemented properly? ._make_cfg_dir")

    # checks if ._make_cfg_file is implemented
    @Test(description="Checks if _make_cfg_file is implemented", critical=True, enabled=True)
    def hasMakeCfgFile(model):
        try:
            model._make_cfg_file
            return TestResult(True)
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? ._make_cfg_file")

    # checks if .bmi is implemented
    @Test(description="Checks if .bmi is implemented", critical=True, enabled=True)
    def hasBmi(model):
        try:
            model.bmi
            return TestResult(True)
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? .bmi")

    # checks if .output_var_names, .get_value is implemented and all variables are reachable
    @Test(description="Checks if .output_var_names, .get_value is implemented and all variables are reachable and of type ndarray", critical=True, enabled=True)
    def hasVarsOutAndGets(model):
        try:
            variables = model.output_var_names
            try:
                for variable in variables:
                    val = model.get_value(variable)
                    if not isinstance(val, np.ndarray):
                        return TestResult(False, "variable <" + variable + "> not of type ndarray")
                return TestResult(True)
            except:
                return TestResult(False, "variable <" + variable + "> not gettable, are these function implemented properly? .output_var_names, .get_value")
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? .output_var_names")

    # checks if .start_time_as_isostr is implemented and has correct format
    @Test(description="Checks if .start_time_as_isostr is implemented and has correct format", critical=True, enabled=True)
    def hasStartTimeAsIsoStr(model):
        try:
            iso = model.start_time_as_isostr
            iso_pattern = re.compile("\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ")
            if re.match(iso_pattern, iso) :
                return TestResult(True)
            return TestResult(False, "Incorrect format, should be: YYYY-MM-DDTHH:MM:SSZ not : " + iso)
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? .start_time_as_isostr")

    # checks if .end_time_as_isostr is implemented and has correct format
    @Test(description="Checks if .end_time_as_isostr is implemented and has correct format", critical=True, enabled=True)
    def hasEndTimeAsIsostr(model):
        try:
            iso = model.end_time_as_isostr
            iso_pattern = re.compile("\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ")
            if re.match(iso_pattern, iso) :
                return TestResult(True)
            return TestResult(False, "Incorrect format, should be: YYYY-MM-DDTHH:MM:SSZ not : " + iso)
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? .end_time_as_isostr")

    # checks if .time_as_isostr is implemented and has correct format
    @Test(description="Checks if .time_as_isostr is implemented and has correct format", critical=True, enabled=True)
    def hasTimeAsIsostr(model):
        try:
            iso = model.time_as_isostr
            iso_pattern = re.compile("\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ")
            if re.match(iso_pattern, iso) :
                return TestResult(True)
            return TestResult(False, "Incorrect format, should be: YYYY-MM-DDTHH:MM:SSZ not : " + iso)
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? .time_as_isostr")

    # checks if .start_time_as_datetime is implemented and has correct typing
    @Test(description="Checks if .start_time_as_datetime is implemented and has correct typing", critical=True, enabled=True)
    def hasStartTimeAsDatetime(model):
        try:
            res = model.start_time_as_datetime
            if isinstance(res, datetime.datetime):
                return TestResult(True)
            return TestResult(False, "Incorrect type, should be: datetime not: " + type(res))
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? .start_time_as_datetime")

    # checks if .end_time_as_datetime is implemented and has correct typing
    @Test(description="Checks if .end_time_as_datetime is implemented and has correct typing", critical=True, enabled=True)
    def hasEndTimeAsDatetime(model):
        try:
            res = model.end_time_as_datetime
            if isinstance(res, datetime.datetime):
                return TestResult(True)
            return TestResult(False, "Incorrect type, should be: datetime not: " + str(type(res)))
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? .end_time_as_datetime")

    # checks if .time_as_datetime is implemented and has correct typing
    @Test(description="Checks if .time_as_datetime is implemented and has correct typing", critical=True, enabled=True)
    def hasTimeAsDatetime(model):
        try:
            res = model.time_as_datetime
            if isinstance(res, datetime.datetime):
                return TestResult(True)
            return TestResult(False, "Incorrect type, should be: datetime not: " + str(type(res)))
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? .time_as_datetime")

    # Checks if timestep is positive, gives a warning if it is not, added at behest of Rolf
    @Test(description="Checks if the time step of the model is greater than 0", critical=False, enabled=True)
    def positiveTimeStep(model):
        try:
            if model.time_step > 0:
                return TestResult(True)
            else:
                return TestResult(False, "model time step is negative or zero, is this correct?")
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? .time_step")


    #Test if the model.version method is implemented
    @Test(description="Checks if the .version method of the model is correctly implemented", critical=True, enabled=True)
    def someVersionCondition(model):
        try:
            if model.version.strip() != "":
                return TestResult(True)
            else:
                return TestResult(False,"model does not have version")
        except:
            return TestResult(False,"error occurred, are these functions implemented properly? .version")

    #Checks if .time_units is implemented correctly
    @Test(description="Checks if the .time_unit method of the model is correctly implemented", critical=True, enabled=True)
    def hasTimeUnitCondition(model):
        try:
            model.time_units
            return TestResult(True)
        except:
            return TestResult(False,"error occurred, are these functions implemented properly? .time_units")

    #checks if .get_latlon_grid is implemented correctly
    @Test(description="Checks if the .get_latlon_grid method of the model is correctly implemented", critical=True, enabled=True)
    def hasGetLatLonGrid(model):
        try:
            vars = model.output_var_names
            try:
                for var in vars:
                        lat, lon, shape = model.get_latlon_grid(var)
                        if not (len(lat) == shape[0] and len(lon) == shape[1]):
                            return TestResult(False, "incorrect shape, returned shape: " + str(shape) + " actual shape: " + str([len(lat), len(lon)]))
                return TestResult(True)
            except:
                return TestResult(False, "Could not use method .get_latlon_grid for variable: " + var)
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? .get_value_at_coords, .output_var_names")

    #checks if .get_value_as_xarray is implemented correctly
    @Test(description="Checks if the .get_value_as_xarray method of the model is correctly implemented", critical=True, enabled=True)
    def hasGetValueAsXArray(model):
        try:
            vars = model.output_var_names
            for var in vars:
                res = model.get_value_as_xarray(var)
                if not isinstance(res, xarray.DataArray):
                    return TestResult(False, ".get_value_as_xarray method does not return DataArray for variable: " + var)
            return TestResult(True)
        except:
            return TestResult(False, "error occurred, are these functions implemented properly? .get_value_as_xarray, .output_var_names")

    #check if .get_value_at_coords is implemented properly, does not work for lumped models
    @Test(description="tests if the .get_value_at_coords method is implemented properly", critical=False, enabled=True)
    def hasGetValueAtCoords(model):
        try:
            vars = model.output_var_names
            lat, lon, shape = model.get_latlon_grid(vars[0])
            model.get_value_at_coords(vars[0], lat=[lat[0]], lon=[lon[0]])
            return TestResult(True)
        except:
            return TestResult(False, "error occured, are these functions implemented properly? .get_value_at_coords, .coords_to_indices\n"
                                     "DOES NOT NEED TO BE IMPLEMENTED FOR LUMPED MODELS SUCH AS LEAKYBUCKET")

    # Test that checks if the time of the model is correctly updated
    @Test(description="tests if the time passes properly when the model is updated", critical=True, enabled=True)
    def properTimePassage(model):
        try:
            number = model.time
            model.update()
            if model.time == number + model.time_step:
                return TestResult(True)
            else:
                return TestResult(False, "the model's time does not update properly")
        except:
            return TestResult(False,"error occurred, are these functions implemented properly? .time, .time_step, .update")

    @Test(description="tests if any of the model's grids have are of invalid type", critical=True, enabled=True)
    def invalidGridType(model):

        # list of all correct grid types as per the BMI specification
        valid_types = ['scalar', 'points', 'vector', 'unstructured', 'structured_quadrilateral', 'rectilinear',
                    'uniform_rectilinear']
        temp = 0
        while True:
            try:
                type = model.get_grid_type(temp)
                # use flag while iterating through the list to check if the type is valid
                flag = 0
                for valid in valid_types:
                    if type == valid:
                        flag = 1
                        break
                if flag == 0:
                    return TestResult(False,"The model's grid's type is invalid")
                else:
                    flag = 0
                    temp += 1
            except:
                return TestResult(True)

    @Test(description="tests if any of the model's grids have are of invalid rank", critical=True, enabled=True)
    def invalidGridRank(model):

        temp = 0
        while True:
            try:
                rank = model.get_grid_rank(temp)
                # you can't have 4 or more dimensional models, that's literally impossible
                if rank != 0 and rank != 1 and rank != 2 and rank != 3:
                    return TestResult(False,"the model's grid's rank is invalid")
                temp += 1
            except:
                return TestResult(True)

    @Test(description="tests if the rank of the model's grids matches their type", critical=True, enabled=True)
    def gridTypeMismatch(model):
        temp = 0
        while True:
            try:
                type = model.get_grid_type(temp)
                rank = model.get_grid_rank(temp)
                # ifs used to check if grid types have correct dimensions
                if type == 'scalar' and rank!=0:
                    return TestResult(False,"the model outputs wrong grid data!")
                if type == 'vector' and rank!=1:
                    return TestResult(False, "the model outputs wrong grid data!")
                if type == 'structured_quadrilateral' and rank != 2:
                    return TestResult(False, "the model outputs wrong grid data!")
                if type == 'rectilinear' and rank != 2:
                    return TestResult(False, "the model outputs wrong grid data!")
                if type == 'uniform_rectilinear' and rank != 2:
                    return TestResult(False, "the model outputs wrong grid data!")
                temp += 1
            except:
                return TestResult(True)

    #Test that checks if model can still do stuff after it is finalized
    @Test(description="Checks if the .finalize method of the model is correctly implemented", critical=True, enabled=True)
    def cannotUpdateAfterFinalizeCondition(model):
        try:
            model.finalize()
            try:
                model.update()
                return TestResult(False, "model.finalize was unsuccessful in finalising the model")
            except:
                return TestResult(True,"Finalized correctly")
        except:
            return TestResult(False,"error occurred, are these functions implemented properly? .finalize")
