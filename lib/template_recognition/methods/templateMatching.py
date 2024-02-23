import cv2
 
 
def globalMathing(frame: cv2.typing.MatLike, template: cv2.typing.MatLike, template_name: str, searchArea: tuple = [(0,0), (0,0)]) -> tuple:
    """_summary_
 
    Args:
        frame (cv2.typing.MatLike): Frame
        template (cv2.typing.MatLike): template
        searchArea (tuple, optional): x,y for bottom_left and top_right. Defaults to [(0,0), (0,0)].
 
    Returns:
        tuple: (presence: bool, position: (x,y), template_name: str, confidence: float ]0,1))
    """    
 
   
    return (True, (500,600), template_name, 0.8954)


