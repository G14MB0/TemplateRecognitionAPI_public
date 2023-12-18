"""
    This module, even if it's empty, is needed since is serve as container for global variable created by other modules!!!
"""
from queue import Queue

# global variable to handle voltage from DAIO. neet to be modified to work as VectorChannel
g_q_Voltage = Queue()