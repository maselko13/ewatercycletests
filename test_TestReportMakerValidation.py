import pytest
from TestReportMaker import GenerateReport
import os
import pathlib

@pytest.mark.validation
def test_generateReportYaml():
    location = GenerateReport.generateReportYaml("I wrote this", os.getcwd(), "validation")
    file = open(location, 'r')
    file_content = file.read()
    assert file_content == "---\nI wrote this"
    os.remove(location)

@pytest.mark.validation
def test_generateReportYamlEmptyFilename():
    location = GenerateReport.generateReportYaml("I wrote this", os.getcwd())
    file = open(location, 'r')
    file_content = file.read()
    assert file_content == "---\nI wrote this"
    os.remove(location)

@pytest.mark.validation
def test_generateReportYamlWhitespaceFilename(request):
    location = GenerateReport.generateReportYaml("I wrote this", os.getcwd(), "     ")
    assert os.path.exists(location)
    file = open(location, 'r')
    file_content = file.read()
    assert file_content == "---\nI wrote this"
    os.remove(location)
