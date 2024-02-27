from lib import local_config
from typing import List, Dict
import cv2
import os
from lib.global_var import logger


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

    all_templates = {}
    # Iterate over all entries in the directory
    for entry in os.listdir(template_folder):
        abs_path = os.path.join(template_folder, entry)
        if os.path.isfile(abs_path):
            base = os.path.splitext(os.path.basename(abs_path))[0]
            if base.endswith("_mask"):
                # This is a mask file
                template_name = base[:-5]  # Remove "_mask" from the end to get the template name
                if template_name in all_templates:
                    # Load and assign the mask to the corresponding template entry
                    all_templates[template_name]['mask'] = cv2.imread(abs_path, cv2.IMREAD_GRAYSCALE)
                else:
                    # Create a new entry for this template with only a mask
                    all_templates[template_name] = {'mask': cv2.imread(abs_path, cv2.IMREAD_GRAYSCALE)}
            else:
                # This is a template file
                if base in all_templates:
                    # Update the existing entry with the template image
                    all_templates[base]['value'] = cv2.imread(abs_path)
                else:
                    # Create a new entry for this template
                    all_templates[base] = {'value': cv2.imread(abs_path), 'mask': None}

    return all_templates