#database, schemas and models
# from .. import schemas

#fastAPI things
from fastapi import APIRouter
from lib.tkinter.methods import *
import os
import subprocess
from lib.local_config import config_folder_path


router = APIRouter(
    prefix="/tkinter",
    tags=['WindowsFileExplorer']
)


@router.get("/")
def getInfo():
    return "FileExplorer"


@router.get("/file")
def selectFile():
    """open a windows filedialog window to select a file path without path parameter
    """   
    file = run_file_dialog("")
    return file

@router.get("/file/{filetype}")
async def select_file(filetype: str = ""):
    """Open a Windows file dialog window to select a file path.

    Args:
        filetype (str): The type of the file, without the dot (e.g., 'dbc' not '.dbc').

    Returns:
        str: The path of the selected file.
    """    
    file_path = await run_file_dialog(filetype)
    print(file_path)
    return file_path


@router.get("/folder")
async def selectFolder():
    folder_path = await run_folder_dialog()
    print(folder_path)
    return folder_path



