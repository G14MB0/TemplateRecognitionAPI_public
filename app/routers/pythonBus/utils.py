'''
these methods are here in order to be used
in different part of the app.
'''

# this dict contain all the VectorCanChannel Object
canChannel = {}


def pythonBusStop():
    for key in canChannel.keys():
        canChannel[key].stop()
    return "succesfully stopped all the buses"
    

def startAllLog():
    for bus in canChannel.values():
        bus.startLog()
    return "Succesfully started all the logs"
    

def stopAllLog():
    for bus in canChannel.values():
        bus.stopLog()
    return "Succesfully stopped all the logs"
