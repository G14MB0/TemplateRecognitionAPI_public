from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
from asyncio import sleep

from lib.pythonBus import pythonBus as pb
from lib.pythonBus import DAIO as d2

from app import schemas
from app.routers.pythonBus.support import getFreeAppChannel
from app.routers.pythonBus import utils

# Custom serialization function
def custom_serializer(obj):
    if isinstance(obj, pb.VectorCanChannel):
        # Here, you can decide how you want to represent your object.
        # For example, you might choose to just represent it with a string:
        return f"VectorCanChannel {obj.channelName}, channel num: {obj.channelNum}"
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")



dd = None


router = APIRouter(
    prefix="/pythonbus",
    tags=['Python Bus']
)


@router.get("/")
def getInfo():
    return "pythonbus"


@router.get("/availableHw")
def getAvailableHardware():
    """this return the dictionary of all available hardware 
    connected to the COM port of the pc.

    Returns:
        _type_: _description_
    """    
    return pb.getAvailableHw()


@router.post("/initialize")
def pythonBusInitialize(data: schemas.VectorChannelConfig):
    

    userChannelConfig = {
        "hw_channel": data.hw_channel, #the channel number (relative to the hardware physical channel)
        "serial_number": data.serial_number, #the number of the harware if more of the same type is connected
        "ch_num": data.ch_num, #application channel number (this should be managed automatically to avoid definition of channel usage number like CANoe)
        "hw_type": data.hw_type, #hardware type among the hardwareDict
        "bitrate": data.bitrate, #bitrate of the current channel
        "fd": data.fd,
        "data_bitrate": data.data_bitrate,
        "name": data.name
    }
    utils.canChannel[data.name] = pb.VectorCanChannel(userChannelConfig, data.db_path, data.txtLog)

    utils.canChannel[data.name].maxSize = data.maxSize
    utils.canChannel[data.name].decode = data.decode

    if data.propagate != "":
        temp = data.propagate.split(",")
        utils.canChannel[data.name].populatePropagation(temp)
        pass


    utils.canChannel[data.name].start()

    
    
    return {"message": "succesfully started the bus"}


@router.get("/canchannel")
def getActiveChannel():
    return json.dumps(utils.canChannel, default=custom_serializer)


@router.post("/daio/start")
def startDAIO(data: schemas.DAIOstart):
    global dd
    dd = d2.DAIOChannel(data.hw_index, data.frequency)
    dd.start()
    return {"message": "succesfully started the DAIO"}


@router.get("/daio/stop")
def stopDAIO():
    global dd
    dd.stop()
    return {"message": "succesfully stopped the DAIO"}


@router.get("/daio/startlog")
def startlogDAIO():
    global dd
    dd.startLog()
    return {"message": "succesfully started the DAIO log"}


@router.get("/daio/stoplog")
def stoplogDAIO():
    global dd
    dd.stopLog()
    return {"message": "succesfully stopped the DAIO log"}



@router.get("/all/stop")
def pbs():
    return utils.pythonBusStop()
    


@router.get("/all/startlog")
def sal():
    return utils.startAllLog()



@router.get("/all/stoplog")
def stal():
    return utils.stopAllLog()



@router.websocket("/ws/start")
async def websocket_endpoint(websocket: WebSocket):
    # Accept 
    await websocket.accept()
    try:
        while True:
            messages = []  # Array to collect messages
            for name in utils.canChannel.keys():
                if utils.canChannel[name].newMessageFlag:
                    messages = utils.canChannel[name].get_messages()
                    utils.canChannel[name].newMessageFlag = False

            # If there are messages, send them as a single array
            if messages:
                await websocket.send_text(json.dumps(messages))
            await sleep(0.5)
    except WebSocketDisconnect:
        # Handle the disconnect
        print("WebSocket disconnected")
        # Exit the while loop
        return