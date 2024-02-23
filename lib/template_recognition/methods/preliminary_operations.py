import logging
from lib import local_config
from typing import List, Dict
import cv2
import os

# Retrieve the root logger
logger = logging.getLogger()


from functools import wraps
def logFunctionDetail(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]  # Convert all arguments to their string representation
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # Convert all keyword arguments
        signature = ", ".join(args_repr + kwargs_repr)  # Combine all strings together

        logger.info(f"Calling {func.__name__}({signature})")

        result = func(*args, **kwargs)
        return result
    return wrapper



@logFunctionDetail
def load_all_templates() -> Dict[str, cv2.typing.MatLike]:
    """Loads all the template from the tmeplate_folder as a dictionary [template_file_name: MatLike]

    Raises:
        ValueError: if template_folder has not been conifugred

    Returns:
        Dict[str, cv2.typing.MatLike]: the dicitonary containing all the template MatLike
    """    

    template_paths = []
    # Geth the template folder from settings
    template_folder = local_config.readLocalConfig().get("template_folder", "")
    if template_folder == "":
        logger.warning("Template Folder not configured, unable to load templates")
        raise ValueError("Template Folder not configured, unable to load  templates")

    # Iterate over all entries in the directory
    for entry in os.listdir(template_folder):
        # Create absolute path
        abs_path = os.path.join(template_folder, entry)
        # Check if it's a file and not a directory
        if os.path.isfile(abs_path):
            template_paths.append(abs_path)
    
    # All themplate dicitonary
    allTemplate = {}

    # Iterate through all the template_path and load them using cv2, then add to the dictionary
    for template_path in template_paths:
        base = os.path.basename(template_path)
        allTemplate[os.path.splitext(base)[0]] = cv2.imread(template_path)

    return allTemplate