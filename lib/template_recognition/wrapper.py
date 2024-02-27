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




######################################################
##      FUNCTIONS TO BE DEFINED      ##
######################################################
        
def startLiveTrigger():
    pass

def stopLiveTrigger():
    pass

def startLiveSearching():
    pass