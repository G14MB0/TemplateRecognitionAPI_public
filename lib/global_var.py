"""
    This module, even if it's empty, is needed since is serve as container for global variable created by other modules!!!
"""
import time
from functools import wraps
from lib import local_config
import logging

# Retrieve the root logger
logger = logging.getLogger()


from functools import wraps
def logFunctionDetail(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]  # Convert all arguments to their string representation
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # Convert all keyword arguments
        signature = ", ".join(args_repr + kwargs_repr)  # Combine all strings together

        logger.info(f"Calling {func.__name__}({signature})")

        result = func(*args, **kwargs)
        return result
    return wrapper

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

# template matching threshold, default to 0.8
g_matching_threshold = local_config.readLocalConfig().get("MATCHING_THRESHOLD", 0.9)



class GlobalManager:
    """This class handle the template matching manager object globally
    """    
    def __init__(self):
        self.template_matching_manager = None
        pass
    
    def segGlobalManager(self, obj):
        self.template_matching_manager = obj
    
    def getGlobalManager(self):
        return self.template_matching_manager
    
# initialize the globalManager object
globalManager = GlobalManager()




