from app import schemas
from app.database import get_db

from lib.template_recognition import wrapper as wp
from lib import global_var
from lib import local_config

import threading
import traceback
import time
from asyncio import sleep
import json
#fastAPI things
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

#pydantic things
from typing import  List #list is used to define a response model that return a list





router = APIRouter(
    prefix="/tm",
    tags=['Template Matching']
)


# Just to get info
@router.get("/")
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
        current = time.time()
        res = wp.startInstantTrigger(data.templates)
        print(f"check instant tooks: {time.time() - current}ms")
        return {"results": res}
    except Exception as e:
        print(traceback.print_exc())
        return {"error": str(e)}



@router.post("/mod/threshold")
def changeThreshold(data: schemas.ChangeThreshold):
    """Change the threshold vlaue of the manager object. it's atemporary change.
    
    """        
    try:
        res = wp.changeLocalThreshold(data.threshold)
        return res
    except Exception as e:
        print(traceback.print_exc())
        return {"error": str(e)}
    


@router.post("/mod/templatelist")
def changeLiveTemplateList(data: schemas.ChangeTemplateList):
    """Change the live template list vlaue of the manager object. it's a temporary change.
    
    """        
    try:
        res = wp.changeLiveTemplateList(data.templateList)
        return res
    except Exception as e:
        print(traceback.print_exc())
        return {"error": str(e)}
    

@router.post("/getsetupdistance")
def getSetupDistance(data: schemas.SetUpDistance):
    return wp.getSetupDistance(data.res, data.index)


@router.get("/stop")
def stopProcesses():
    """Stop any template matching operations and close multiprocessing pool
    """        
    try:
        wp.stopProcesses()
        return {"message": "Operations terminated, multiprocess pool closed"}
    except Exception as e:
        print(traceback.print_exc())
        return {"error": str(e)}
    

@router.get("/close")
def closeAll():
    """Stop any template matching operations and close multiprocessing pool and release the Camera
    """        
    try:
        wp.closeAll()
        return {"message": "Operations terminated, camera released"}
    except Exception as e:
        print(traceback.print_exc())
        return {"error": str(e)}
    


# def start_live_trigger_in_background(loop, manager):
#     asyncio.run_coroutine_threadsafe(manager.startLiveTrigger(), loop)

@router.websocket("/ws/startLiveTrigger")
async def websocket_endpoint_info(websocket: WebSocket):
    sample_time = local_config.readLocalConfig().get("LIVE_TRIGGER_INTERVAL", 0.25)
    # Accept 
    await websocket.accept()
    print("connection active")
    manager = global_var.globalManager.getGlobalManager()
    # manager.isLastLiveValueQueue = True
    if manager:
        print("manager live, start live triggering")

        threading.Thread(target=manager.startLiveTrigger).start()

        try:
            while True:
                lastValue = manager.getLastLiveValue()
                await websocket.send_text(json.dumps(lastValue))
                await sleep(float(sample_time))
        except WebSocketDisconnect:
            # Handle the disconnect
            manager.stopLiveTrigger()
            print("WebSocket disconnected")
            # Exit the while loop
            return
        except Exception as e:
            manager.stopLiveTrigger()
            print("WebSocket disconnected")
            return
        finally:
            # Make sure to close the executor to clean up resources
            # executor.shutdown(wait=False)
            manager.stopLiveTrigger()

    else:
        manager.stopLiveTrigger()
        print("manager not initialized yet, call initializeManager")
        await websocket.send_text(json.dumps({"error": "manager not initialized yet, call initializeManager"}))
        await websocket.close()