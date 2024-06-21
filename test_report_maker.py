"""
Has a class that generates test reports based on the results of the tests
"""

import os.path
import markdown2 #pylint:disable=E0401

class GenerateReport:
    """"
    Generate a test report YAML file, if no filename is given or
    Param report is the string to be made into a test report
    Param directory is the location where the report will be deposited
    Param filename is the name of the yaml file, if not specified it will be testReport
    """

    @staticmethod
    def generate_report_yaml(report: str, directory: str, filename: str = ""):
        """
        generates a markdown file from the test results.
        @param report: the test results
        @param directory: the directory where the report will be deposited
        @param filename: the name of the report file
        """
        if filename.strip() == "":
            filename = "testReport"
        file = open(os.path.join(directory, filename + ".yaml"), "w")
        file.write("---\n")
        file.write(report)
        file.close()
        return os.path.join(directory, filename + ".yaml")

    @staticmethod
    def generate_mark_down(results, directory, file_name, modelname):
        """
        generates a markdown file from the test results.
        @param results: test results
        @param directory: the directory where the report will be deposited
        @param file_name: name of the markdown file
        @param modelname: name of the model
        """
        md_content = ""
        fpassed = False
        for i in results:
            # print(results.get(i))
            if isinstance(results.get(i), bool):
                fpassed = results.get(i)
            else:
                name = results.get(i).get('name').replace("_", "\_")
                description = results.get(i).get('description').replace("_", "\_")
                critical = results.get(i).get('critical')
                enabled = results.get(i).get('enabled')
                passed = results.get(i).get('passed')
                reason = results.get(i).get('reason').replace("_", "\_")

                if passed:
                    color = "green"
                else:
                    if critical:
                        color = "red"
                    else:
                        color = "orange"

                md_content += f"## <span style='color:{color}'>{name}</span>\n"
                md_content += f"**Description:** {description}\n\n"
                md_content += f"**Critical:** {critical}\n\n"
                md_content += f"**Enabled:** {enabled}\n\n"
                md_content += f"**Passed:** {passed}\n\n"
                md_content += f"**Reason:** {reason}\n\n"
                if os.path.isfile(os.path.join(directory, results.get(i).get('name')+".png")):
                    md_content += "<img src="+ name + ".png width=350 height=300>\n"
                md_content += "---\n\n"

        if fpassed:
            md_content = ("## <span style='color:green'>"
                          "TestSuite Passed (All Critical Tests Passed)"
                          "</span>\n") + md_content
        else:
            md_content = ("## <span style='color:red'>"
                          "TestSuite Did Not Pass! (A Critical Test Has Failed)"
                          "</span>\n") + md_content

        md_content = f"# Test Results: {modelname}\n\n" + md_content
        html_content = markdown2.markdown(md_content)
        # print(passed)
        with open(os.path.join(directory, file_name + ".md"), 'w') as f:
            f.write(html_content)

        return os.path.join(directory, file_name + ".md")
