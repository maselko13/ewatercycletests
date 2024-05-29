import ewatercycle
from ewatercycle_wflow.model import Wflow
from ewatercycle_pcrglobwb.model import PCRGlobWB
from ewatercycle.base.parameter_set import ParameterSet
import posixpath
import matplotlib.pyplot as plt
from ewatercycle.base.forcing import GenericLumpedForcing
from pathlib import Path
from pathlib import PosixPath
import numpy as np
import ewatercycle.parameter_sets
import ewatercycle.models
import ewatercycle.forcing
import ewatercycle.analysis

print(ewatercycle.models.sources)

shape = Path(ewatercycle.__file__).parent / "testing/data/Rhine/Rhine.shp"

# print(ewatercycle.parameter_sets.available_parameter_sets)
#
print(ewatercycle.parameter_sets.available_parameter_sets(
    target_model="pcrglobwb"
)["pcrglobwb_rhinemeuse_30min"])

print(ewatercycle.forcing.sources)

parameter_set = ewatercycle.parameter_sets.available_parameter_sets(
    target_model="pcrglobwb"
)["pcrglobwb_rhinemeuse_30min"]

# parameter_set = ewatercycle.parameter_sets.available_parameter_sets(
#     target_model="wflow"
# )["wflow_rhine_sbm_nc"]

forcing = ewatercycle.forcing.sources["PCRGlobWBForcing"](
    directory=str(parameter_set.directory),
    start_time="2001-01-01T00:00:00Z",
    end_time="2001-12-31T00:00:00Z",
    shape=shape,
    # Additional information about the external forcing data needed for the model configuration
    # netcdfinput="inmaps.nc",
    # Precipitation="/blabla",
    # EvapoTranspiration="/PET",
    # Temperature="/TEMP",
)



# model = Wflow(version="2020.1.1", parameter_set=parameter_set, forcing=forcing)
model = PCRGlobWB(
    version="setters", parameter_set=parameter_set
)

cfg_file, cfg_dir = model.setup(
    # end_time="2001-12-15T00:00:00Z",
    # use `cfg_dir="/path/to/output_dir"` to specify the output directory
)

model.initialize(cfg_file)

print(model.bmi.get_component_name())
print("Output PCRGLOB")
print(model.output_var_names)

grdc_latitude = 51.756918
grdc_longitude = 6.395395

output = []
while model.time < model.end_time:
    model.update()
    # print(model.time)

    discharge = model.get_value_at_coords(
        "discharge", lon=[grdc_longitude], lat=[grdc_latitude]
    )[0]

    output.append(discharge)

    # Here you could do whatever you like, e.g. update soil moisture values before doing the next timestep.

    # print(model.time_as_isostr)
    # print(discharge)

import xarray as xr

# discharge = xr.concat(output, dim="time")
# a = output.plot()
model.get_value_as_xarray("discharge").plot()
plt.show()

model.finalize()

import ewatercycle.observation.grdc

grdc_station_id = "6335020"

observations, metadata = ewatercycle.observation.grdc.get_grdc_data(
    station_id=grdc_station_id,
    start_time="1991-01-01T00:00:00Z",  # or: model_instance.start_time_as_isostr
    end_time="1995-12-31T00:00:00Z",
    column="GRDC",
)

import ewatercycle.analysis

combined_discharge = observations
combined_discharge["pcrglob"] = output

ewatercycle.analysis.hydrograph(
    discharge=combined_discharge,
    reference="GRDC",
)

plt.show()
