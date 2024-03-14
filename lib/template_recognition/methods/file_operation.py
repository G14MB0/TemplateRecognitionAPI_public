import cv2
from typing import List, Tuple
from lib import local_config
from datetime import datetime
from lib.global_var import logFunctionDetail
from lib.global_var import logger




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
                position: List[Tuple[int]] = [(0,0), (0,0)],
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



def saveFrameWithTemplates(frame: cv2.typing.MatLike,
                            results: dict,
                            saving_folder: str,
                            rectangleColor: Tuple[int, int, int] = (0,255,0),
                            rectangleThickness: int = 2):
    

    for key, value in results.items():
        top_left = (value["position"][0], value["position"][1])
        bottom_right =  (top_left[0]+value["dimension"][1], top_left[1]+value["dimension"][0])
        cv2.rectangle(frame, top_left, bottom_right, rectangleColor, rectangleThickness)

        # Determina se c'è spazio sopra il rettangolo per il testo
        labelSize, baseLine = cv2.getTextSize(key, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        if top_left[1] - labelSize[1] - baseLine >= 0:  # Se c'è spazio sopra
            textOrg = (top_left[0], top_left[1] - baseLine)
        else:  # Altrimenti, posiziona il testo sotto il rettangolo
            textOrg = (top_left[0], bottom_right[1] + labelSize[1] + baseLine)

        # Disegna il nome del template sopra o sotto il rettangolo
        cv2.putText(frame, key, textOrg, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    
    cv2.imwrite(f'{saving_folder}/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}_{"TM"}.jpg', frame)
    
    return frame