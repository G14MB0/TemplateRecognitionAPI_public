import cv2
import numpy as np
from typing import List, Tuple



def globalMatching(frame: cv2.typing.MatLike,
                   template: cv2.typing.MatLike,
                   template_name: str,
                   search_area: List[Tuple[int, int]],
                   mask: cv2.typing.MatLike = None) -> Tuple[bool,List[int], str, float]:
    
    """
    Performs template matching over a given frame to find a specified template within an optional search area.
    The function can utilize a mask to focus on specific parts of the template. It returns whether the template
    was found, the location of the best match, the template's name, and the highest matching value.

    Parameters:
        frame (np.ndarray): The source image in which to search for the template.
        template (np.ndarray): The template image to be searched within the frame.
        template_name (str): A name or identifier for the template.
        search_area (List[Tuple[int, int]]): The top-left and bottom-right coordinates defining the search area within the frame.
                                             If the search area is [(0, 0), (0, 0)], the entire frame is searched.
        mask (np.ndarray, optional): An optional mask to apply on the template for focused searching. Must be the same size as the template.

    Raises:
        ValueError: If the mask is not of type np.ndarray or its dimensions do not match the template.
        ValueError: If the specified search area is smaller than the template.

    Returns:
        Tuple[bool, List[int], str, float]: A tuple containing a boolean indicating whether the template was found,
                                            the location of the top-left corner of the best match, the template's name,
                                            and the maximum correlation value found during matching.
    """
    if mask is not None:
        if not isinstance(mask, np.ndarray):
            return False, [0, 0], template_name, max_val
            raise ValueError("Mask must be a numpy ndarray")
        if mask.shape[:2] != template.shape[:2]:
            return False, [0, 0], template_name, max_val
            raise ValueError("Mask dimensions must match the template dimensions")
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    threshold = 0.85

    if search_area != [(0, 0), (0, 0)]:
        top_left_search, bottom_right_search = search_area
        cut_frame = frame_gray[top_left_search[1]:bottom_right_search[1], top_left_search[0]:bottom_right_search[0]]
        if cut_frame.shape[0] < template_gray.shape[0] or cut_frame.shape[1] < template_gray.shape[1]:
            raise ValueError("Search area is too small compared to the template size.")
        res = cv2.matchTemplate(cut_frame, template_gray, cv2.TM_CCOEFF_NORMED, mask=mask)
    else:
        res = cv2.matchTemplate(frame_gray, template_gray, cv2.TM_CCOEFF_NORMED, mask=mask)

    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val > threshold:
        if search_area != [(0, 0), (0, 0)]:
            max_loc = (max_loc[0] + top_left_search[0], max_loc[1] + top_left_search[1])
        return True, list(max_loc), template_name, max_val
    else:
        return False, [0, 0], template_name, max_val
    
