from ewatercycle_leakybucket.model import LeakyBucket

from ewatercycle.base.forcing import GenericLumpedForcing
import ewatercycle
from pathlib import Path
import numpy as np
import ewatercycle.parameter_sets
from ewatercycle.base.parameter_set import ParameterSet
import posixpath
import matplotlib.pyplot as plt

from ewatercycle.base.forcing import GenericLumpedForcing
from pathlib import Path
from pathlib import PosixPath
import ewatercycle.models
import ewatercycle.forcing
import ewatercycle.analysis

shape = Path(ewatercycle.__file__).parent / "testing/data/Rhine/Rhine.shp"

cmip_dataset = {
                "dataset": "EC-Earth3",
                "project": "CMIP6",
                "grid": "gr",
                "exp": "historical",
                "ensemble": "r6i1p1f1",
            }

forcing = GenericLumpedForcing.generate(
    dataset=cmip_dataset,
    start_time="2000-01-01T00:00:00Z",
    end_time="2000-12-31T00:00:00Z",
    shape=shape.absolute(),
)

# parameter_set = ParameterSet(
#         name='wflow_rhine_sbm_nc',
#         directory=PosixPath('/ewatercycle/parameter-sets/wflow_rhine_sbm_nc'),
#         config=PosixPath('/ewatercycle/parameter-sets/wflow_rhine_sbm_nc/wflow_sbm_NC.ini'),
#         doi='N/A',
#         target_model='wflow',
#         supported_model_versions={'2020.1.2', '2020.1.3', '2020.1.1'},
#         # downloader=GitHubDownloader(
#         #     org='openstreams',
#         #     repo='wflow',
#         #     branch='master',
#         #     subfolder='examples/wflow_rhine_sbm_nc'
#         # )
#     )

# forcing = ewatercycle.forcing.sources["WflowForcing"](
#     directory=str(parameter_set.directory),
#     start_time="1990-01-01T00:00:00Z",
#     end_time="1990-01-31T00:00:00Z",
#     shape=None,
#     # Additional information about the external forcing data needed for the model configuration
#     netcdfinput="inmaps.nc",
#     Precipitation="/P",
#     EvapoTranspiration="/PET",
#     Temperature="/TEMP",
# )

model = LeakyBucket(forcing=forcing)
cfg_file, _ = model.setup(leakiness=1)

model.initialize(cfg_file)

model.bmi.get_component_name()
# print("Input WFLOW \n")
# print(model.input_var_names())
print("Output WFLOW \n")
print(model.output_var_names)

import xarray as xr

discharges = []
while model.time < model.end_time:
    discharges.append(model.get_value_as_xarray("discharge"))
    model.update()

print(discharges)
discharge = xr.concat(discharges, dim="time")
a = discharge.plot()
plt.show()

