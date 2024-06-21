"""
a module that has a ui for enabling and disabling tests
"""

import os.path
import ttkbootstrap as ttk
import yaml
from plugin_owner_test_ui import TestSelector
from test_suite import TestSuite
import constants as c
from test_report_maker import GenerateReport



class DevRunTests:
    """
    #Run this class to open the UI
    """

    @staticmethod
    def run():
        """
        runs the ui
        """
        ts = TestSuite()
        test_dict = DevRunTests.get_dictionary(ts)
        app = DevRunTests.show_ui(test_dict)
        model_name = 'PCRGlobWB'
        model_type = 'Distributed'
        output_variable_name = 'discharge'
        parameter_set_name = 'pcrglobwb_rhinemeuse_30min'
        setup_variables = {}
        custom_forcing_name = 'PCRGlobWBForcing'
        parameter_set = None
        try:
            for par_set in list(ewatercycle.parameter_sets.available_parameter_sets()
                                        .values()):
                if par_set.name == parameter_set_name:
                    parameter_set = par_set
        except:
            parameter_set = None

        # Don't need shape and start_time/end_time in custom_forcing_variables dictionary!!!
        if parameter_set is None:
            custom_forcing_variables = None
        else:
            # Wflow
            # custom_forcing_variables = {'directory': str(parameter_set.directory),
            #                             'netcdfinput': "inmaps.nc",
            #                             'Precipitation': "/P",
            #                             'EvapoTranspiration': "/PET",
            #                             'Temperature': "/TEMP"}
            # PCRGLOB
            custom_forcing_variables = {'directory': (parameter_set.directory / 'forcing'),
                                        'precipitationNC': 'precipitation_2001to2010.nc',
                                        'temperatureNC': 'temperature_2001to2010.nc'}
        if app.success:
            DevRunTests.enable_disable(ts.tests.values(), app.selected_tests)
            results = ts.run_all(model_name, model_type, output_variable_name,
                                     parameter_set, setup_variables,
                                     custom_forcing_name, custom_forcing_variables)

            if results[c.SUITE_PASSED_ATTRIBUTE]:
                print("tests passed!")
            else:
                print("tests failed!")
            DevRunTests.generate_test_report(results)
        else:
            print("No tests run due to cancellation or termination")

    @staticmethod
    def get_dictionary(testsuite):
        """
        gets a dictionary of tests
        """
        test_dict = {}
        for tb in testsuite.testBanks.values():
            test_dict[tb.name] = tb.tests

        return test_dict

    @staticmethod
    def show_ui(test_dict):
        """
        shows the ui on screen
        """

        # root = ttk.Window(themename="cyborg")
        root = ttk.Window(themename="darkly")
        app = TestSelector(root, test_dict)
        root.mainloop()
        return app


    @staticmethod
    def enable_disable(tests, selected_tests):
        """
        enables or disables the tests
        """
        for test in tests:
            if test.name in selected_tests:
                test.enabled = True
            else:
                test.enabled = False

    @staticmethod
    def generate_test_report(results):
        """
        generates the test report
        """
        print("Generating Yaml")
        GenerateReport.generate_report_yaml(yaml.dump(results), os.path.join(os.getcwd(), 'output'))
        print("Generating MarkDown")
        GenerateReport.generate_mark_down(results, "output.md", "MockModel v1")

DevRunTests.run()
