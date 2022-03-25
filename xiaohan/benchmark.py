import os
import re
import numpy as np
import pandas as pd
import linecache
from natsort import natsorted
from openpyxl import load_workbook


def process_file(file_path, regex, counter, successful):
    """
    Compare the regex with positive and negative examples, return the number of matching positive examples,
    total number of positive exaples, the number of matching negative examples, total number of negative examples.

    :param file_path: the filepath of the test file.
    :param regex: the regex used to compare with examples
    :param counter: list of counters: [# of successful solution regex, # unsuccessfully compiled regex, 
            successfully repaired regex in java but failed commpiled]
    :param successful: boolean if the solution regex is successfully fixed.

    :return: nums=[pos_match, pos_total, neg_match, neg_total] and a string to output
    """
    # print(file_path)
    pos = False
    neg = False
    pos_match, pos_total = 0, 0
    neg_match, neg_total = 0, 0
    use_sol_regex = False

    with open(file_path, 'r') as infile:
        # use original regex if regex is None or successful is False
        if regex == "None" or successful == False:
            regex = infile.readline().rstrip("\n")
            pattern = re.compile(regex)
        else:
            try:
                # successful ==True solution regex is possible to fail to compile.
                pattern = re.compile(regex)
                use_sol_regex = True
            except:
                # solution regex failed to compile, use original regex from test file.
                print(f"Fail to compile: {sheet_name}, {file_path}, {regex}")
                regex = infile.readline().rstrip("\n")
                pattern = re.compile(regex)
                counter[0] += 1
        for line in infile:
            line = line.rstrip("\n")
            if line == "+++":
                pos = True
                continue
            if line == "---":
                pos = False
                neg = True
                continue
            if pos:
                # if fullmatch does not return None
                if pattern.fullmatch(line):
                    pos_match += 1
                elif use_sol_regex:
                    print(f"Did not match: {sheet_name}, {file_path}, {regex}")
                pos_total += 1
            if neg:
                if not pattern.fullmatch(line):
                    neg_match += 1
                elif use_sol_regex:
                    print(f"Did not match: {sheet_name}, {file_path}, {regex}")
                neg_total += 1
    pos_ratio = pos_match / pos_total
    neg_ratio = neg_match / neg_total
    nums = np.asarray([pos_match, pos_total, neg_match, neg_total])
    if use_sol_regex:
        string = f"Pos: {pos_match}/{pos_total}: {pos_ratio:.2f}, \t Neg: {neg_match}/{neg_total}: {neg_ratio:.2f}. Solution RegEx.\n"
    else:
        string = f"Pos: {pos_match}/{pos_total}: {pos_ratio:.2f}, \t Neg: {neg_match}/{neg_total}: {neg_ratio:.2f}. Originial RegEx.\n"
    
    # increase # of pass regex check only when all examples are matched.
    if use_sol_regex and pos_match == pos_total and neg_match == neg_total:
        counter[1] += 1
    # number of solution regex did not pass the check
    elif use_sol_regex and ( pos_match != pos_total or neg_match != neg_total ):
        counter[2] += 1
    return nums, string


def process_sheet(sheet, sheet_name, counter, time_list):
    """
    Process a sheet of a dataset, save matching information to a text file.

    :param sheet: the excel sheet to be processed
    :param sheet_name: name of the excel sheet (experiment name)
    :param counter: counter list [# failed compiled regex, # pass solution regex check, # failed solution regex check, 
                    # successful==True]
    :param time_list: [total_time, total_time_entries, SAT_time, SAT_time_entries]

    :return total_nums: the 4 nums of the whole sheet. [pos_match, pos_total, neg_match, neg_total]
    """

    folder_path = os.path.join(results_path, sheet_name, sheet.iloc[0,0])
    outfile = open(folder_path + ".txt", "w")
    total_nums = np.zeros(4)

    for index, row in sheet.iterrows():
        file_name = row["filename"]
        regex = row["Solution regex"]
        successful = row["Successful"]
        if successful == True:
            counter[3] += 1
        file_path = os.path.join(tests_path, row["Dataset"], file_name)

        if row["Total time(ms)"] != "None":
            time_list[0] += int(row["Total time(ms)"])
            time_list[1] += 1
        if row["SAT time(ms)"] != "None":
            time_list[2] += int(row["SAT time(ms)"])
            time_list[3] += 1

        # process the test file with solution regex
        nums, string = process_file(file_path, regex, counter, successful)
        total_nums += nums
        outfile.write(file_name + ":   " + string)

    # calculate and add summary
    pos_ratio = total_nums[0] / total_nums[1]
    neg_ratio = total_nums[2] / total_nums[3]
    summary = f"Total Pos: {total_nums[0]}/{total_nums[1]}={pos_ratio:.2f}, \
                Total Neg: {total_nums[2]}/{total_nums[3]}={neg_ratio:.2f}\n"
    outfile.write(summary)
    outfile.close()
    return total_nums


results_path = "results"
tests_path = "tests"
# read all sheets from the excel to a dictionary of dataframes: sheet_name=None
df_rebele = pd.read_excel("results/Rebele.xlsx", sheet_name=None)
df_regexlib = pd.read_excel("results/RegExLib.xlsx", sheet_name=None)
df_autotutor = pd.read_excel("results/AutoTutor.xlsx", sheet_name=None)
writer = pd.ExcelWriter("results/summary.xlsx", engine='xlsxwriter')

summary_headers = ["Rebele pos match", "Rebele pos total", "Rebele neg match", "Rebele neg total",
           "RegExLib pos match", "RegExLib pos total", "RegExLib neg match", "RegExLib neg total",
           "AutoTutor pos match", "AutoTutor pos total", "AutoTutor neg match", "AutoTutor neg total",
           "total pos match", "total pos", "total neg match", "total neg",
           "Rebele pos ratio", "Rebele neg ratio", "RegExLib pos ratio", "RegExLib neg ratio", "AutoTutor pos ratio",
           "AutoTutor neg ratio",  "total pos ratio", "total neg ratio",  
           "failed compiled regex", "pass solution regex check", "fail solution regex check", "successful==True",
           "total regex", "pass rate", "F1 score", "F score", "average total time(ms)", "average SAT time(ms)"]

# loop through the each experiment 
sheet_names = list(df_rebele.keys())

# summary table
table = []

regex_headers = ["Dataset", "filename", "Origin regex"] + sheet_names
total_time_headers = ["Dataset", "filename", "Origin regex"] + sheet_names
sheet_rebele = df_rebele[sheet_names[0]]
sheet_regexlib = df_regexlib[sheet_names[0]]
sheet_autotutor = df_autotutor[sheet_names[0]]

# initialize first 3 columns as "Dataset", "filename", "Origin regex".
regex_table = np.concatenate((sheet_rebele.iloc[:, :3].values, sheet_regexlib.iloc[:, :3].values, \
                              sheet_autotutor.iloc[:, :3].values))
total_time_table = np.concatenate((sheet_rebele.iloc[:, :3].values, sheet_regexlib.iloc[:, :3].values, \
                                   sheet_autotutor.iloc[:, :3].values))

for sheet_name in sheet_names:
    sheet_rebele = df_rebele[sheet_name]
    sheet_regexlib = df_regexlib[sheet_name]
    sheet_autotutor = df_autotutor[sheet_name]

    # [# failed compiled regex, # pass solution regex check, # failed solution regex check,
    #  # successful==True]
    counter = [0, 0, 0, 0]
    
    # [total_time, total_time_entries, SAT_time, SAT_time_entries]
    time_list = [0, 0, 0, 0]
    
    # [pos_match, pos_total, neg_match, neg_total]
    rebele_nums = process_sheet(sheet_rebele, sheet_name, counter, time_list)
    regexlib_nums = process_sheet(sheet_regexlib, sheet_name, counter, time_list)
    autotutor_nums = process_sheet(sheet_autotutor, sheet_name, counter, time_list)
    sheet_nums = rebele_nums + regexlib_nums + autotutor_nums

    # calculate matching ratio of each dataset and total
    rebele_pos_ratio = rebele_nums[0] / rebele_nums[1]
    rebele_neg_ratio = rebele_nums[2] / rebele_nums[3]
    regexlib_pos_ratio = regexlib_nums[0] / regexlib_nums[1]
    regexlib_neg_ratio = regexlib_nums[2] / regexlib_nums[3]
    autotutor_pos_ratio = autotutor_nums[0] / autotutor_nums[1]
    autotutor_neg_ratio = autotutor_nums[2] / autotutor_nums[3]
    total_pos_ratio = sheet_nums[0] / sheet_nums[1]
    total_neg_ratio = sheet_nums[2] / sheet_nums[3]

    # calculate repair rate of regex
    total_regex = sheet_rebele.shape[0] + sheet_regexlib.shape[0] + sheet_autotutor.shape[0]
    repair_rate = counter[1] / total_regex

    # calculate F1 score and F score
    TP = sheet_nums[0]
    TN = sheet_nums[2]
    FP = sheet_nums[3] - sheet_nums[2]
    FN = sheet_nums[1] - sheet_nums[0]
    recall = TP / (TP + FN)
    precision = TP / (TP + FP)
    F1_score = 2 * precision * recall / ( precision + recall )
    F_score = (TP - FN + TN - FP) / (sheet_nums[1] + sheet_nums[3])

    # average total time and average SAT time
    avg_total_time = time_list[0] / time_list[1]
    avg_SAT_time = time_list[2] / time_list[3]

    # add new row of summary to summary table
    new_row = np.concatenate((rebele_nums, regexlib_nums, autotutor_nums, sheet_nums)).tolist()
    new_row += [rebele_pos_ratio, rebele_neg_ratio, regexlib_pos_ratio, regexlib_neg_ratio, autotutor_pos_ratio, 
               autotutor_neg_ratio, total_pos_ratio, total_neg_ratio, counter[0], counter[1], counter[2], counter[3],
               total_regex, repair_rate, F1_score, F_score, avg_total_time, avg_SAT_time]
    table.append(new_row)

    # append new column of regex and total time to corresponding table
    regex_column = np.concatenate((sheet_rebele["Solution regex"].values, sheet_regexlib["Solution regex"].values,
                                 sheet_autotutor["Solution regex"].values))
    time_column = np.concatenate((sheet_rebele["Total time(ms)"].values, sheet_regexlib["Total time(ms)"].values,
                                 sheet_autotutor["Total time(ms)"].values))
    regex_table = np.append(regex_table, regex_column[:, None], axis=1)
    total_time_table = np.append(total_time_table, time_column[:, None], axis=1)

    print(f"not match {counter[2]} + match {counter[1]} + fail compiled {counter[0]}= \
        {counter[2] + counter[1] + counter[0]}, {counter[3]}")

# Transpose and save summary table to excel sheet
df = pd.DataFrame(table, columns = summary_headers)
df = df.T
df.columns = sheet_names
df.to_excel(writer, sheet_name="summary", index=True)
# set column header width to the length of header
worksheet = writer.sheets["summary"]
worksheet.set_column(0, 0, len(summary_headers[-8])) 
for i in range(len(sheet_names)):
    worksheet.set_column(i+1, i+1, len(sheet_names[i])+3) 

# save regex summary table to excel sheet
df = pd.DataFrame(regex_table, columns = regex_headers)
df.to_excel(writer, sheet_name="RegEx", index=False)
worksheet = writer.sheets["RegEx"]
for i in range(len(regex_headers)):
    worksheet.set_column(i, i, len(regex_headers[i])+3)

# save total time table to excel sheet
df = pd.DataFrame(total_time_table, columns = total_time_headers)
df.to_excel(writer, sheet_name="Total time", index=False)
worksheet = writer.sheets["Total time"]
for i in range(len(total_time_headers)):
    worksheet.set_column(i, i, len(total_time_headers[i])+3)

writer.save()
