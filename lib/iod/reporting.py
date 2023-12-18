import importlib
import os
import csv
from datetime import datetime

module = importlib.import_module("lib.global_var")


# Getting the %USERPROFILE% environment variable
user_profile = os.environ.get('USERPROFILE')
new_folder_path = os.path.join(user_profile, 'Documents', 'Ready2tesT', 'IOD')
report_folder = os.path.join(new_folder_path, 'report')
# Checking if the folder exists, if not, create it along with the subfolder
if not os.path.exists(new_folder_path):
    os.makedirs(new_folder_path)
    print(f"Created folder: {new_folder_path}")

if not os.path.exists(report_folder):
    os.makedirs(report_folder)
    print(f"Created subfolder: {report_folder}")




def averagingVariable(variable):
    """this methods takes all the value from a fifo and return average

    Returns:
        _type_: _description_
    """    
    if not hasattr(module, variable):
        print(f"{module} has no attribute {variable}")
        return
    
    l_variable = getattr(module, variable)
    
    if l_variable.empty():
        print("Empty")
        return 0  # Return 0 or None if you prefer, for an empty queue

    total = 0
    count = 0

    while not l_variable.empty():
        item = l_variable.get()
        total += item
        count += 1

    print(total)
    print(count)
    average = total / count
    return average



def createReport(info):
    print("**** GENERATING REPORT ****")
    print(info)

    averageCurrent = averagingVariable("962.CSM_BAT_CURRENT")
    averageVoltage = averagingVariable("g_q_Voltage")

    # Get the current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Define the CSV file name
    csv_file_name = 'IOD_' + info + 'report.csv'
    
    # Open the file in append mode ('a') so that it creates the file if it doesn't exist
    with open(os.path.join(report_folder, csv_file_name), mode='a', newline='') as file:
        writer = csv.writer(file)

        # Write the header if the file is new/empty
        if file.tell() == 0:
            writer.writerow(["Date and Time", "Info", "Average Current", "Average Voltage"])

        # Write the data
        writer.writerow([current_datetime, info, averageCurrent, averageVoltage])

    print(f"Report saved to {csv_file_name}")
