from app import schemas
from app.database import get_db

from lib.template_recognition import wrapper as wp


from sqlalchemy.orm import Session
import traceback
#fastAPI things
from fastapi import status, HTTPException, APIRouter, Depends

#pydantic things
from typing import  List #list is used to define a response model that return a list


router = APIRouter(
    prefix="/tm",
    tags=['Template Matching']
)


# Just to get info
@router.get("/", response_model=List[schemas.DataResponse])
def getInfo():
    """ **Get all info of current manager object**
    """    
    return {"info": wp.getInfo()}




@router.post("/init")
def initializeManager(data: schemas.InitializeManager):
    """ **Initialize the manager object**

    Args:
      -  processNumber (int): number of processes for template matching.
      -  resolution (Tuple[int, int], optional): camera resolution. Defaults to (1920, 1080).
      -  multiprocess (bool, optional): if true, activate the multiprocess. Defaults to True.
      -  camIndex (int, optional): index of the USB camera, depends on how Windows chose index for usb camera. Defaults to 1.
      -  showImage (bool, optional): If true, show a live video in proper methods. Defaults to False.
      -  saveFrame (bool, optional): if true, save a frame locally only in instantTrigger. Defaults to True.
      -  showImageGray (bool, optional): if true, the image (showImage) is converted to gray. Defaults to False.
    """      

    processNumber = data.processNumber
    resolution = data.resolution
    multiprocess = data.multiprocess
    camIndex = data.camIndex
    showImage = data.showImage
    saveFrame = data.saveFrame
    showImageGray = data.showImageGray
    
    
    wp.initializeManager(processNumber=processNumber, 
                      resolution=resolution, 
                      multiprocess=multiprocess, 
                      camIndex=camIndex, 
                      showImage=showImage, 
                      saveFrame=saveFrame,
                      showImageGray=showImageGray)
    
    return {"message": "Manager initialized successfully"}



@router.get("/loadtemplate")
def loadTemplates():
    """ **Reload all the template from the templates folder**
    """    
    try:
        wp.loadAllTemplates()
        return {"message": "template updated correctly"}
    except Exception as e:
        return {"error": str(e)}



@router.get("/startprocesses")
def startProcesses():
    """ **Start the process execution pool**
    Since the template recognition can be run in a multiprocess environment, the process pool
    must be started.
    If the process pool isn't started before any operation and the multiprocess flag is set to True,
    it will return an error!

    """    
    try:
        wp.startProcesses()
        return {"message": "processes started correctly"}
    except Exception as e:
        return {"error": str(e)}
    

@router.get("/startvideo")
def startLiveVideo():
    """ Start a live video of the camera. 
    """    
    try:
        wp.startLiveVideo()
        return {"message": "video started correctly, press 'q' on video screen to stop it"}
    except Exception as e:
        return {"error": str(e)}
    


@router.post("/check/instant")
def checkInstantTrigger(data: schemas.TemplateTriggering):
    """Start the instant trigger check routine. It returns the results of template matching

    
    Returns:
        dict: {"resutls": result dictionary}

    result dicitonary:
    - templateName:
        - template position (x,y) from top-left corner of the frame
        - confidence (norm %) of the results
        - dimension [y,x, channel] where channel is the number of dimensions (if 3 generally is a colored image)
    """        
    try:
        res = wp.startInstantTrigger(data.templates)
        return {"results": res}
    except Exception as e:
        print(traceback.print_exc())
        return {"error": str(e)}

