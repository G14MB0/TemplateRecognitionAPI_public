"""
    This module, even if it's empty, is needed since is serve as container for global variable created by other modules!!!
"""
import time
from functools import wraps

def fps(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Start time of the loop
        iterations = 1  # How many tasks have been processed

        def calculate_fps():
            nonlocal iterations, start_time
            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time > 0:
                fps = iterations / elapsed_time
                print(f"{func.__name__} processed tasks at {fps:.2f} FPS", end="\r")
            start_time = current_time  # Reset the start time for the next interval
            iterations = 1  # Reset iterations

        result = func(*args, **kwargs, calculate_fps=calculate_fps)  # Pass the calculate_fps function to the worker
        return result
    return wrapper

g_matching_threshold = 0.9
