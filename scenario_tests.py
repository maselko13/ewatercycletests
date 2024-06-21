"""Module containing the test bank that includes scenario tests."""

import math

from test import Test, TestType
from test_result import TestResult
from test_bank import TestBank


@TestBank(description=None)
class ScenarioTests:
    """Test Bank that contains all scenario tests.

    Scenario tests test the model based on specific inputs, called scenarios
    It checks whether its discharge output is sensible from
     a hydrological modelling perspective based on those scenarios
    """

    @staticmethod
    @Test(description="Tests if the model outputs any discharge"
                 " on an input with 0 precipitation", critical=False, enabled=True, test_type=TestType.LUMPED)
    def zero_precipitation_lumped_test(model, outputvar):
        """Test if a lumped model outputs any discharge
         on an input with 0 precipitation.

       Args:
           model: the hydrological model to run this scenario test on.
            must be set up with the proper scenario input.
       """
        while model.time < model.end_time:
            model.update()
            discharge = model.get_value(outputvar)
            for i in discharge:
                if i != 0:
                    return TestResult(False,"the model output discharge"
                                       " despite 0 precipitation, is this intentional?")
        return TestResult(True)

    @staticmethod
    @Test(description="Tests if the model outputs any discharge on"
                      " an input with 0 precipitation", critical=False, enabled=True, test_type=TestType.DISTRIBUTED)
    def zero_precipitation_distributed_test(model, outputvar):
        """Test if a distributed model outputs any discharge
        on an input with 0 precipitation.

       Args:
           model: the hydrological model to run this scenario test on.
            must be set up with the proper scenario input.
       """
        while model.time < model.end_time:
            model.update()
            discharge = model.get_value(outputvar)
            for i in discharge:
                if i != 0:
                    return TestResult(False,"the model output discharge"
                 " despite 0 precipitation, is this intentional?")
        return TestResult(True)

    @staticmethod
    @Test(description="Tests if the model outputs"
        " constant discharge on an input"
         " with constant precipitation", critical=False, enabled=True, test_type=TestType.LUMPED)
    def permanent_precipitation_lumped_test(model, outputvar):
        """Test if a lumped model outputs constant discharge
         on an input with constant precipitation.

        Args:
            model: the hydrological model to run this scenario test on.
             must be set up with the proper scenario input.
        """
        while model.time < model.end_time:
            model.update()
            discharge = model.get_value(outputvar)
            for i in discharge:
                if i == 0:
                    return TestResult(False, "the model output"
        " no discharge despite constant rain, is this intentional?")
        return TestResult(True)

    @staticmethod
    @Test(description="Tests if the model "
    " constant discharge on an input"
      " with constant precipitation", critical=False, enabled=True, test_type=TestType.DISTRIBUTED)
    def permanent_precipitation_distributed_test(model, outputvar):
        """Test if a distributed model outputs constant discharge
         on an input with constant precipitation.

        Args:
            model: the hydrological model to run this scenario test on.
             must be set up with the proper scenario input.
        """
        while model.time < model.end_time:
            model.update()
            discharge = model.get_value(outputvar)
            for i in discharge:
                if i == 0:
                    return TestResult(False, "the model output no discharge"
         " despite constant rain, is this intentional?")
        return TestResult(True)

    @staticmethod
    @Test(description="Tests if the model"
            " outputs increasing discharge on an input"
            " with increasing precipitation", critical=False, enabled=True, test_type=TestType.BOTH)
    def strict_increase_test(model, outputvar):
        """Test if a lumped model outputs increasing discharge
         on an input with increasing precipitation.

        Args:
            model: the hydrological model to run this scenario test on.
             must be set up with the proper scenario input.
        """
        temp = 0
        while model.time < model.end_time:
            model.update()
            discharge = model.get_value(outputvar)
            for i in discharge:
                if i < temp:
                    return TestResult(False,
    'the model does not output increasing dicharge on increasing precipitation,'
    ' is this intentional?')
                else:
                    temp = i
        return TestResult(True)

    @staticmethod
    @Test(description="Tests if the model"
        " outputs decreasing discharge on an input"
       " with decreasing precipitation", critical=False, enabled=True, test_type=TestType.BOTH)
    def strict_decrease_test(model, outputvar):
        """Test if a lumped model outputs decreasing discharge
        on an input with decreasing precipitation.

        Args:
            model: the hydrological model to run this scenario test on.
             must be set up with the proper scenario input.
        """
        temp = float('inf')
        while model.time < model.end_time:
            model.update()
            discharge = model.get_value(outputvar)
            for i in discharge:
                if i > temp:
                    return TestResult(False,
  'the model does not output increasing dicharge on increasing precipitation,'
  ' is this intentional?')
                else:
                    temp = i
        return TestResult(True)

    @staticmethod
    @Test(description="Tests if the model"
         " outputs correct discharge when there's periodical,"
        " high precipitation", critical=False, enabled=True, test_type=TestType.LUMPED)
    def proper_mid_spike_handling_lumped_test(model, outputvar):
        """Test if a lumped model outputs correct discharge
         when there's periodical, high precipitation.

        Args:
            model: the hydrological model to run this scenario test on.
             must be set up with the proper scenario input.
        """
        temp = []
        while model.time < model.end_time:
            model.update()
            discharge = model.get_value(outputvar)
            for i in discharge:
                temp.append(i)
        if (temp.index(max(temp)) < len(temp)/2
                or temp.index(max(temp)) > len(temp)* 0.6):
            return TestResult(False,
    "The model handles spikes in the input precipitation in an odd way,"
    " is that intentional?")
        else:
            return TestResult(True)

    @staticmethod
    @Test(description="Tests if the model"
         " outputs correct discharge when there's periodical,"
       " high precipitation", critical=False, enabled=True, test_type=TestType.DISTRIBUTED)
    def proper_mid_spike_handling_distributed_test(model, outputvar):
        """Test if a distributed odel outputs correct discharge
         when there's periodical, high precipitation.

        Args:
            model: the hydrological model to run this scenario test on.
             must be set up with the proper scenario input.
        """
        temp = []
        while model.time < model.end_time:
            model.update()
            discharge = model.get_value(outputvar)
            for i in discharge:
                temp.append(i)
        if (temp.index(max(temp)) < len(temp) * 0.45
                or temp.index(max(temp)) > len(temp)* 0.55):
            return TestResult(False,"The model handles spikes"
 " in the input precipitation in an odd way, is that intentional?")
        else:
            return TestResult(True)

    @staticmethod
    @Test(description="Tests if the model"
         " outputs correct discharge when there's periodical,"
         " high precipitation", critical=False, enabled=True, test_type=TestType.LUMPED)
    def proper_start_spike_handling_lumped_test(model, outputvar):
        """Test if a lumped model outputs correct discharge
         when there's periodical, high precipitation.

        Args:
            model: the hydrological model to run this scenario test on.
             must be set up with the proper scenario input.
        """
        temp = []
        while model.time < model.end_time:
            model.update()
            discharge = model.get_value(outputvar)
            for i in discharge:
                temp.append(i)
        if (temp.index(max(temp)) < (len(temp)/10) - 1
                or temp.index(max(temp)) > len(temp)* 0.2):
            return TestResult(False,"The model handles spikes"
 " in the input precipitation in an odd way,"
                         " is that intentional?")
        else:
            return TestResult(True)

    @staticmethod
    @Test(description="Tests if the model"
        " outputs correct discharge when there's periodical,"
      " high precipitation", critical=False, enabled=True, test_type=TestType.DISTRIBUTED)
    def proper_start_spike_handling_distributed_test(model, outputvar):
        """Test if a distributed model outputs correct discharge
         when there's periodical, high precipitation.

        Args:
            model: the hydrological model to run this scenario test on.
             must be set up with the proper scenario input.
        """
        temp = []
        while model.time < model.end_time:
            model.update()
            discharge = model.get_value(outputvar)
            for i in discharge:
                temp.append(i)
        if (temp.index(max(temp)) < len(temp) * 0.05
                or temp.index(max(temp)) > len(temp) * 0.15):
            return TestResult(False,
                              "The model handles spikes"
 " in the input precipitation in an odd way, is that intentional?")
        else:
            return TestResult(True)

    @staticmethod
    @Test(description="Tests if the model"
            " outputs correct discharge when there's periodical,"
      " high precipitation", critical=False, enabled=True, test_type=TestType.LUMPED)
    def proper_end_spike_handling_lumped_test(model, outputvar):
        """Test if a lumped model outputs correct discharge
         when there's periodical, high precipitation.

        Args:
            model: the hydrological model to run this scenario test on.
             must be set up with the proper scenario input.
        """
        temp = []
        while model.time < model.end_time:
            model.update()
            discharge = model.get_value(outputvar)
            for i in discharge:
                temp.append(i)
        if (temp.index(max(temp)) < (len(temp) * 0.8)-1
                or temp.index(max(temp)) > len(temp)* 0.9):
            return TestResult(False,"The model handles spikes"
    " in the input precipitation in an odd way, is that intentional?")
        else:
            return TestResult(True)

    @staticmethod
    @Test(description="Tests if the model"
            " outputs correct discharge when there's periodical,"
        " high precipitation", critical=False, enabled=True, test_type=TestType.DISTRIBUTED)
    def proper_end_spike_handling_distributed_test(model, outputvar):
        """Test if a distributed model outputs correct discharge
         when there's periodical, high precipitation.

        Args:
            model: the hydrological model to run this scenario test on.
             must be set up with the proper scenario input.
        """
        temp = []
        while model.time < model.end_time:
            model.update()
            discharge = model.get_value(outputvar)
            for i in discharge:
                temp.append(i)
        if (temp.index(max(temp)) < len(temp) * 0.75
                or temp.index(max(temp)) > len(temp)* 0.85):
            return TestResult(False,"The model handles spikes"
    " in the input precipitation in an odd way, is that intentional?")
        else:
            return TestResult(True)

    @staticmethod
    @Test(description="Tests if the model"
 " outputs correct discharge when precipitation only"
" occurs in the first half of the input period", critical=False, enabled=True, test_type=TestType.LUMPED)
    def first_half_precip_lumped_test(model, outputvar):
        """Test if a lumped model outputs correct discharge
             when precipitation only occurs in the first half of the input period.

            Args:
                model: the hydrological model to run this scenario test on.
                 must be set up with the proper scenario input.
            """
        temp = []
        while model.time < model.end_time:
            model.update()
            discharge = model.get_value(outputvar)
            for i in discharge:
                temp.append(i)
        for i in range(math.floor(len(temp) / 2)):
            if temp[i] == 0:
                return TestResult(False, "the model output"
      " no discharge despite precipitation, is this intentional?")
        for i in range(math.ceil(len(temp) / 2), len(temp)):
            if temp[i] != 0:
                return TestResult(False,"the model output"
        " discharge despite 0 precipitation, is this intentional?")
        return TestResult(True)

    @staticmethod
    @Test(description="Tests if the model outputs"
        " correct discharge when precipitation only occurs"
   " in the first half of the input period", critical=False, enabled=True, test_type=TestType.DISTRIBUTED)
    def first_half_precip_distributed_test(model, outputvar):
        """Test if a distributed model outputs correct discharge
             when precipitation only occurs in the first half of the input period.

            Args:
                model: the hydrological model to run this scenario test on.
                 must be set up with the proper scenario input.
            """
        temp = []
        while model.time < model.end_time:
            model.update()
            discharge = model.get_value(outputvar)
            for i in discharge:
                temp.append(i)
        for i in range(math.floor(len(temp) / 2)):
            if temp[i] == 0:
                if i < len(temp) * 0.45:
                    return TestResult(False, "the model output"
    " no discharge despite precipitation, is this intentional?")
            else:
                break
        for i in range(math.ceil(len(temp) / 2), len(temp)):
            if temp[i] != 0:
                if i > len(temp) * 0.55:
                    return TestResult(False,"the model output"
         " discharge despite 0 precipitation, is this intentional?")
        return TestResult(True)

    @staticmethod
    @Test(description="Tests if the model"
     " outputs correct discharge when precipitation only occurs"
     " in the second half of the input period", critical=False, enabled=True, test_type=TestType.LUMPED)
    def second_half_precip_lumped_test(model, outputvar):
        """Test if a lumped model outputs correct discharge
             when precipitation only occurs in the second half of the input period.

            Args:
                model: the hydrological model to run this scenario test on.
                 must be set up with the proper scenario input.
            """
        temp = []
        while model.time < model.end_time:
            model.update()
            discharge = model.get_value(outputvar)
            for i in discharge:
                temp.append(i)
        for i in range(math.floor(len(temp) / 2)):
            if temp[i] != 0:
                return TestResult(False,"the model output"
         " discharge despite 0 precipitation, is this intentional?")
        for i in range(math.ceil(len(temp) / 2), len(temp)):
            if temp[i] == 0:
                return TestResult(False, "the model output"
       " no discharge despite precipitation, is this intentional?")
        return TestResult(True)

    @staticmethod
    @Test(description="Tests if the model"
  " outputs correct discharge when precipitation only occurs "
     "in the second half of the input period", critical=False, enabled=True, test_type=TestType.DISTRIBUTED)
    def second_half_precip_distributed_test(model, outputvar):
        """Test if a distributed model outputs correct discharge
             when precipitation only occurs in the second half of the input period.

            Args:
                model: the hydrological model to run this scenario test on.
                 must be set up with the proper scenario input.
            """
        temp = []
        while model.time < model.end_time:
            model.update()
            discharge = model.get_value(outputvar)
            for i in discharge:
                temp.append(i)
        for i in range(math.floor(len(temp) / 2)):
            if temp[i] != 0:
                if i < len(temp) * 0.45:
                    return TestResult(False, "the model output"
                " no discharge despite precipitation, is this intentional?")
            else:
                break
        for i in range(math.ceil(len(temp) / 2), len(temp)):
            if temp[i] == 0:
                if i > len(temp) * 0.55:
                    return TestResult(False,"the model output"
     " discharge despite 0 precipitation, is this intentional?")
        return TestResult(True)

    @staticmethod
    @Test(description="Tests if the model"
     " outputs any discharge prior"
    " to the start of the calculations", critical=False, enabled=True, test_type=TestType.LUMPED)
    def pre_existing_discharge_lumped_test(model, outputvar):
        """Test if a lumped model outputs any discharge
         prior to the start of the calculations.

        Args:
            model: the hydrological model to run this scenario test on
        """
        discharge = model.get_value(outputvar)
        for i in discharge:
            if i != 0:
                return TestResult(False,
                "the model has pre-existing discharge, is this intentional?")
        return TestResult(True)

    @staticmethod
    @Test(description="Tests if the model"
            " outputs any discharge prior"
     " to the start of the calculations", critical=False, enabled=True, test_type=TestType.DISTRIBUTED)
    def pre_existing_discharge_distributed_test(model, outputvar):
        """Test if a distributed model outputs any discharge
         prior to the start of the calculations.

        Args:
            model: the hydrological model to run this scenario test on
        """
        discharge = model.get_value(outputvar)
        for i in discharge:
            if i != 0:
                return TestResult(False,
                "the model has pre-existing discharge, is this intentional?")
        return TestResult(True)
