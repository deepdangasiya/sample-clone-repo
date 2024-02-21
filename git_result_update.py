import git
import os
import openpyxl
import re


def git_readme_update(readme_data):
    repo = git.Repo(os.getcwd())
    branch = repo.active_branch.name
    content = ("### Test Results: ###\n\n"
               "| Test-ID | Test Case Name | Test Case Result |\n"
               "| :------:|:--------------:|:----------------:|\n")
    for ele in readme_data:
        content += f"|{ele['test_id']}|{ele['test_name']}|{ele['result']}|\n"
    with open("README.md", "w") as f:
        f.write(content)
    print(branch)
    # repo.index.add("README.md")
    # repo.index.commit("Update README.md with tests results")
    # origin = repo.remote(name="origin")
    # origin.push(branch)


def extract_excel_data():
    excel_file = "report_all.xlsx"
    wb = openpyxl.load_workbook(excel_file)
    ws = wb.active
    # header = [cell.value for row in
    #           ws.iter_rows(min_row=1, max_row=1, max_col=9) for cell in row]
    data_list = [[cell.value for cell in row] for row in
                 ws.iter_rows(min_row=2)]
    dict_list = []
    reg = r'(\w+)\[(\w+-\d+)]'
    for ele in data_list:
        test_name, test_id = re.search(reg, ele[1]).groups()
        temp_dict = {"test_id": test_id, "test_name": test_name,
                     "result": ele[3]}
        dict_list.append(temp_dict)
    return dict_list


if __name__ == "__main__":
    data = extract_excel_data()
    git_readme_update(data)
