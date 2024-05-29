from pathlib import Path
import xarray
import ewatercycle
from ewatercycle.base.forcing import GenericLumpedForcing
from ewatercycle_leakybucket.model import LeakyBucket
from ewatercycle_wflow.model import Wflow
import matplotlib.pyplot as plt
import ewatercycle.parameter_sets
import ewatercycle.models
import ewatercycle.forcing
import ewatercycle.analysis

class RunModelUtil:
    @staticmethod
    def runbasicmodel(model):
        cfg_file, cfg_dir = model.setup(
            end_time=model.forcing.end_time,
        )
        model.initialize(cfg_file)
        model.bmi.get_component_name()
        while model.time < model.end_time:
            model.update()

        return model

    @staticmethod
    def getwflowmodel():
        parameter_set = ewatercycle.parameter_sets.available_parameter_sets(
            target_model="wflow"
        )["wflow_rhine_sbm_nc"]
        forcing = ewatercycle.forcing.sources["WflowForcing"](
            directory=str(parameter_set.directory),
            start_time="1991-01-01T00:00:00Z",
            end_time="1992-12-31T00:00:00Z",
            shape=None,
        )
        model = Wflow(version="2020.1.1", parameter_set=parameter_set, forcing=forcing)
        return model

    @staticmethod
    def getleakymodel():
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
        return LeakyBucket(forcing=forcing)


    @staticmethod
    def runxarraymodel(model, outputvaridx, setupparam):
        if setupparam != None:
            cfg_file, _ = model.setup(leakiness=setupparam)
        else:
            print("NO setupparam, using 1")
            cfg_file, _ = model.setup(leakiness=1)
        model.initialize(cfg_file)
        discharges = []
        while model.time < model.end_time:
            model.update()
            discharges.append(model.get_value_as_xarray(model.output_var_names[outputvaridx]))


        # print(discharges)
        return discharges

    @staticmethod
    def neverzero(list):
        for a in list:
            # print(a[0][0][0])
            if a[0][0][0] == 0:
                return False
        return True

    @staticmethod
    def sum(list):
        count = 0
        for a in list:
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

# discharge = xarray.concat((RunModelUtil.runxarraymodel(RunModelUtil.getleakymodel(), "discharge", 0.15)), dim="time")
# a = discharge.plot()
# plt.show()

