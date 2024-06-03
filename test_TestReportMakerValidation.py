import pytest
from TestReportMaker import GenerateReport
import os
import markdown2
import pathlib

@pytest.fixture
def results_test():
    return {
        "Test 1":
        {
            "name": "Test 1",
            "description": "This is the first test.",
            "critical": True,
            "enabled": True,
            "passed": False,
            "reason": "Some failure reason."
        },
        "Test 2":
        {
            "name": "Test 2",
            "description": "This is the second test.",
            "critical": False,
            "enabled": True,
            "passed": True,
            "reason": "Passed successfully."
        },
        "Test 3":
        {
                "name": "Test 3",
                "description": "This is the third test.",
                "critical": False,
                "enabled": True,
                "passed": False,
                "reason": "Non critical failed."
        }
    }

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

@pytest.mark.validation
def test_file_exists(results_test):
    report_file = "randomname.md"
    GenerateReport.generateMarkDown(results_test, report_file, "Random model v1")
    assert os.path.exists(report_file)
    os.remove(report_file)

@pytest.mark.validation
def test_colors(results_test):
    report_file = "randomname.md"
    GenerateReport.generateMarkDown(results_test, report_file, "Random model v1")
    with open(report_file, 'r') as f:
        content = f.read()

    # Check for the critical test color (red)
    assert "<span style='color:red'>Test 1</span>" in content

    # Check for the non-critical test color (blue)
    assert "<span style='color:green'>Test 2</span>" in content

    assert "<span style='color:orange'>Test 3</span>" in content
    os.remove(report_file)




