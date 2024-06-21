"""Module containing the tests of the YAML-format submission file."""
import yaml
import Exceptions

def contains_model_name_test(data):
    """Test if the submission file contains the name of the model.

    Args:
        data: the submission.yml file.
    """
    try:
        data.get("model_name")
    except Exception as exception:
        raise Exceptions.NotFoundException("The model name was not provided")\
            from exception
    if not isinstance(data.get("model_name"),str):
        raise Exceptions.WrongFormatException("The model name is"
                                              " of the wrong format!")


def contains_model_type_test(data):
    """Test if the submission file contains the type of the model.

    Args:
        data: the submission.yml file.
    """
    try:
        data.get("model_type")
    except Exception as exception:
        raise Exceptions.NotFoundException("The model type was not provided")\
            from exception
    if not isinstance(data.get("model_type"),str):
        raise Exceptions.WrongFormatException("The model type is "
                                              "of the wrong format!")
    if (data.get("model_type") != 'Lumped'
            and data.get("model_type") != 'Distributed'):
        raise Exceptions.WrongFormatException("The model type is "
              "of the wrong format (it is neither Distributed nor Lumped!)")

def contains_output_var_name_test(data):
    """Test if the submission file contains the name of the output variable of the model.

    Args:
        data: the submission.yml file.
    """
    try:
        data.get("output_variable_name")
    except Exception as exception:
        raise Exceptions.NotFoundException("The output variable name was not provided")\
            from exception

    if not isinstance(data.get("output_variable_name"),str):
        raise Exceptions.WrongFormatException("The output variable name is "
                                              "of the wrong format!")

def contains_parameter_set_name_test(data):
    """Test if the submission file contains the name of the parameter set of the model (can be None or Null).

    Args:
        data: the submission.yml file.
    """
    try:
        print(data.get("parameter_set_name"))
    except Exception as exception:
        raise Exceptions.NotFoundException("No parameter set was provided"
     "(add parameter_set_name and set it to None if not applicable to the model)")\
            from exception


def contains_setup_variables_test(data):
    """Test if the submission file contains the setup variables of the model (can be None or Null).

    Args:
        data: the submission.yml file.
    """
    try:
        data.get("setup_variables")
    except Exception as exception:
        raise Exceptions.NotFoundException("No setup variables were provided"
     "(add setup_variables and set it to None if not applicable to the model)")\
            from exception


def contains_custom_forcing_name_test(data):
    """Test if the submission file contains the name of the custom forcing for the model (can be None or Null).

    Args:
        data: the submission.yml file.
    """
    try:
        data.get("custom_forcing_name")
    except Exception as exception:
        raise Exceptions.NotFoundException("No custom forcing name was provided"
     "(add custom_forcing_name and set it to None if not applicable to the model)")\
            from exception


def contains_custom_forcing_variables_test(data):
    """Test if the submission file contains the variables for the custom forcing of the model (can be None or Null).

    Args:
        data: the submission.yml file.
    """
    try:
        data.get("custom_forcing_variables")
    except Exception as exception:
        raise Exceptions.NotFoundException("No custom forcing variables were provided"
 "(add custom_forcing_variables and set it to None if not applicable to the model)") \
            from exception

# extract file
with open('submissionMocks/submission.yml') as file:
    file = yaml.safe_load(file)
# test file
contains_model_name_test(file)
contains_model_type_test(file)
contains_output_var_name_test(file)
contains_parameter_set_name_test(file)
contains_setup_variables_test(file)
contains_custom_forcing_name_test(file)
contains_custom_forcing_variables_test(file)
