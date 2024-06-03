import ewatercycle
from ewatercycle_wflow.model import Wflow
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
ewatercycle.parameter_sets.download_example_parameter_sets()


# cmip_dataset = {
#     "dataset": "EC-Earth3",
#     "project": "CMIP6",
#     "grid": "gr",
#     "exp": "historical",
#     "ensemble": "r6i1p1f1",
# }

# forcing = GenericLumpedForcing.generate(
#     dataset=cmip_dataset,
#     start_time="2000-01-01T00:00:00Z",
#     end_time="2000-12-31T00:00:00Z",
#     shape=shape.absolute(),
# )



# tmp_path = Path("")
# directory = tmp_path / "wflow_testcase"
# config = directory / "wflow_sbm_nc.ini"

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


parameter_set = ewatercycle.parameter_sets.available_parameter_sets(
    target_model="wflow"
)["wflow_rhine_sbm_nc"]


# forcing = ewatercycle.forcing.sources["WflowForcing"](
#     directory=str(parameter_set.directory),
#     start_time="1991-01-01T00:00:00Z",
#     end_time="1992-12-31T00:00:00Z",
#     shape=None,
#     # Additional information about the external forcing data needed for the model configuration
#     netcdfinput="inmaps.nc",
#     Precipitation="/P",
#     EvapoTranspiration="/PET",
#     Temperature="/TEMP",
# )

forcing = ewatercycle.forcing.sources["WflowForcing"](
    directory=str(parameter_set.directory),
    start_time="1991-01-01T00:00:00Z",
    end_time="1992-12-31T00:00:00Z",
    shape=None,
    # Additional information about the external forcing data needed for the model configuration
    netcdfinput="inmaps.nc",
    Precipitation="/P",
    EvapoTranspiration="/PET",
    Temperature="/TEMP",
)


#model = Wflow(version="2020.1.1", parameter_set=parameter_set, forcing=forcing)
model = Wflow(version="2020.1.3", parameter_set=parameter_set, forcing=forcing)

cfg_file, cfg_dir = model.setup(
    end_time="1992-12-15T00:00:00Z",
    # use `cfg_dir="/path/to/output_dir"` to specify the output directory
)

model.initialize(cfg_file)

print(model.bmi.get_component_name())
print("Output WFLOW")
print(model.output_var_names)

grdc_latitude = 51.756918
grdc_longitude = 6.395395

output = []
while model.time < model.end_time:
    model.update()
    print(model.time)

    discharge = model.get_value_at_coords(
        "RiverRunoff", lon=[grdc_longitude], lat=[grdc_latitude]
    )[0]
    output.append(discharge)

    # Here you could do whatever you like, e.g. update soil moisture values before doing the next timestep.

    print(model.time_as_isostr)
    print(discharge)

model.get_value_as_xarray("RiverRunoff").plot()
plt.show()
