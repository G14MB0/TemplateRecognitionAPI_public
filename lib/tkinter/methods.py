from tkinter import Tk, filedialog


def tk_selectFile(fileType: str = "") -> str:
    """ Use tkinter to opens a windows file selection dialog

        Errors are not handles. If any, it returns an empty string

    Args:
        fileType (str, optional): defining a fileType (like .txt) add the restriction to file selection. Defaults to "".

    Returns:
        str: the absolute file path
    """    
    try:
        root = Tk()
        root.withdraw()   
        root.wm_attributes('-topmost',1)
        if fileType != "":
            file = filedialog.askopenfilename(filetypes=[(f"{fileType} files", f"*.{fileType}")])
        else:
            file = filedialog.askopenfilename()
        print(file)
        return file
    except:
        return ""
    

def tk_selectFolder() -> str:
    """Use tkinter to opens a windows folder selection dialog

    Errors are not handles. If any, it returns an empty string

    Returns:
        str: the folder absolute path
    """    
    try:
        root = Tk()
        root.withdraw()
        root.attributes("-topmost",True)
        root.overrideredirect(True)
        folder = filedialog.askdirectory()
        return folder
    except:
        return ""