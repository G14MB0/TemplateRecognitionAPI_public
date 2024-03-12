from lib import local_config
from typing import List, Dict, Tuple
import cv2
import os
from lib.global_var import logger
import json
import math


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
    """Loads all the template from the tmeplate_folder as a dictionary [template_file_name: MatLike].
    Loads only file with these extensions: .jpg, .jpeg, .png
    It also load a template_config.json file (if exists in the template folder) which contain templates resolution and setup distance.
    the template_config.json format must be:
    {
        "template_name": {
            "distance": "30",
            "resolution": {
                "w": 1920,
                "h": 1080
            }
        },
        ...
    }

    all this are example values

    if a template name is not found in the template_config.json, defaults value (found in local_config) are used.

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

    template_config = {}
    default_w = int(local_config.readLocalConfig().get("DEFAULT_RESOLUTION", "1920,1080").split(",")[0])
    default_h = int(local_config.readLocalConfig().get("DEFAULT_RESOLUTION", "1920,1080").split(",")[1])
    default_distance = float(local_config.readLocalConfig().get("DEFAULT_DISTANCE", -1))
    with open(f"{template_folder}/template_config.json", "r") as f:
        template_config = json.load(f)


    all_templates = {}
    # Iterate over all entries in the directory
    for entry in os.listdir(template_folder):
        abs_path = os.path.join(template_folder, entry)
        if os.path.isfile(abs_path) and abs_path.split(".")[1] in ["jpeg", "png", "jpg"]:
            base = os.path.splitext(os.path.basename(abs_path))[0]
            if base.endswith("_mask"):
                # This is a mask file
                template_name = base[:-5]  # Remove "_mask" from the end to get the template name
                if template_name in all_templates:
                    # Load and assign the mask to the corresponding template entry
                    if template_name in template_config.keys():
                        all_templates[template_name]['distance'] = template_config[template_name]["distance"]
                        all_templates[template_name]['resolution'] = template_config[template_name]["resolution"]
                    else:
                        all_templates[base]['distance'] = default_distance
                        all_templates[base]['resolution'] = {"w": default_w, "h": default_h}
                        logger.warning(f"the template {template_name} has not been found in template_config.json. Using default values")
                    all_templates[template_name]['mask'] = cv2.imread(abs_path, cv2.IMREAD_GRAYSCALE)
                else:
                    # Create a new entry for this template with only a mask
                    all_templates[template_name] = {'mask': cv2.imread(abs_path, cv2.IMREAD_GRAYSCALE)}
                    if template_name in template_config.keys():
                        all_templates[template_name]['distance'] = template_config[template_name]["distance"]
                        all_templates[template_name]['resolution'] = template_config[template_name]["resolution"]
                    else:
                        all_templates[base]['distance'] = default_distance
                        all_templates[base]['resolution'] = {"w": default_w, "h": default_h}
                        logger.warning(f"the template {template_name} has not been found in template_config.json. Using default values")
            else:
                # This is a template file
                if base in all_templates:
                    # Update the existing entry with the template image
                    if template_name in template_config.keys():
                        all_templates[base]['distance'] = template_config[base]["distance"]
                        all_templates[base]['resolution'] = template_config[base]["resolution"]
                    else:
                        all_templates[base]['distance'] = default_distance
                        all_templates[base]['resolution'] = {"w": default_w, "h": default_h}
                        logger.warning(f"the template {base} has not been found in template_config.json. Using default values")
                    all_templates[base]['value'] = cv2.imread(abs_path)
                else:
                    # Create a new entry for this template
                    all_templates[base] = {'value': cv2.imread(abs_path), 'mask': None}
                    if base in template_config.keys():
                        all_templates[base]['distance'] = template_config[base]["distance"]
                        all_templates[base]['resolution'] = template_config[base]["resolution"]
                    else:
                        all_templates[base]['distance'] = default_distance
                        all_templates[base]['resolution'] = {"w": default_w, "h": default_h}
                        logger.warning(f"the template {base} has not been found in template_config.json. Using default values")

    return all_templates




def scale_all_templates(allTemplates: Dict, setUpDistance: float, cameraRes: Tuple[int, int]) -> Dict:
    """_summary_

    allTemplates = {
        "template_name": {
            "mask": MatLike,
            "value": MatLike,
            "distance": float,
            "resolution": {
                "w": int,
                "h": int
            }
        },
        ...
    }

    Args:
        allTemplates (Dict): _description_
        setUpDistance (float): _description_
        cameraRes (Tuple[int, int]): _description_

    Returns:
        Dict: _description_
    """    
    if setUpDistance == -1:
        raise RuntimeError("No given setup distance. try adding in local_config!")

    allTemplates_new = {}

    camera_pixels = cameraRes[0]*cameraRes[1]

    for name, value in allTemplates.items():
        scale_factor = math.sqrt(camera_pixels / (int(value["resolution"]["h"]) * int(value["resolution"]["w"]))) * float(value["distance"]) / setUpDistance
        print(f"scaling factor for {name}: {scale_factor}")
        width = int(value["value"].shape[1] * scale_factor)
        height = int(value["value"].shape[0] * scale_factor)
        dim = (width, height)
        # resize image
        resized_value = cv2.resize(value["value"], dim, interpolation = cv2.INTER_AREA)

        resized_mask = None
        if value["mask"] is not None:
            resized_mask = cv2.resize(value["mask"], dim, interpolation = cv2.INTER_AREA)

        allTemplates_new[name] = {
            "value": resized_value,
            "mask": resized_mask,
            "distance": value["distance"],
            "resolution": {
                "w": int(value["resolution"]["h"] * scale_factor / 100),
                "h": int(value["resolution"]["w"] * scale_factor / 100)
            }
        }

    return allTemplates_new

