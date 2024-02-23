import os
from pathlib import Path

# Get the user's home directory (equivalent to %USERPROFILE% in Windows)
user_profile = Path.home()
# Define the new folder name
new_folder_name = 'TemplateRecognitionAPI'
# Create the full path for the new folder
config_folder_path = user_profile / new_folder_name

# Define the file name
file_name = 'localConfiguration.txt'
config_file_path = config_folder_path / file_name

# Check if the folder exists, and create it if it doesn't
if not config_folder_path.exists():
    config_folder_path.mkdir()



# default configuration 
template = '''
template_folder=D:/users/s005859/Pictures/templateRecognition/template
saving_folder=D:/users/s005859/Pictures/templateRecognition/saving
'''


def readLocalConfig():
    # Check if the file exists, and create it if it doesn't
    if not config_file_path.is_file():
        try:
            # 'x' mode will create the file, if it does not exist
            with open(config_file_path, 'x') as file:
                print(f"config file '{file_name}' created at {config_file_path}")
                file.write(template)
                # You can write to the file here if you need to
        except FileExistsError:
            print(f"configuration file already exist")
        finally:
            # Read the file and parse it into a dictionary
            variables_dict = {}
            with open(config_file_path, 'r') as file:
                for line in file:
                    # Remove any whitespace and split the line on '='
                    parts = line.strip().split('=')
                    if len(parts) == 2:
                        # Assign the variable name and value to the dictionary
                        variables_dict[parts[0]] = parts[1]
                        
            return variables_dict
    else:
        # Read the file and parse it into a dictionary
        variables_dict = {}
        with open(config_file_path, 'r') as file:
            for line in file:
                # Remove any whitespace and split the line on '='
                parts = line.strip().split('=')
                if len(parts) == 2:
                    # Assign the variable name and value to the dictionary
                    variables_dict[parts[0]] = parts[1]
        
        return variables_dict


def writeLocalConfigVariable(variable_name, variable_value):
    # Initialize an empty dictionary for the variables
    variables_dict = {}
    # Check if the config file exists
    if not os.path.isfile(config_file_path):
        try:
            # 'x' mode will create the file if it does not exist
            with open(config_file_path, 'x') as file:
                print(f"Config file '{file_name}' created at {config_file_path}")
                # Write the new variable to the file
                file.write(f"\n{variable_name} = {variable_value}\n")
        except FileExistsError:
            print("Configuration file already exists.")
    else:
        # File exists, read the existing variables
        with open(config_file_path, 'r') as file:
            for line in file:
                parts = line.strip().split(' = ')
                if len(parts) == 2:
                    variables_dict[parts[0]] = parts[1]

        # Update the variable's value or add it if it doesn't exist
        variables_dict[variable_name] = variable_value

        # Write the updated content back to the file
        with open(config_file_path, 'w') as file:
            for key, value in variables_dict.items():
                file.write(f"{key} = {value}\n")
        print(f"Updated variable '{variable_name}' in the configuration file with value {variable_value}.")
