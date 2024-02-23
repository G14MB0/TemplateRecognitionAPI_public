from tkinter import Tk, filedialog
import threading
from queue import Queue


def thread_safe_file_dialog(q, file_type):
    root = Tk()
    root.withdraw()  # Hide the main window
    root.attributes("-topmost",True)

    if file_type:
        file_path = filedialog.askopenfilename(filetypes=[(f"{file_type} files", f"*.{file_type}")])
    else:
        file_path = filedialog.askopenfilename()
    root.destroy()
    q.put(file_path)

async def run_file_dialog(file_type: str = "") -> str:
    q = Queue()
    dialog_thread = threading.Thread(target=thread_safe_file_dialog, args=(q, file_type), daemon=True)
    dialog_thread.start()
    dialog_thread.join()  # Wait for the thread to finish
    return q.get()
    


def thread_safe_folder_dialog(q):
    try:
        root = Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        root.overrideredirect(True)
        folder = filedialog.askdirectory()
        root.destroy()
    except Exception as e:
        print(e)
        folder = ""
    q.put(folder)


async def run_folder_dialog() -> str:
    q = Queue()
    dialog_thread = threading.Thread(target=thread_safe_folder_dialog, args=(q,), daemon=True)
    dialog_thread.start()
    dialog_thread.join()  # Wait for the thread to finish
    return q.get()
    



