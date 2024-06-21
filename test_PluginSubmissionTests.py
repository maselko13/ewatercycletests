import PluginSubmissionTests
import pytest
import yaml
import Exceptions

@pytest.mark.validation
def test_correctFileTest():
    data = yaml.safe_load(open('submissionMocks/submission.yml'))
    variables = ["discharge"]
    PluginSubmissionTests.includesRepositoryLinkTest(data)
    PluginSubmissionTests.containsVariablesTest(data)
    PluginSubmissionTests.containsForcingParametersTest(data)
    PluginSubmissionTests.definesCriticalVarsTest(data, variables)

@pytest.mark.validation
def test_emptySubmissionTest():
    data = yaml.safe_load(open('submissionMocks/emptysubmission.yml'))
    variables = ["discharge"]
    with pytest.raises(Exceptions.NotFoundException):
        PluginSubmissionTests.includesRepositoryLinkTest(data)
    with pytest.raises(Exceptions.NotFoundException):
        PluginSubmissionTests.containsVariablesTest(data)
    with pytest.raises(Exceptions.NotFoundException):
        PluginSubmissionTests.containsForcingParametersTest(data)
    with pytest.raises(Exceptions.NotFoundException):
        PluginSubmissionTests.definesCriticalVarsTest(data, variables)

@pytest.mark.validation
def test_badRepoNameSubmissionTest():
    data = yaml.safe_load(open('submissionMocks/badreponamesubmission.yml'))
    variables = ["discharge"]
    with pytest.raises(Exceptions.WrongFormatException):
        PluginSubmissionTests.includesRepositoryLinkTest(data)
    PluginSubmissionTests.containsVariablesTest(data)
    PluginSubmissionTests.containsForcingParametersTest(data)
    PluginSubmissionTests.definesCriticalVarsTest(data, variables)