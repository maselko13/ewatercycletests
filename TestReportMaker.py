import os.path


class GenerateReport:

    """"
    Generate a test report YAML file, if no filename is given or
    Param report is the string to be made into a test report
    Param directory is the location where the report will be deposited
    Param filename is the name of the yaml file, if not specified it will be testReport
    """
    def generateReportYaml(report: str, directory: str, filename: str = ""):
        if (filename.strip() == ""):
            filename = "testReport"
        file = open(os.path.join(directory, filename + ".yaml"), "w")
        file.write("---\n")
        file.write(report)
        file.close()
        return os.path.join(directory, filename + ".yaml")
