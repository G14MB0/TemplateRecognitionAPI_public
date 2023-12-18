from lib.pythonBus import DAIO as daio
from pprint import pprint
import time



dd = daio.DAIOChannel(0, 500)



try:

    dd.start()
    dd.startLog()
    
    while True:
        if dd.newMessageFlag:
            pprint(dd.get_messages())
            dd.newMessageFlag = False
except KeyboardInterrupt:
    dd.stop()
    dd.stopLog()
    