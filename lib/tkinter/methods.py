from tkinter import Tk, filedialog


def tk_selectFile(fileType: str):
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
        return []
    

def tk_selectFolder():
    try:
        root = Tk()
        root.withdraw()
        root.attributes("-topmost",True)
        root.overrideredirect(True)
        folder = filedialog.askdirectory()
        return folder
    except:
        return []