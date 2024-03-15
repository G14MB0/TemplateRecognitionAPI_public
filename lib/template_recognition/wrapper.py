'''
Wrapper Module is used to define interface for the Manager class.
Here are defined all the function that are then published over API

Usage:
Always call initializeManager first to create the manager object, 
this will create the connection with camera and load all templates from 
the templates folder
'''


from lib.template_recognition.manager import Manager
from typing import Tuple
from lib.global_var import globalManager


def initializeManager(processNumber: int, 
                      resolution: Tuple[int, int] = (1920, 1080), 
                      multiprocess: bool = True, 
                      camIndex: int = 1, 
                      showImage: bool = False, 
                      saveFrame: bool = True,
                      returnFrame: bool = True,
                      showImageGray: bool = False):
    """ initialize the manager object and pass it to the global_var class globalManager

    Args:
        processNumber (int): number of processes for template matching
        resolution (Tuple[int, int], optional): camera resolution. Defaults to (1920, 1080).
        multiprocess (bool, optional): if true, activate the multiprocess. Defaults to True.
        camIndex (int, optional): index of the USB camera, depends on how Windows chose index for usb camera. Defaults to 1.
        showImage (bool, optional): If true, show a live video in proper methods. Defaults to False.
        saveFrame (bool, optional): if true, save a frame locally only in instantTrigger. Defaults to True.
        showImageGray (bool, optional): if true, the image (showImage) is converted to gray. Defaults to False.
    """    
    globalManager.segGlobalManager(Manager(camIndex=camIndex,
                                            showImage=showImage,
                                            processesNumber=processNumber, 
                                            res=resolution,
                                            multiprocess=multiprocess, 
                                            saveFrame=saveFrame,
                                            returnFrame=returnFrame,
                                            showImageGray=showImageGray))
    



def getInfo():
    """Print all info from manager object
    """    
    manager = globalManager.getGlobalManager()
    if manager:
        return manager.getInfo()
    else:
        print("manager not initialized yet, call initializeManager")
        return "manager not initialized yet, call initializeManager"


def loadAllTemplates():
    """Call this if templates are added or removed from folder after manager definition
    """    
    manager = globalManager.getGlobalManager()
    if manager:
        manager.loadAllTemplates()
    else:
        print("manager not initialized yet, call initializeManager")
        raise RuntimeError("manager not initialized yet, call initializeManager")

def startProcesses():
    manager = globalManager.getGlobalManager()
    if manager:
        manager.startProcesses()
    else:
        print("manager not initialized yet, call initializeManager")
        raise RuntimeError("manager not initialized yet, call initializeManager")


def startInstantTrigger(templates: list = []):
    """Start an instant trigger to check if *templates* are in the current frame

    Args:
        templates (list, optional): list of templates name. Defaults to [].

    Returns:
        dict: dictionary of results
    """    
    manager = globalManager.getGlobalManager()
    if manager:
        return manager.startInstantTrigger(templates)
    else:
        print("manager not initialized yet, call initializeManager")
        raise RuntimeError("manager not initialized yet, call initializeManager")
    

def startLiveVideo():
    manager = globalManager.getGlobalManager()
    if manager:
        manager.startLiveVideo()
    else:
        print("manager not initialized yet, call initializeManager")
    

def stopProcesses():
    manager = globalManager.getGlobalManager()
    if manager:
        manager.stop()
    else:
        print("manager not initialized yet, call initializeManager")


def closeAll():
    manager = globalManager.getGlobalManager()
    if manager:
        manager.close()
    else:
        print("manager not initialized yet, call initializeManager")




def changeLocalThreshold(value: int):
    if value < 0 or value > 1:
        raise ValueError("Trheashold should be in [0,1]")
    else:
        manager = globalManager.getGlobalManager()
        if manager:
            manager.threshold = value
            return {"message": f"threshold value correctly set to {value}"}
        else:
            raise RuntimeError("manager not initialized yet, call initializeManager")


def changeLiveTemplateList(value: list):
    manager = globalManager.getGlobalManager()
    if manager:
        manager.liveTemplateList = value
        return {"message": f"live template list value correctly set to {value}"}
    else:
        raise RuntimeError("manager not initialized yet, call initializeManager")


######################################################
##      FUNCTIONS DEFINED BUT NOT USED IN APIs      ##
######################################################
        
def startLiveTrigger():
    manager = globalManager.getGlobalManager()
    if manager:
        manager.startLiveTrigger()
    else:
        print("manager not initialized yet, call initializeManager")

def stopLiveTrigger():
    manager = globalManager.getGlobalManager()
    if manager:
        manager.stopLiveTrigger()
    else:
        print("manager not initialized yet, call initializeManager")


def startLiveSearching():
    pass


######################################################
##    METODI WRAPPER DI MODULI AGGIUNTIVI           ##
######################################################
from lib.template_recognition.methods import aruco_operations as ao


def getSetupDistance(res, camIndex):
    """get the setup distance using ARUCO

    Args:
        res (_type_): _description_
        camIndex (_type_): _description_

    Returns:
        _type_: _description_
    """    
    return {"distance": ao.calculateSetupDistance(res, camIndex)}