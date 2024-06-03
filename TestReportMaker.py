import os.path
import markdown2

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

    def generateMarkDown(results, file_name, modelname):
        md_content = ""
        fpassed = False
        for i in results:
            # print(results.get(i))
            if (results.get(i) == False or results.get(i) == True):
                fpassed = results.get(i)
            else:
                name = results.get(i).get('name')
                description = results.get(i).get('description')
                critical = results.get(i).get('critical')
                enabled = results.get(i).get('enabled')
                passed = results.get(i).get('passed')
                reason = results.get(i).get('reason')

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
                md_content += "---\n\n"

        if (fpassed):
            md_content = f"## <span style='color:green'>TestSuite Passed (All Critical Tests Passed)</span>\n" + md_content
        else:
            md_content = f"## <span style='color:red'>TestSuite Did Not Pass! (A Critical Test Has Failed)</span>\n" + md_content

        md_content = f"# Test Results: {modelname}\n\n" + md_content
        html_content = markdown2.markdown(md_content)
        # print(passed)
        with open(file_name, 'w') as f:
            f.write(html_content)
