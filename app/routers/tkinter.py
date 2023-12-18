#database, schemas and models
# from .. import schemas

#fastAPI things
from fastapi import APIRouter
from lib.tkinter.methods import *


router = APIRouter(
    prefix="/explorer",
    tags=['WindowsFileExplorer']
)


@router.get("/")
def getInfo():
    return "FileExplorer"


@router.get("/file")
def selectFile():
    """open a windows filedialog window to select a file path without path parameter
    """   
    file = tk_selectFile("")
    return file

@router.get("/file/{filetype}")
def selectFile(filetype = ""):
    """open a windows filedialog window to select a file path

    Args:
        filetype (_type_): the type of the file. must be inserted as without the dot (dbc and not .dbc)

    Returns:
        _type_: the path of the selected file
    """    
    file = tk_selectFile(filetype)
    return file


@router.get("/folder")
def selectFolder():
    folder = tk_selectFolder()
    return folder

