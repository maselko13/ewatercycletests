# basic model mock
# for now only contains classes that are tested by our framework, TODO: add mocking for remaining methods
class BasicModelMock:
        notdischarge = 3.0
        def __init__(self) -> None:
            self.time = 0.0

        def initialize(self,cfg):
            # hardcoded for now
            if cfg != 'cfg.json':
                 raise Exception('nuh-uh')

        def finalize(self):
            placeholder = 1

        def update(self):
            self.time = self.time + self.get_time_step()

        def get_current_time(self):
            return self.time

        def get_end_time(self):
            return 100.0

        def get_grid_type(self,number):
            if number == 0:
                return 'scalar'
            if number == 1:
                return 'rectilinear'
            else:
                raise Exception('nope')

        def get_grid_rank(self,number):
            if number == 0:
                return 0
            if number == 1:
                return 2
            else:
                raise Exception('nope')

        def get_grid_shape(self,number):
            return [number,number]

        def get_grid_size(self,number):
            return number*number

        def get_grid_x(self,number):
            return number

        def get_grid_y(self,number):
            return number
        def get_output_var_names(self):
            return ['name1', 'name2']

        def get_start_time(self):
            return 0.0

        def get_time_step(self):
            return 1.0

        def get_time_units(self):
            return "days"