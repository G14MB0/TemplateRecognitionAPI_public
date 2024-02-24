"""
    This module, even if it's empty, is needed since is serve as container for global variable created by other modules!!!
"""
import time
from functools import wraps

def fps(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Tempo di inizio
        result = func(*args, **kwargs)  # Esecuzione della funzione
        end_time = time.time()  # Tempo di fine
        execution_time = end_time - start_time  # Calcolo del tempo di esecuzione
        if execution_time > 0:  # Prevenzione della divisione per zero
            fps = 1 / execution_time  # Calcolo degli FPS come inverso del tempo di esecuzione
            print(f"{func.__name__} executed at {fps:.2f} FPS")
        else:
            print(f"{func.__name__} executed too quickly to measure FPS accurately.")
        return result
    return wrapper


g_matching_threshold = 0.9
