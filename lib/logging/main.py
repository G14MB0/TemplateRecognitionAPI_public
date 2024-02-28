import logging
import os
from pathlib import Path

# Get the user's home directory (equivalent to %USERPROFILE% in Windows)
user_profile = Path.home()
# Define the new folder name
new_folder_name = 'TemplateRecognitionAPI'
# Create the full path for the new folder
config_folder_path = user_profile / new_folder_name
logfolderPath = config_folder_path / "log"

# Define the file name

# Check if the folder exists, and create it if it doesn't
if not config_folder_path.exists():
    config_folder_path.mkdir()
if not logfolderPath.exists():
    logfolderPath.mkdir()


def configure_logger():
    # Configure the root logger
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler(f"{logfolderPath}/application.log"),
                            logging.StreamHandler()
                        ])
