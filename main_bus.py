from lib.pythonBus import pythonBus as pb
from pprint import pprint



userChannelConfig1 = {
                        "hw_channel": 0, #the channel number (relative to the hardware physical channel)
                        "serial_number": 569535, #the number of the harware if more of the same type is connected
                        "ch_num": 0, #application channel number (this should be managed automatically to avoid definition of channel usage number like CANoe)
                        "hw_type": "VN1630", #hardware type among the hardwareDict
                        "bitrate": 500000, #bitrate of the current channel
                        "fd": True,
                        "data_bitrate": 2000000,
                        "name": "CAN1"
                    }

userChannelConfig2 = {
                        "hw_channel": 1, #the channel number (relative to the hardware physical channel)
                        "serial_number": 569535, #the number of the harware if more of the same type is connected
                        "ch_num": 1, #application channel number (this should be managed automatically to avoid definition of channel usage number like CANoe)
                        "hw_type": "VN1630", #hardware type among the hardwareDict
                        "bitrate": 500000, #bitrate of the current channel
                        "fd": True,
                        "data_bitrate": 2000000,
                        "name": "CAN2"
                    }

pprint(pb.getAvailableHw())

vc1 = pb.VectorCanChannel(userChannelConfig1, "./FD.dbc")
vc2 = pb.VectorCanChannel(userChannelConfig2, "./FD.dbc")

vc1.start()
vc2.start()

try:
    vc1.startLog()
    vc2.startLog()
    while True:
        if vc1.newMessageFlag:
            print(vc1.get_messages())
            print(f"BUSLOAD: {vc1.bus_load}")
except KeyboardInterrupt:
    vc1.stop()
    vc1.stopLog()
    vc2.stop()
    vc2.stopLog()