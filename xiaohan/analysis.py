import sys
import re
import os
import glob 
import numpy as np
import pandas as pd
import linecache
from natsort import natsorted


def generate_sheet(files, writer, foldername):
    """
    This function extracts information from the input files and generate an excel sheet.

    :param files: a list of test file results.
    :param writer: excel writer
    :param foldername: the configuration of the test file results, used for sheet_name.
    :param headers: the headers of each sheet which are the modes.
    """

    table = []

    for i in range(len(files)):
        with open(files[i], 'r') as file:
            contents = file.read()
            # get dataset directory name and filename
            dirname, filename = files[i].split("/")[-2:]
            # get original regex from 4th line
            origin_regex = linecache.getline(files[i], 4).strip(" \n")

            # get solution and check successful, check fail reason
            content = contents.partition("#sol#")[2]
            solution, _, check  = content.partition("#sol#")
            successful = "True"
            fail_reason = ""
            # check if solution is empty
            if not solution:
                solution = "None"
                successful = "False"
                # for mode 2 syntax error result files
                if "exception while checking" in contents:
                    fail_reason = "Syntax error"
                else:
                    fail_reason = "TimeOut/OutOfMemory"
            # check if exception occurred
            elif "exception while checking" in check:
                successful = "False"
                fail_reason = "exception while checking"
            # some example did not match with the solution regex
            elif "pattern cfail" in check or "auto cfail" in check:
                successful = "False"
                fail_reason = "example check failed"
            # has solution, but timeout or out of memory when creating Automaton from solution regex
            elif "before exit" not in contents:
                successful = "False"
                fail_reason = "didn't exit successfully (OutOfMemory/timeout)"

            # get total time
            content = contents.partition('#c#')[2]
            total_time = content.partition('#c#')[0]
            if not total_time:
                total_time = "None"
            
            # get SAT time
            content = contents.partition("#s#")[2]
            SAT_time = content.partition("#s#")[0]
            if not SAT_time:
                SAT_time = "None"
            
            # get depth
            content = contents.partition("#dep#")[2]
            depth = content.partition("#dep#")[0]
            if not depth:
                depth = "None"
        
        new_row = [dirname, filename, origin_regex, successful, solution, total_time, SAT_time, depth, fail_reason]
        table.append(new_row)

    # save the table to excel with sheet_name same as the foldername
    df = pd.DataFrame(table, columns = headers)
    df.to_excel(writer, sheet_name=foldername, index=False)
    # set column header width to the length of header
    worksheet = writer.sheets[foldername]
    for i in range(len(headers)):
        worksheet.set_column(i, i, len(headers[i])) 


foldernames = ["mode1", "mode1_TO20", 
               "mode1base_TO20", "mode1max_TO20", "mode1basemax_TO20", \
               "mode2", "mode2_TO20", "mode2base_TO20", "mode2max_TO20", "mode2basemax_TO20"]
headers = ["Dataset", "filename", "Origin regex", "Successful", "Solution regex", \
           "Total time(ms)", "SAT time(ms)", "depth", "Failed reason"]

rebele_writer = pd.ExcelWriter("results/Rebele.xlsx", engine='xlsxwriter')
regexlib_writer = pd.ExcelWriter("results/RegExLib.xlsx", engine='xlsxwriter')
autotutor_writer = pd.ExcelWriter("results/AutoTutor.xlsx", engine='xlsxwriter')

for j in range(len(foldernames)):
    # glob test result files to a list
    rebele = glob.glob(f"results/{foldernames[j]}/allRebele/*.txt", recursive=True)
    regexlib = glob.glob(f"results/{foldernames[j]}/benchmark_explicit/*.txt", recursive=True)
    autotutor = glob.glob(f"results/{foldernames[j]}/clean_AutoTutor/*.txt", recursive=True)

    # sort test files
    rebele = natsorted(rebele)
    regexlib = natsorted(regexlib)
    autotutor = natsorted(autotutor)

    # generate excel sheet for each configurations
    generate_sheet(rebele, rebele_writer, foldernames[j])
    generate_sheet(regexlib, regexlib_writer, foldernames[j])
    generate_sheet(autotutor, autotutor_writer, foldernames[j])

rebele_writer.save()
regexlib_writer.save()
autotutor_writer.save()