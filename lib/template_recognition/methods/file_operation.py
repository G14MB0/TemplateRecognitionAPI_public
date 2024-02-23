import cv2
from typing import List, Tuple
import logging
from lib import local_config
from datetime import datetime


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
def load_template(template_path: str, grayScale: bool = True) -> cv2.typing.MatLike:


    """load a template using opencv and return it as a MatLike.
    Make it in grayscale if grayScale is True

    Args:
        template_path (str): absolute path of template
        grayScale (bool, optional): if set to True, returns a grayscaled template. Defaults to True.

    Returns:
        cv2.typing.MatLike: the template
    """    
    
    template = cv2.imread(template_path)

    if grayScale:
        return cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    else:
        return template



@logFunctionDetail
def save_frame(frame: cv2.typing.MatLike,
               frame_name: str,
                withMatching: bool = True,
                position: List[Tuple[int, int], Tuple[int, int]] = [(0,0), (0,0)],
                rectangleColor: Tuple[int, int, int] = (0,255,0),
                rectangleThickness: int = 2):
    """Save a frame with a rectangle in the matching position if "withMatching" is True, else save just the frame

    Args:
        frame (cv2.typing.MatLike): the frame
        frame_name (str): frame name
        withMatching (bool, optional): create a rectangle in the matching area. Defaults to True.
        position (List[Tuple[int, int], Tuple[int, int]], optional): Matching bottom-left and top-right position. Defaults to [(0,0), (0,0)].
        rectangleColor (Tuple[int, int, int], optional): rectangle color. Defaults to (0,255,0).
        rectangleThickness (int, optional): rectangle thickness. Defaults to 2.

    Raises:
        ValueError: If saving folder has not been configured
    """       

    saving_folder = local_config.readLocalConfig().get("saving_folder", "")
    if saving_folder == "":
        logger.warning("Saving Folder not configured, unable to save the template")
        raise ValueError("Saving Folder not configured, unable to save the template")

    if withMatching:
        # Draw the rectangle on 'immagine'
        cv2.rectangle(frame, position[0], position[1], rectangleColor, rectangleThickness)
        cv2.imwrite(f'{saving_folder}/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}_{frame_name}', frame)

    else:
        cv2.imwrite(f'{saving_folder}/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}_{frame_name}', frame)

