#
# Script to convert an Eagle BOM to a CSV
# Version 1.0 March 2021 - Johan Korten
#

# importing panda library

#!/usr/bin/python

try:
    import pandas as pd
except ModuleNotFoundError:
    print("Please install pandas (python3 -m pip install pandas)...")
    exit

try:
    import re
except ModuleNotFoundError:
    print("Please install (python3 -m pip install re)...")
    exit

try:
    import sys
except ModuleNotFoundError:
    print("Please install sys (python3 -m pip install pandas)...")
    exit

ignore_lines = ["Partlist", "Exported", "EAGLE", "Assembly"]

# Converts bom file to tabbed file:
# 1. remove lines that are either empty or start with items from  ignore_lines
# 2. save to .tab file

bom_header_index = ""

line_counter = 0
added_lines = 0
skipped_lines = 0
empty_lines = 0

def loadBOM(text_file_tab, text_file_bom):
    tabbedFile = open(text_file_tab, 'w')

    # Using readlines()
    bomFile = open(text_file_bom, 'r')
    bom_lines = bomFile.readlines()
    return (bom_lines, tabbedFile, bomFile)


def processBOM(bom_lines, tabbedFile):
    line_counter = 0
    skipped_lines = 0
    empty_lines = 0
    added_lines = 0

    for bom_line in bom_lines:
        line_counter += 1
        skipLine = False

        if (len(bom_line.strip()) > 0):
            for ignore_item in ignore_lines:
                if bom_line.startswith(ignore_item):
                    # skips line that starts with item of ignore_lines
                    #print("Skipped line " + str(line_counter) + " as it is contains: " + str(ignore_item))
                    skipped_lines += 1
                    skipLine = True
        else:
            # Strips empty lines
            skipLine = True
            #print("Skipped line " + str(line_counter) + " as it is empty...")

        if (skipLine == False):
            added_lines += 1
            if (added_lines == 1):
                bom_header_index = re.split(r'\s+', bom_line)
            bom_line = bom_line.replace(" - ", "-")
            tabbedFile.writelines(bom_line)

    return bom_header_index, skipped_lines, empty_lines, added_lines

def writeTabbedFile(text_file_tab, tabbedFile, bomFile):
    tabbedFile.close()

    # read these lines
    tabbedFile = open(text_file_tab, 'r')
    tabbed_lines = bomFile.readlines()
    tabbedFile.close()
    return tabbed_lines

def writeCSV(text_file_tab, text_file_csv):
    # readinag given csv file
    # and creating dataframe
    csv_helper_pandas = pd.read_csv(text_file_tab,  delim_whitespace=True)
    csv_helper_pandas.to_csv(text_file_csv, index = None)

def rereadCSV(text_file_csv, bom_header_index):
    csv_helper_pandas = pd.read_csv(text_file_csv, header = 1)

    bom_header_index.remove('')
    csv_helper_pandas.columns = bom_header_index

    return csv_helper_pandas

def writeFinalCSV(csv_helper_pandas, text_file_csv):
    # for summing up items:
    grouped = csv_helper_pandas.groupby(['Value', 'Device', 'Package'])['Part'].count().reset_index()
    grouped = grouped.sort_values(by='Part')

    # storing this dataframe in a csv file
    grouped.to_csv(text_file_csv, index = None)


def processBOMandExport(_filename):

    text_file_noext = _filename
    text_file_bom = text_file_noext + ".bom" # original file
    text_file_tab = text_file_noext + ".tab" # only tab separated info
    text_file_csv = text_file_noext + ".csv" # target file
    text_file_sum = text_file_noext + ".sum.csv" # summary file

    bom_lines, tabbedFile, bomFile = loadBOM(text_file_tab, text_file_bom)
    bom_header_index, skipped_lines, empty_lines, added_lines = processBOM(bom_lines, tabbedFile)

    print(" Results are written to " + str(text_file_tab) + " now...")
    tabbed_lines = writeTabbedFile(text_file_tab, tabbedFile, bomFile)

    writeCSV(text_file_tab, text_file_csv)
    print("\n Overview of BOM file contents:")
    print("===============================================================================")
    print(" Bill of Materials : " + str(added_lines) + " parts added.")
    print(" Ignored: " + str(skipped_lines) + " lines.")
    print(" Skipped: " + str(empty_lines) + " empty lines.")

    csv_helper_pandas = rereadCSV(text_file_csv, bom_header_index)
    writeFinalCSV(csv_helper_pandas, text_file_sum)

    print("===============================================================================")
    print("\n Summed items written in following file: \"" + str(text_file_sum) + "\"\n")


if (len(sys.argv) >= 1):
    if (sys.argv[1].endswith(".bom")):
        _filename = sys.argv[1].rsplit(".", 1)
        #print(_filename)
        print()
        print("===============================================================================")
        print(" Tool to convert Eagle BOM file to .csv files (normal csv and summed csv) V1.0")
        print(" V1.0, March 2021, Johan Korten")
        print("===============================================================================\n")
        print(" About to process BOM file: \"" + str(_filename[0]) + ".bom\"")
        print()
        processBOMandExport(_filename[0])
