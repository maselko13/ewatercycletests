"""
module for getting a model instance

this module provides a class that has methods to get a model instance of
different models.
"""
#pylint:disable=import-error
from datetime import datetime, timezone
from pathlib import Path
import ewatercycle
import ewatercycle.parameter_sets
import ewatercycle.models
import ewatercycle.forcing
import ewatercycle.analysis
from ewatercycle.base.forcing import GenericLumpedForcing, GenericDistributedForcing
from ewatercycle.util import CaseConfigParser
from ewatercycle_leakybucket.model import LeakyBucket
from ewatercycle_wflow.model import Wflow

class RunModelUtil:
    """
    class that has methods to get a model instance of different models.
    """
    @staticmethod
    def run_basic_model(model):
        """
        method to get a basic model instance
        """
        cfg_file, _ = model.setup(
            end_time=model.forcing.end_time,
        )
        model.initialize(cfg_file)
        model.bmi.get_component_name()
        while model.time < model.end_time:
            model.update()

        return model


    @staticmethod
    def refresh_model(model, path):
        """
         Refreshes a model so it is not affected by other tests
         @param model: The model to be refreshed
         @param path: The path where the refreshed models cfg_dir will go to
         @return: The refreshed model and directory which the refreshed model made
         """
        cfg_file, cfg_dir = model.setup(cfg_dir=path)
        model.initialize(cfg_file)
        return model, cfg_dir

    @staticmethod
    def get_leaky_bucket_run_all():
        return dict(model_name='LeakyBucket', model_type='Lumped', output_variable_name='discharge',
                    parameter_set=None, setup_variables={"leakiness": 1}, custom_forcing_name=None,
                    custom_forcing_variables={})

    @staticmethod
    def get_wflow_run_all():
        parameter_set = ewatercycle.parameter_sets.available_parameter_sets(
            target_model="wflow"
        )["wflow_rhine_sbm_nc"]

        return dict(model_name='Wflow', model_type='Distributed', output_variable_name='RiverRunoff',
                    parameter_set=parameter_set, setup_variables={}, custom_forcing_name="WflowForcing",
                    custom_forcing_variables={'directory': str(parameter_set.directory),
                                'netcdfinput': "inmaps.nc",
                                'Precipitation': "/P",
                                'EvapoTranspiration': "/PET",
                                'Temperature': "/TEMP"})


    @staticmethod
    def get_lumped_forcing(parameter_set, shape):
        cmip_dataset = {
            "dataset": "EC-Earth3",
            "project": "CMIP6",
            "grid": "gr",
            "exp": "historical",
            "ensemble": "r6i1p1f1",
        }
        if parameter_set is None:
            forcing = GenericLumpedForcing.generate(
                dataset=cmip_dataset,
                start_time="2001-01-01T00:00:00Z",
                end_time="2001-12-31T00:00:00Z",
                shape=shape.absolute(),
            )
        else:
            cfg = CaseConfigParser()
            cfg.read(parameter_set.config)
            start_time_str = cfg.get("run", "starttime")
            end_time_str = cfg.get("run", "endtime")
            start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).isoformat()
            end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).isoformat()
            forcing = GenericLumpedForcing.generate(
                dataset=cmip_dataset,
                start_time=start_time,
                end_time=end_time,
                shape=shape.absolute(),
            )
        print("Lumped Forcing generated: " + str(forcing))
        return forcing

    @staticmethod
    def get_distributed_forcing(parameter_set, shape):
        cmip_dataset = {
            "dataset": "EC-Earth3",
            "project": "CMIP6",
            "grid": "gr",
            "exp": "historical",
            "ensemble": "r6i1p1f1",
        }
        if parameter_set is None:
            forcing = GenericDistributedForcing.generate(
                dataset=cmip_dataset,
                start_time="2001-01-01T00:00:00Z",
                end_time="2001-12-31T00:00:00Z",
                shape=shape.absolute(),
            )
        else:
            cfg = CaseConfigParser()
            cfg.read(parameter_set.config)
            start_time_str = cfg.get("run", "starttime")
            end_time_str = cfg.get("run", "endtime")
            start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).isoformat()
            end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).isoformat()

            forcing = GenericDistributedForcing.generate(
                dataset=cmip_dataset,
                start_time=start_time,
                end_time=end_time,
                shape=shape.absolute(),
            )
        print("Distributed Forcing generated: " + str(forcing))
        return forcing

    @staticmethod
    def get_custom_forcing(shape, custom_forcing_name, custom_forcing_variables):
        # Time short as customforcing models can take very long to run
        forcing = ewatercycle.forcing.sources[custom_forcing_name](
            start_time="2001-01-01T00:00:00Z",
            end_time="2001-03-31T00:00:00Z",
            shape=shape.absolute(),
            **custom_forcing_variables
        )
        print("Custom Forcing generated: "+str(forcing))
        return forcing


    @staticmethod
    def get_lumped_model(modelname, parameter_set, shape):
        cmip_dataset = {
            "dataset": "EC-Earth3",
            "project": "CMIP6",
            "grid": "gr",
            "exp": "historical",
            "ensemble": "r6i1p1f1",
        }
        if parameter_set is None:
            forcing = GenericLumpedForcing.generate(
                dataset=cmip_dataset,
                start_time="1991-01-01T00:00:00Z",
                end_time="1991-12-31T00:00:00Z",
                shape=shape.absolute(),
            )
            model = ewatercycle.models.sources[modelname](forcing=forcing)
        else:
            cfg = CaseConfigParser()
            cfg.read(parameter_set.config)
            start_time_str = cfg.get("run", "starttime")
            end_time_str = cfg.get("run", "endtime")
            start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).isoformat()
            end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).isoformat()
            forcing = GenericLumpedForcing.generate(
                dataset=cmip_dataset,
                start_time=start_time,
                end_time=end_time,
                shape=shape.absolute(),
            )
            model = ewatercycle.models.sources[modelname](parameter_set=parameter_set, forcing=forcing)
        return model


    @staticmethod
    def get_distributed_model(modelname, parameter_set, shape):
        """
        Method to get a standard forcing for a distributed model
        WORK IN PROGRESS
        """
        cfg = CaseConfigParser()
        cfg.read(parameter_set.config)
        start_time_str = cfg.get("run", "starttime")
        end_time_str = cfg.get("run", "endtime")
        start_time = (datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
                      .replace(tzinfo=timezone.utc).isoformat())
        end_time = (datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")
                    .replace(tzinfo=timezone.utc).isoformat())
        cmip_dataset = {
            "dataset": "EC-Earth3",
            "project": "CMIP6",
            "grid": "gr",
            "exp": "historical",
            "ensemble": "r6i1p1f1",
        }
        forcing = GenericDistributedForcing.generate(
            dataset=cmip_dataset,
            start_time=start_time,
            end_time=end_time,
            shape=shape.absolute(),
        )
        if parameter_set is None:
            model = ewatercycle.models.sources[modelname](forcing=forcing)
        else:
            model = ewatercycle.models.sources[modelname](parameter_set=parameter_set, forcing=forcing)
        return model

    @staticmethod
    def get_wflow_model():
        parameter_set = ewatercycle.parameter_sets.available_parameter_sets(
            target_model="wflow"
        )["wflow_rhine_sbm_nc"]
        forcing = ewatercycle.forcing.sources["WflowForcing"](
            directory=str(parameter_set.directory),
            start_time="1991-01-01T00:00:00Z",
            end_time="1991-12-31T00:00:00Z",
            shape=None,
        )
        model = Wflow(version="2020.1.1", parameter_set=parameter_set, forcing=forcing)
        # cfg_file, cfg_dir = model.setup(
        #     end_time="1992-12-15T00:00:00Z",
        #     # use `cfg_dir="/path/to/output_dir"` to specify the output directory
        # )
        #
        # model.initialize(cfg_file)
        return model

    @staticmethod
    def get_wflow_model_time(start_date, end_date):
        shape = Path(ewatercycle.__file__).parent / "testing/data/Rhine/Rhine.shp"

        parameter_set = ewatercycle.parameter_sets.available_parameter_sets(
            target_model="wflow"
        )["wflow_rhine_sbm_nc"]
        forcing = ewatercycle.forcing.sources["WflowForcing"](
            directory=str(parameter_set.directory),
            start_time=start_date,
            end_time=end_date,
            shape=shape,
        )
        model = Wflow(version="2020.1.1", parameter_set=parameter_set, forcing=forcing)
        cfg_file, _ = model.setup(
            end_time=end_date,
            # use `cfg_dir="/path/to/output_dir"` to specify the output directory
        )
        model.initialize(cfg_file)
        return model

    @staticmethod
    def get_wflow_model_rhine():
        """
        method to get a model instance of the Wflow model with the region being the
        Rhine.
        """
        parameter_set = ewatercycle.parameter_sets.available_parameter_sets(
            target_model="wflow"
        )["wflow_rhine_sbm_nc"]
        forcing = ewatercycle.forcing.sources["WflowForcing"](
            directory=str(parameter_set.directory),
            start_time="1991-01-01T00:00:00Z",
            end_time="1991-12-31T00:00:00Z",
            shape=None,
        )
        model = Wflow(version="2020.1.1", parameter_set=parameter_set, forcing=forcing)
        # cfg_file, cfg_dir = model.setup(
        #     end_time="1992-12-15T00:00:00Z",
        #     # use `cfg_dir="/path/to/output_dir"` to specify the output directory
        # )
        #
        # model.initialize(cfg_file)
        return model

    @staticmethod
    def get_leaky_model(start_date, end_date):
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
            start_time=start_date,
            end_time=end_date,
            shape=shape.absolute(),
        )
        model = LeakyBucket(forcing=forcing)
        cfg_file, _ = model.setup(leakiness=1)
        model.initialize(cfg_file)
        return model


    @staticmethod
    def run_x_array_model(model, outputname):
        # cfg_file, _ = model.setup(leakiness=1)
        # model.initialize(cfg_file)
        discharges = []
        while model.time < model.end_time:
            model.update()
            discharges.append(model.get_value_as_xarray(outputname))


        # print(discharges)
        return discharges

    @staticmethod
    def run_x_array_model_coords(model, outputname, long, lat):
        # cfg_file, _ = model.setup(leakiness=1)
        # model.initialize(cfg_file)
        discharges = []
        while model.time < model.end_time:
            model.update()
            discharges.append(model.get_value_at_coords(outputname, lat=[lat], lon=[long]))

        # print(discharges)
        return discharges


    @staticmethod
    def never_zero(list_coords):
        for a in list_coords:
            # print(a[0][0][0])
            if a[0][0][0] == 0:
                return False
        return True

    @staticmethod
    def sum(coord_list):
        """
        method to sum a list of numbers
        """
        count = 0
        for a in coord_list:
            # print(a[0][0][0])
            count += a[0][0][0]
        # print(count)
        if count == 0:
            return False
        return True



# Temporary Code example
# modelfinal = RunModelUtil.runbasicmodel(RunModelUtil.getwflowmodel())
# modelfinal.get_value_as_xarray("RiverRunoff").plot()
# plt.show()

# discharge = xarray.concat((RunModelUtil.runxarraymodel(RunModelUtil.getleakymodel(),
#                                                       "discharge", 0.15)), dim="time")
# a = discharge.plot()
# plt.show()
