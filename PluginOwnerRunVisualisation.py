from PluginOwnerVisualisationUI import ModelRunnerPopup
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from run_model_util import RunModelUtil
import xarray as xr
import matplotlib.pyplot as plt
import mocks


class PluginOwnerRunVisualisation:

    @staticmethod
    def run():
        root = ttk.Window(themename="darkly")
        app = ModelRunnerPopup(root)
        root.mainloop()
        if app.flag:
            model_type = app.model_var.get()
            variable_name = app.variable_entry.get()
            start_date = app.start_date_entry.get() + "T00:00:00Z"
            end_date = app.end_date_entry.get() + "T00:00:00Z"
            if model_type == "Distributed":
                graph_type = app.graph_type_var.get()
                if graph_type == "LineGraph":
                    longitude = float(app.longitude_entry.get())
                    latitude = float(app.latitude_entry.get())
            root.destroy()
            print(start_date+" - "+end_date)
            # Temporary Models for testing purposes
            # model = RunModelUtil.getleakymodel(start_date, end_date)
            model = RunModelUtil.get_wflow_model_time(start_date, end_date)
            if variable_name not in model.output_var_names:
                print("Variable name does not exist: "+variable_name)
                return
            if len(model.get_value_as_xarray(variable_name)[0]) > 1:
                if model_type == "Lumped":
                    print("Model looks like distributed but Lumped was selected, possible error.")
            else:
                if model_type == "Distributed":
                    print("Model looks like lumped but Distributed was selected, possible error.")


            if model_type == "Lumped":
                outputs = RunModelUtil.run_x_array_model(model, variable_name)
                result = xr.concat(outputs, dim="time")
                result.plot()
                plt.show()
            else:
                if graph_type == "HeatMap":
                    RunModelUtil.runbasicmodel(model)
                    a = model.get_value_as_xarray(variable_name)
                    print(a)
                    a.plot()
                    plt.show()
                else:
                    outputs = RunModelUtil.run_x_array_model_coords(model, variable_name, longitude, latitude)
                    # result = xr.concat(outputs, dim="time")
                    print(outputs)
                    plt.plot(outputs)
                    plt.show()
        else:
            print("Cancelled")


# model = Mocks.BasicModelMock()
# model = RunModelUtil.getleakymodel()
PluginOwnerRunVisualisation.run()