# from rich import print

import ewatercycle.models
import matplotlib.pyplot as plt
print(ewatercycle.models.sources)

import ewatercycle.forcing
import ewatercycle.models
import ewatercycle.parameter_sets

parameter_set = ewatercycle.parameter_sets.available_parameter_sets(
    target_model="wflow"
)["wflow_rhine_sbm_nc"]
forcing = ewatercycle.forcing.sources["WflowForcing"](
    directory=str(parameter_set.directory),
    start_time="1991-01-01T00:00:00Z",
    end_time="1995-12-31T00:00:00Z",
    shape=None,
    # Additional information about the external forcing data needed for the model configuration
    netcdfinput="inmaps.nc",
    Precipitation="/P",
    EvapoTranspiration="/PET",
    Temperature="/TEMP",
)

model_instance = ewatercycle.models.Wflow(
    version="2020.1.3", parameter_set=parameter_set, forcing=forcing
)

model_instance.parameters

cfg_file, cfg_dir = model_instance.setup(
    end_time="1995-12-31T00:00:00Z",
    # use `cfg_dir="/path/to/output_dir"` to specify the output directory
)

print(cfg_file)

model_instance.initialize(cfg_file)

grdc_latitude = 51.756918
grdc_longitude = 6.395395

output = []
while model_instance.time < model_instance.end_time:
    model_instance.update()
    discharge = model_instance.get_value_at_coords(
        "RiverRunoff", lon=[grdc_longitude], lat=[grdc_latitude]
    )[0]
    output.append(discharge)
    # print(
    #     model_instance.time_as_isostr,
    #     end="\r",
    #     flush=True,
    # )

model_instance.get_value_as_xarray("RiverRunoff").plot()

model_instance.get_value_at_coords("RiverRunoff", lat=[50.0], lon=[8.05])

model_instance.output_var_names

model_instance.bmi.get_component_name()

model_instance.finalize()

import ewatercycle.observation.grdc

grdc_station_id = "6335020"

observations, metadata = ewatercycle.observation.grdc.get_grdc_data(
    station_id=grdc_station_id,
    start_time="1991-01-01T00:00:00Z",  # or: model_instance.start_time_as_isostr
    end_time="1995-12-31T00:00:00Z",
    column="GRDC",
)

print(observations.head())

print(metadata)

import ewatercycle.analysis

combined_discharge = observations
combined_discharge["wflow"] = output

ewatercycle.analysis.hydrograph(
    discharge=combined_discharge,
    reference="GRDC",
)

plt.show()
