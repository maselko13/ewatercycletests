"""
A module with a test bank with metric tests
"""

from test import Test, TestType
import os

import numpy as np
import ewatercycle.analysis
import ewatercycle.observation.grdc
import matplotlib.pyplot as plt
from test_result import TestResult
from test_bank import TestBank



def get_observation_data_rees(model):
    grdc_station_id = "6335020"
    observations = 0
    # Commented out because of gitlab eqatercycle problems.
    # NEEDS TO BE CODE AGAIN WHEN PIPELINE IS FIXED.
    observations, _ = ewatercycle.observation.grdc.get_grdc_data(
        station_id=grdc_station_id,
        start_time=model.forcing.start_time,
        end_time=model.forcing.end_time,
        column="GRDC",
    )
    return observations

def get_observation_data_lobith(model):
    grdc_station_id = "6435060"
    observations = 0
    # Commented out because of gitlab eqatercycle problems.
    # NEEDS TO BE CODE AGAIN WHEN PIPELINE IS FIXED.
    observations, _ = ewatercycle.observation.grdc.get_grdc_data(
        station_id=grdc_station_id,
        start_time=model.forcing.start_time,
        end_time=model.forcing.end_time,
        column="GRDC",
    )
    return observations

def get_observation_data_schermbeck(model):
    grdc_station_id = "6335080"
    observations = 0
    # Commented out because of gitlab eqatercycle problems.
    # NEEDS TO BE CODE AGAIN WHEN PIPELINE IS FIXED.
    observations, _ = ewatercycle.observation.grdc.get_grdc_data(
        station_id=grdc_station_id,
        start_time=model.forcing.start_time,
        end_time=model.forcing.end_time,
        column="GRDC",
    )
    return observations

def get_output_rees(model, dischargename):
    output = []
    grdc_latitude = 51.756918
    grdc_longitude = 6.395395
    while model.time < model.end_time:
        model.update()
        discharge = model.get_value_at_coords(
            dischargename, lon=[grdc_longitude], lat=[grdc_latitude]
        )[0]
        output.append(discharge)
    return output

def get_output_lobith(model, dischargename):
    output = []
    grdc_latitude = 51.84
    grdc_longitude = 6.11
    while model.time < model.end_time:
        model.update()
        discharge = model.get_value_at_coords(
            dischargename, lon=[grdc_longitude], lat=[grdc_latitude]
        )[0]
        output.append(discharge)
    return output

def get_output_schermbeck(model, dischargename):
    output = []
    grdc_latitude = 51.6739
    grdc_longitude = 6.8511
    while model.time < model.end_time:
        model.update()
        discharge = model.get_value_at_coords(
            dischargename, lon=[grdc_longitude], lat=[grdc_latitude]
        )[0]
        output.append(discharge)
    return output

def calculate_nse(output, observations):
    denom = 0
    omean = (sum(observations["GRDC"]) / len(observations["GRDC"]))
    for value in observations["GRDC"]:
        denom = denom + (pow((value - omean), 2))

    sub = observations["GRDC"].sub(output)
    num = 0
    for subval in sub:
        num += pow(subval, 2)

    if num == 0:
        return 1
    # Observation data is never all the same, so this should nearly never happen
    if denom == 0:
        return -999
    return 1 - (num / denom)

def calculate_kge(output, observations):
    out_mean = sum(output) / len(output)
    obs_mean = sum(observations["GRDC"]) / len(observations["GRDC"])

    f1 = []
    f21 = []
    f22 = []

    for (out, obs) in zip(output, observations["GRDC"]):
        f1.append((out - out_mean) * (obs - obs_mean))
        f21.append((out - out_mean) ** 2)
        f22.append((obs - obs_mean) ** 2)

    r_num = sum(f1)
    r_den = (sum(f21) * sum(f22)) ** 0.5
    r = r_num / r_den

    alpha = np.std(output) / np.std(observations["GRDC"])
    beta = (sum(output) / sum(observations["GRDC"]))
    kge = 1 - np.sqrt((r - 1) ** 2 + (alpha - 1) ** 2 + (beta - 1) ** 2)
    return kge

@TestBank(description=None)
class MetricTests:


    @staticmethod
    @Test(description="Checks and returns the Nash Sutcliffe Efficiency for location Rees germany", critical=False, enabled=True, test_type=TestType.DISTRIBUTED)
    def nash_sutcliffe_efficiency_rees(model, dischargename):
        """
        Test that checks and returns the Nash Sutcliffe Efficiency for location Rees germany for 1991.
        """
        try:

            output = get_output_rees(model, dischargename)

            observations = get_observation_data_rees(model)
            combined_discharge = observations
            combined_discharge["Model name"] = output

            # Use this to plot the graph. Maybe usefull for adding to human readable format could have.
            fig, _ = ewatercycle.analysis.hydrograph(
                 discharge=combined_discharge,
                 reference="GRDC",
            )
            fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", "nash_sutcliffe_efficiency_rees.png"))
            nse = calculate_nse(output, observations)

            if nse < 0.36:
                return TestResult(False, f"Nash-Sutcliffe efficiency is unsatisfactory. Nash Sutcliffe was {nse} , which is lower than 0.36")
            if nse < 0.75:
                return TestResult(True, f"Nash-Sutcliffe efficiency is satisfactory. Nash Sutcliffe was {nse} , which is higher than 0.36")
            return TestResult(True,
                              f"Nash-Sutcliffe efficiency is very good. Nash Sutcliffe was {nse} , which is higher than 0.75")

        except:
            return TestResult(False, "Error occurred, the model did not run correctly")

    @staticmethod
    @Test(description="Checks and returns the Kling Glupta Efficiency for location Rees germany", critical=False, enabled=True, test_type=TestType.DISTRIBUTED)
    def kling_gupta_efficiency_rees(model, dischargename):
        try:

            output = get_output_rees(model, dischargename)

            observations = get_observation_data_rees(model)
            combined_discharge = observations
            combined_discharge["Model name"] = output

            # Use this to plot the graph. Maybe usefull for adding to human readable format could have.
            fig, _ = ewatercycle.analysis.hydrograph(
                 discharge=combined_discharge,
                 reference="GRDC",
            )
            fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", "kling_gupta_efficiency_rees.png"))
            kge = calculate_kge(output, observations)

            if kge < -0.41:
                return TestResult(False,
                                  f"Kling-Gupta efficiency is unsatisfactory. Kling Gupta was {kge} , which is lower than -0.41")
            if kge < 0.75:
                return TestResult(True,
                                  f"Kling-Gupta efficiency is satisfactory. Kling Gupta was {kge} , which is higher than -0.41")
            return TestResult(True,
                              f"Kling-Gupta efficiency is very good. Kling Gupta was {kge} , which is higher than 0.75")
        except:
            return TestResult(False, "Error occurred, the model did not run correctly")

    @staticmethod
    @Test(description="Checks and returns the Nash Sutcliffe Efficiency for location Lobith netherlands", critical=False, enabled=True, test_type=TestType.DISTRIBUTED)
    def nash_sutcliffe_efficiency_lobith(model, dischargename):
        try:

            output = get_output_lobith(model, dischargename)

            observations = get_observation_data_lobith(model)
            combined_discharge = observations
            combined_discharge["Model name"] = output

            # Use this to plot the graph. Maybe usefull for adding to human readable format could have.
            fig, _ = ewatercycle.analysis.hydrograph(
                 discharge=combined_discharge,
                 reference="GRDC",
            )
            fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", "nash_sutcliffe_efficiency_lobith.png"))
            nse = calculate_nse(output, observations)

            if nse < 0.36:
                return TestResult(False, f"Nash-Sutcliffe efficiency is unsatisfactory. Nash Sutcliffe was {nse} , which is lower than 0.36")
            if nse < 0.75:
                return TestResult(True, f"Nash-Sutcliffe efficiency is satisfactory. Nash Sutcliffe was {nse} , which is higher than 0.36")
            return TestResult(True,
                              f"Nash-Sutcliffe efficiency is very good. Nash Sutcliffe was {nse} , which is higher than 0.75")

        except:
            return TestResult(False, "Error occurred, the model did not run correctly")

    @staticmethod
    @Test(description="Checks and returns the Kling Glupta Efficiency for location Lobith netherlands", critical=False, enabled=True, test_type=TestType.DISTRIBUTED)
    def kling_gupta_efficiency_lobith(model, dischargename):
        try:
            output = get_output_lobith(model, dischargename)

            observations = get_observation_data_lobith(model)
            combined_discharge = observations
            combined_discharge["Model name"] = output

            # Use this to plot the graph. Maybe usefull for adding to human readable format could have.
            fig, _ = ewatercycle.analysis.hydrograph(
                 discharge=combined_discharge,
                 reference="GRDC",
            )
            fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", "kling_gupta_efficiency_lobith.png"))
            kge = calculate_kge(output, observations)
            if kge < -0.41:
                return TestResult(False,
                                  f"Kling-Gupta efficiency is unsatisfactory. Kling Gupta was {kge} , which is lower than -0.41")
            if kge < 0.75:
                return TestResult(True,
                                  f"Kling-Gupta efficiency is satisfactory. Kling Gupta was {kge} , which is higher than -0.41")

            return TestResult(True,
                              f"Kling-Gupta efficiency is very good. Kling Gupta was {kge} , which is higher than 0.75")
        except:
            return TestResult(False, "Error occurred, the model did not run correctly")


    @staticmethod
    @Test(description="Checks and returns the Nash Sutcliffe Efficiency for location Schermbeck netherlands", critical=False, enabled=True, test_type=TestType.DISTRIBUTED)
    def nash_sutcliffe_efficiency_schermbeck(model, dischargename):
        try:

            output = get_output_schermbeck(model, dischargename)

            observations = get_observation_data_schermbeck(model)
            combined_discharge = observations
            combined_discharge["Model name"] = output

            # Use this to plot the graph. Maybe usefull for adding to human readable format could have.
            fig, _ = ewatercycle.analysis.hydrograph(
                 discharge=combined_discharge,
                 reference="GRDC",
            )
            fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", "nash_sutcliffe_efficiency_lobith.png"))
            nse = calculate_nse(output, observations)

            if nse < 0.36:
                return TestResult(False, f"Nash-Sutcliffe efficiency is unsatisfactory. Nash Sutcliffe was {nse} , which is lower than 0.36")
            if nse < 0.75:
                return TestResult(True, f"Nash-Sutcliffe efficiency is satisfactory. Nash Sutcliffe was {nse} , which is higher than 0.36")
            return TestResult(True,
                              f"Nash-Sutcliffe efficiency is very good. Nash Sutcliffe was {nse} , which is higher than 0.75")

        except:
            return TestResult(False, "Error occurred, the model did not run correctly")


    @staticmethod
    @Test(description="Checks and returns the Kling Glupta Efficiency for location Schmermbeck germany", critical=False, enabled=True, test_type=TestType.DISTRIBUTED)
    def kling_gupta_efficiency_schermbeck(model, dischargename):
        try:
            output = get_output_schermbeck(model, dischargename)

            observations = get_observation_data_schermbeck(model)
            combined_discharge = observations
            combined_discharge["Model name"] = output

            # Use this to plot the graph. Maybe usefull for adding to human readable format could have.
            fig, _ = ewatercycle.analysis.hydrograph(
                 discharge=combined_discharge,
                 reference="GRDC",
            )
            fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", "kling_gupta_efficiency_lobith.png"))
            kge = calculate_kge(output, observations)
            if kge < -0.41:
                return TestResult(False,
                                  f"Kling-Gupta efficiency is unsatisfactory. Kling Gupta was {kge} , which is lower than -0.41")
            if kge < 0.75:
                return TestResult(True,
                                  f"Kling-Gupta efficiency is satisfactory. Kling Gupta was {kge} , which is higher than -0.41")

            return TestResult(True,
                              f"Kling-Gupta efficiency is very good. Kling Gupta was {kge} , which is higher than 0.75")
        except:
            return TestResult(False, "Error occurred, the model did not run correctly")
