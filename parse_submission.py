"""
A module that parses a yaml file containing model data and returns it as a dictionary
"""

import ewatercycle


class ParseSubmission:


    """
    Main method for parsing the submission file
    @param data: The data of the yaml file
    """
    @staticmethod
    def get_parameters_from_submission(data):
        """
        Main method for parsing the submission file
        """

        parameter_set = ParseSubmission.get_parameter_set(data)

        setup_variables = ParseSubmission.get_setup_variables(data)

        custom_forcing_variables = \
            (ParseSubmission.get_custom_forcing_variables(data, parameter_set))

        result = {'model_name': data["model_name"],
                  'model_type': data["model_type"],
                  'output_variable_name': data["output_variable_name"],
                  'parameter_set': parameter_set,
                  'setup_variables': setup_variables,
                  'custom_forcing_name': data["custom_forcing_name"],
                  'custom_forcing_variables': custom_forcing_variables}

        return result

    @staticmethod
    def get_parameter_set(data):
        """
        Gets the parameter set that is used by a model
        (or None if no parameter set is used)
        """
        parameter_set_name = data["parameter_set_name"]
        parameter_set = None
        for par_set in list(ewatercycle.parameter_sets.available_parameter_sets()
                                    .values()):
            if par_set.name == parameter_set_name:
                parameter_set = par_set
        return parameter_set

    @staticmethod
    def get_setup_variables(data):
        """
        Parses and returns the setup variables needed for a model
        """

        setup_variables = {}
        if data["setup_variables"] is not None:
            for setupvar in data["setup_variables"]:
                key, = setupvar
                value, = setupvar.values()
                setup_variables[key] = value

        return setup_variables

    @staticmethod
    def get_custom_forcing_variables(data, parameter_set):
        """
        Parses and returns the forcing variables needed for a model's forcing data
        """

        custom_forcing_variables = {}
        if data["custom_forcing_variables"] is not None:
            for setupvar in data["custom_forcing_variables"]:
                key, = setupvar
                value, = setupvar.values()
                if (key == 'directory') and (parameter_set is not None):
                    custom_forcing_variables[key] = str(parameter_set.directory / value)
                else:
                    custom_forcing_variables[key] = value

        return custom_forcing_variables
