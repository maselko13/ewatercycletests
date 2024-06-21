"""Module containing all the mocks that are used for validation testing.

Most mocks in this module are used for validation of the BmiSpecTests and SpecTests bank.
Some of them are also used for integration tests.
Each mock is supposed to closely mirror the methods that are expected of a hydrological model.
"""
import datetime as dt
import numpy as np
import xarray
import exceptions
import ewatercycle.models

class BasicModelMock:
    """The basic model mock.

    This mock contains all necessary methods to make the specification-based tests pass.
    Some of the methods simply return, some have a tad more elaborate functionality.
    This mock also contains a lot of placeholder variables, also to make the specification-based tests pass.
    Many models in this module are children of this model.
    """

    notdischarge = 3.0
    parameters = ()
    _make_cfg_dir = 0
    _make_cfg_file = 0
    bmi = 32
    output_var_names = ['name1', 'name2']
    start_time_as_isostr = "2015-12-03T12:05:72Z"
    time_as_isostr = "2015-12-05T12:05:72Z"
    end_time_as_isostr = "2015-12-07T12:05:72Z"
    start_time_as_datetime = dt.datetime(32,10,1,12,32,22,11)
    end_time_as_datetime = dt.datetime(35,10,5,12,32,22,11)
    time_as_datetime = dt.datetime(33,7,3,12,32,22,11)
    version = "1.2"
    time_units = "seconds"
    finalized = False

    def __init__(self) -> None:
        """Create a new basic model mock.

        When created, the basic model mock sets its vital time and time step variables,as well as the 'finalized' boolean.
        """
        self.time = 0.0
        self.start_time = 0.0
        self.end_time = 3.0
        self.time_step = 1.0
        self.finalized = False

    def initialize(self, *args, **kwargs):
        """Initialize the basic model mock.

        When initialized, the basic model mock sets its vital time and time step variables,as well as the 'finalized' boolean.
        """
        # hardcoded for now
    #    if cfg != "cfg.json":
     #      raise Exception('nuh-uh')
        self.start_time = 3.0
        self.time = 3.0
        self.end_time = 100.0
        self.finalized = False

    def setup(self, *, cfg_dir: str | None = None, **kwargs) -> tuple[str, str]:
        """Mock the setup method.

        This method simply follows the proper return pattern of a regular model.
        """
        if cfg_dir != "cfg.json":
            raise ValueError("Invalid config.")
        return "", ""

    def finalize(self):
        """Mock the finalize method.

        This method simply sets the 'finalized' attribute to true, to ensure that the update() method cannot be called.
        """
        self.finalized = True

    def update(self):
        """Mock the update method.

        This method updates the model 'time' attribute by its 'time_step' attribute.
        It will not work if the finalize() method has already been called on the mock.
        """
        if self.finalized is True:
            raise Exception("the model has already finalized!")
        self.time = self.time + self.get_time_step()

    def get_current_time(self):
        """Mock the get_current_time method."""
        return self.time

    def get_end_time(self):
        """Mock the get_end_time method."""
        return self.end_time

    def get_grid_type(self,number):
        """Mock the get_grid_type method.

        This mock supposedly only has 2 grids, hence this if clause.
        """
        if number == 0:
            return 'scalar'
        if number == 1:
            return 'rectilinear'
        raise exceptions.VarDoesntExistException

    def get_grid_rank(self,number):
        """Mock the get_grid_rank method.

        This mock only has 2 grids, hence this if clause.
        """
        if number == 0:
            return 0
        if number == 1:
            return 2
        raise exceptions.VarDoesntExistException

    def get_grid_shape(self,number):
        """Mock the get_grid_type method.

        This mock only has 2 grids, hence this return value.
        """
        return [number,number]

    def get_grid_size(self,number):
        """Mock the get_grid_size method."""
        return number*number

    def get_grid_x(self,number):
        """Mock the get_grid_x method."""
        return (number,number+1)

    def get_grid_y(self,number):
        """Mock the get_grid_y method."""
        return (number+1,number+3.0)

    def get_output_var_names(self):
        """Mock the get_output_var_names method.

        The mock only contains 2 named variables.
        """
        return ['name1', 'name2']

    def get_var_grid(self,value):
        """Mock the get_var_grid method.

        The mock only contains 2 named variables, hence this if clause.
        """
        if value == 'name1':
            return 2
        if value == 'name2':
            return 3.0
        raise exceptions.VarDoesntExistException

    def get_var_itemsize(self,value):
        """Mock the get_var_itemsize method."""
        return self.get_var_grid(value)

    def get_var_nbytes(self,value):
        """Mock the get_var_nbytes method."""
        return self.get_var_itemsize(value)

    def get_var_type(self,value):
        """Mock the get_var_type method.

        The mock only contains 2 named variables, hence this if clause.
        """
        if value == 'name1':
            return 'int'
        if value == 'name2':
            return 'float'
        raise exceptions.VarDoesntExistException

    def set_value_at_indices(self,var1,var2,var3):
        """Mock the set_value_at_indices method."""
        return

    def set_value(self,value,value2):
        """Mock the set_value method."""
        return

    def get_start_time(self):
        """Mock the get_start_time method."""
        return self.start_time

    def get_time_step(self):
        """Mock the get_time_step method."""
        return self.time_step

    def get_time_units(self):
        """Mock the get_time_units method."""
        return "days since 1970"

    def _check_parameter_set(self):
        """Mock the _check_parameter_set method."""
        return

    def _make_bmi_instance(self):
        """Mock the _make_bmi_instance method."""
        return

    def __repr_args__(self):
        """Mock the __repr_args__ method."""
        return

    def get_value(self,value):
        """Mock the get_value method.

        The mock only contains 2 variables, 'name1' and 'name2, hence this if clause.
        """
        if value == 'name1':
            return np.ndarray(3)
        if value == 'name2':
            return np.ndarray(5)

    def get_latlon_grid(self,value):
        """Mock the get_latlon_grid method.

        The mock only contains 2 variables, 'name1' and 'name2, hence this if clause.
        """
        if value == 'name1':
            return ("abc", "efg", (3, 3))
        if value == 'name2':
            return ("thisshouldwork", "test22", (14, 6))

    def get_value_as_xarray(self,value):
        """Mock the get_value_as_xarray method.

        The mock only contains 2 variables, 'name1' and 'name2, hence this if clause.
        """
        if value == 'name1':
            return xarray.DataArray(2)
        if value == 'name2':
            return xarray.DataArray(3)

    def get_value_at_coords(self,value,lat,lon):
        """Mock the get_value_at_coords method for one of the 2 variables."""
        if value == 'name1':
            return (lat,lon)

    def get_value_at_indices(self,var,var2):
        """Mock the get_value_at_indices method."""
        raise ValueError

class worstModelMock:
    """The worst model mock.

    This is a mock that implements nothing which makes it fail every test.
    """

    def __init__(self) -> None:
        """Mock the __init__ method."""
        return
    def setup(self, cfg_dir):
        """Mock the setup method."""
        return "", ""

    def initialize(self, cfg_file):
        """Mock the initialize method."""
        return

class FaultyTimeMock(BasicModelMock):
    """The faulty time mock.

    This mock is a child of the basic model mock that has all sorts of mistakes regarding time and time methods.
    It has many various time-related attributes which are all in the wrong format to make their respective tests fail.
    """

    version = ""
    start_time_as_isostr = "20153-12-03T12:05:72Z"
    time_as_isostr = "2015312-03T12:05:72Z"
    end_time_as_isostr = "20153-12-03:12:05:72"
    start_time_as_datetime = "12:05"
    end_time_as_datetime = 150345
    time_as_datetime = 150345.0

    def __init__(self) -> None:
        """Create a new FaultyTimeMock.

        When created, the FaultyTim mock sets its end time lower than its start time and sets its time step to negative as both of these make related tests fail.
        """
        self.time = 13.0
        self.start_time = 15.0
        self.end_time = 1.0
        self.time_step = -4.0

    def initialize(self, cfg):
        """Mock the initialize method."""
        self.start_time = 15.0
        self.time = 10.0
        self.end_time = 1.0

    def update(self):
        """Mock the update method.

        When this mock is updated, it decreases its time by its time step instead of increasing it, failing the respective test.
        """
        self.time == self.time - self.time_step

    def get_time_units(self):
        """Mock the get_time_units method, returning an incorrect format."""
        return "years"

class FaultyTimeMock2(FaultyTimeMock):
    """Simple class created from FaultyTimeMock for the sake of additional branch coverage of one of the validation tests."""

    def get_time_units(self):
        """Mock the get_time_units method, returning an incorrect format."""
        return "days"

class FaultyInitMock(BasicModelMock):
    """The faulty initalization mock.

    This mock is a child of the basic model mock that contains incorrect updating, initialization and finalization methods.
    """

    def setup(self, cfg_dir):
        """Mock the setup method."""
        return ("path " + str(cfg_dir) + "!",0),""

    def initialize(self,cfg):
        """Mock the initialize method."""
        # if not cfg.endswith(".json"):
        #    raise Exception('nuh-uh')
        return

    def finalize(self):
        """Mock the finalize method without doing anything."""
        return

    def update(self):
        """Mock the update method without doing anything."""
        return



class FaultyInitMock2(FaultyInitMock):
    """Simple class created from FaultyInitMock for the sake of additional branch coverage of the validation tests."""

    def setup(self,leakiness):
        """Mock the setup method."""
        return ("path " + str(leakiness) + "!",0),""

    def initialize(self, cfg):
        """Mock the initialize method."""
        return

class BadVariablesMock(BasicModelMock):
    """The bad variables mock.

    This mock is a child of the basic model mock that contains incorrect variables and getters.
    """

    output_var_names = (3 , 5)

    def get_output_var_names(self):
        """Mock the get_output_var_names method."""
        return self.output_var_names

    def get_value(self,value):
        """Mock the get_value method.

        for the 2nd variable , "5", this method does not return an ndarray, failing the respective test.
        """
        if value == 3:
            return np.ndarray(3)
        if value == 5:
            return 5

    def get_latlon_grid(value):
        """Mock the get_latlon_grid method.

        for the 2nd variable, "5", this method returns a wrong grid size, failing the respective test.
        """
        if value == 3:
            return ("abc","efg",(3,3))
        if value == 5:
            return ("adsev","test22",(4,6))

    def get_grid_type(self, number):
        """Mock the get_grid_type method.

        on the number == 4 condition, there is a typo in the grid type, failing the respective test.
        """
        if number == 0:
            return 'scalar'
        if number == 1:
            return 'rectilinear'
        if number == 2:
            return 'rectilinear'
        if number == 3:
            return 'rectilinear'
        if number == 4:
            return 'rectilineer'
        else:
            raise exceptions.VarDoesntExistException

    def get_grid_rank(self, number):
        """Mock the get_grid_rank method.

        on the number == 3 condition, the method returns that a grid is 4-dimensional, which is clearly impossible.
        """
        if number == 0:
            return 0
        if number == 1:
            return 2
        if number == 2:
            return 2
        if number == 3:
            return 4
        raise exceptions.VarDoesntExistException

    def get_grid_shape(self, number):
        """Mock the get_grid_shape method."""
        return number

    def get_grid_size(self,number):
        """Mock the get_grid_size method."""
        return "fairly big"

    def get_grid_x(self,number):
        """Mock the get_grid_x method with wrong typing."""
        return [number,3,5,"not a number"]

    def get_grid_y(self,number):
        """Mock the get_grid_y method with wrong sizes and typing."""
        if number == 0:
            return [3,5]
        if number == 1:
            return [3,5,7]
        return [number,3,2,"not a number"]

    def get_value_at_indices(self,var,var2):
        """Mock the get_value_at_indices method by simply returning a number."""
        return 3

    def get_value(self,var):
        """Mock the get_value method with wrong typing."""
        return "nope"

    def get_var_grid(self,value):
        """Mock the get_var_grid method with wrong typing."""
        return "grid"

    def get_var_itemsize(self,value):
        """Mock the get_var_itemsize method."""
        return "2"

    def get_var_nbytes(self,value):
        """Mock the get_var_nbytes method with wrong typing."""
        return "16"

    def get_var_type(self,value):
        """Mock the get_grid_shape method by returning a zero(wrong typing)."""
        return 0

class ErrorThrowerMock(BasicModelMock):
    """The error thrower mock.

    This mock is a child of the basic model mock that contains methods that throw errors to test error tests.
    """
    def get_value(self, value):
        """Mock the get_value method with error throw."""
        raise Exception("no value")

    def get_value_as_xarray(self, value):
        """Mock the get_value method with error throw."""
        raise Exception("no value")

    def update(self):
        """Mock the update method with error throw."""
        raise Exception("no value")

    def get_latlon_grid(self, value):
        """Mock the get_latlon_grid method with exception."""
        if value.contains("averylongnamethatisnotonthelist"):
            raise Exception("no value")
        return [0], [0], [1,1]

    def get_value_at_coords(self, value, lat, lon):
        """Make mock crash by calling lat and lon."""
        lat += lon

    def get_value_at_indices(self, var, var2):
        """Mock the get_latlon_grid method with exception."""
        raise Exception("no value")

    def get_var_itemsize(self, value):
        """Mock the get_var_itemsize method with exception."""
        raise Exception("no value")

    def get_var_nbytes(self, value):
        """Mock the get_var_nbytes method with exception."""
        raise Exception("no value")

class ArrayTooSmallMock(BasicModelMock):
    """The ArrayTooSmallMock mock.

    This mock is a child of the basic model mock that contains an array that will be too small throwing an error.
    """

    def get_latlon_grid(self, value):
        """Mock the get_latlon_grid method with incorrect info."""
        return [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [1,1]

    def get_value_at_coords(self,value,lat,lon):
        """attempt to make mock crash by calling lat and lon."""
        lat += lon

class NoErrorMock(BasicModelMock):
    """The IndicesNoErrorMock mock.

    This mock is a child of the basic model mock that
    contains methods that return without error.
    """

    def get_value_at_indices(self, var, var2):
        """Mock the get_value_at_indices method."""
        return

    def get_var_itemsize(self, value):
        """Mock the get_var_itemsize method."""
        return

    def get_var_nbytes(self, value):
        """Mock the get_var_nbytes method."""
        return

class NoGettersMock:
    """The no getters mock.

    This is a simple mock, containing one attribute that is missing all getters.
    """

    output_var_names = (3 , 5)

class FaultyTimeBmi():
    """The bmi for the faulty time mock.

    This is a mock of mock's bmi, that wrongfully mocks bmi methods related to time.
    """

    def get_current_time(self):
        """Mock the get_current_time method with the wrong format."""
        return "today"

    def get_end_time(self):
        """Mock the get_end_time method with the wrong format."""
        return "tomorrow"

    def get_start_time(self):
        """Mock the get_start_time method with the wrong format."""
        return "yesterday"

    def get_time_step(self):
        """Mock the get_time_step method with the wrong format."""
        return "1 day"

    def get_time_units(self):
        """Mock the get_time_units method with the wrong format."""
        return 2.0

    def update(self):
        """Mock the update method."""
        return

"""This section of the module contains model mocks with bmi.

These mocks are needed for bmi specification-based tests. 
As the BmiSpecTests test models bmi attributed and are very similar in nature to the regular specification-based tests, 
a few methods and attributes were added to the mocks and calling them with a bmi simply sets their bmi attribute to a new instance of the same mock.
"""

class BasicModelMockWithBmi(BasicModelMock):
    """The basic model mock with bmi."""

    bmi = BasicModelMock()

class FaultyInitMockWithBmi(FaultyInitMock):
    """The faulty initialization mock with bmi."""

    bmi = FaultyInitMock()

class FaultyInitMock2WithBmi(FaultyInitMock2):
    """The second faulty initialization mock with bmi."""

    bmi = FaultyInitMock2()

class WrongUnitsBmiMock(BasicModelMock):
    """The wrong units mock with bmi."""

    bmi = FaultyTimeBmi()

class FaultyTimeMockWithBmi(FaultyTimeMock):
    """The faulty time mock with bmi."""

    bmi = FaultyTimeMock()

class BadVariablesMockWithBmi(BadVariablesMock):
    """The bad variables mock with bmi."""

    bmi = BadVariablesMock()

class FaultyTimeMock2WithBmi(FaultyTimeMock2):
    """The second faulty time mock with bmi."""

    bmi = FaultyTimeMock2()

class ErrorThrowerBmiMock(ErrorThrowerMock):
    bmi = ErrorThrowerMock()

class NoErrorBmiMock(NoErrorMock):
    bmi = NoErrorMock()

class ScenarioDistributedMock(BasicModelMock):
    counter = 0
    output = []

    def setup(self,forcing):
        self.counter = 0
        self.output = []
        path = str(forcing.directory) + "/" + forcing.filenames.get('pr')
        data = xarray.open_dataset(path)
        for a in enumerate(data['pr'].values):
            for grid in data['pr'].values[a[0]]:
               self.output.append(grid)

    def update(self):
        self.counter = self.counter + 1
        if(len(self.output) < self.counter + 2):
            self.time = 100.0
            self.end_time = 99.0
    def get_value(self,value):
        if value == "discharge":
            return self.output[self.counter]
        return 0