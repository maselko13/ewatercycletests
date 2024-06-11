import Exceptions
import pytest
import ModelsModificationTests

@pytest.mark.validation
def test_correctModelsTxtTest():
    file1 = open('submissionMocks/models.txt', 'r')
    data = file1.readlines()
    ModelsModificationTests.containsNameTest(data)
    ModelsModificationTests.includesRepositoryLinkTest(data)

@pytest.mark.validation
def test_noDataTest():
    file1 = open('submissionMocks/nodatamodels.txt', 'r')
    data = file1.readlines()
    with pytest.raises(Exceptions.NotFoundException):
        ModelsModificationTests.containsNameTest(data)
    with pytest.raises(Exceptions.NotFoundException):
      ModelsModificationTests.includesRepositoryLinkTest(data)

@pytest.mark.validation
def test_badNamingTest():
    file1 = open('submissionMocks/badreponamemodels.txt', 'r')
    data = file1.readlines()
    with pytest.raises(Exceptions.NotFoundException):
        ModelsModificationTests.containsNameTest(data)
    with pytest.raises(Exceptions.WrongFormatException):
      ModelsModificationTests.includesRepositoryLinkTest(data)


