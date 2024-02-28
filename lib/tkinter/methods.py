from tkinter import Tk, filedialog
import threading
from queue import Queue


def thread_safe_file_dialog(q, file_type):
    """
    Opens a thread-safe file dialog allowing the user to select a file, and places the selected file path into a queue.

    This function creates a temporary, hidden Tkinter window to ensure the file dialog appears on top of all other windows.
    It's designed to run in a separate thread to avoid blocking the main application thread, especially useful in GUI applications
    that require a non-blocking file dialog.

    Parameters:
    - q (queue.Queue): The queue where the selected file path will be placed.
    - file_type (str): The type of file to filter for in the dialog. If empty, all file types will be shown.

    Returns:
    - None: This function places the selected file path into the provided queue and does not directly return a value.
    """
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
    """
    Asynchronously runs a file dialog to select a file of a specific type, ensuring thread safety.

    This function creates a separate thread to display the file dialog without blocking the main asyncio event loop,
    making it suitable for async applications. The selected file path is retrieved from a queue after the dialog is closed.

    Parameters:
    - file_type (str, optional): The type of files to display in the dialog. Defaults to an empty string, which shows all file types.

    Returns:
    - str: The path to the selected file. Returns an empty string if no file is selected or the dialog is cancelled.

    Note:
    - This function is designed to be used in async applications where blocking the event loop is undesirable.
    """
    q = Queue()
    dialog_thread = threading.Thread(target=thread_safe_file_dialog, args=(q, file_type), daemon=True)
    dialog_thread.start()
    dialog_thread.join()  # Wait for the thread to finish
    return q.get()
    


def thread_safe_folder_dialog(q):
    """
    Opens a thread-safe folder dialog allowing the user to select a directory, and places the selected directory path into a queue.

    Similar to thread_safe_file_dialog, this function creates a temporary, hidden Tkinter window to ensure the folder dialog
    appears on top of all other windows. It's designed to run in a separate thread to avoid blocking the main application thread,
    which is particularly useful in GUI applications requiring a non-blocking folder selection dialog.

    Parameters:
    - q (queue.Queue): The queue where the selected directory path will be placed.

    Returns:
    - None: This function places the selected directory path into the provided queue and does not directly return a value.

    Raises:
    - Exception: Captures and prints any exception that occurs during the folder selection process, returning an empty string as the folder path.
    """
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
    """
    Asynchronously runs a folder dialog to select a directory, ensuring thread safety.

    This function creates a separate thread to display the folder dialog without blocking the main asyncio event loop,
    making it suitable for async applications. The selected directory path is retrieved from a queue after the dialog is closed.

    Returns:
    - str: The path to the selected directory. Returns an empty string if no directory is selected or the dialog is cancelled.

    Note:
    - This function is designed to be used in async applications where blocking the event loop is undesirable.
    """
    q = Queue()
    dialog_thread = threading.Thread(target=thread_safe_folder_dialog, args=(q,), daemon=True)
    dialog_thread.start()
    dialog_thread.join()  # Wait for the thread to finish
    return q.get()
    



