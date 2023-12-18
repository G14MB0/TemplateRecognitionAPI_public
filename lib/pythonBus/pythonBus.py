import can
import can.interfaces.vector as vt
import threading
from datetime import datetime
import cantools

import importlib

from collections import deque

import os
import traceback

from lib.pythonBus.support import flags


_MEGABYTE = 1024 * 1024
_KILOBYTE = 1024

APPNAME = "Ready2tesT_IOD"

# Getting the %USERPROFILE% environment variable
user_profile = os.environ.get('USERPROFILE')
new_folder_path = os.path.join(user_profile, 'Documents', 'Ready2tesT', 'IOD')
log_folder = os.path.join(new_folder_path, 'log')
# Checking if the folder exists, if not, create it along with the subfolder
if not os.path.exists(new_folder_path):
    os.makedirs(new_folder_path)
    print(f"Created folder: {new_folder_path}")

if not os.path.exists(log_folder):
    os.makedirs(log_folder)
    print(f"Created subfolder: {log_folder}")


harwareDict = {
    "VN1630": 57
}

defaultConfig = can.detect_available_configs(interfaces=['vector'])[0]

def getAvailableHw():
    channelConfig = {}
    channel_config = vt.get_channel_configs()
    for i in range(len(channel_config)):
        conf = channel_config[i]
        channelConfig[conf.serial_number] = {}

    #Recreate a smaller channelConfig dictionary to use them as a check when initialize a bus
    for i in range(len(channel_config)):
        conf = channel_config[i]
        set_flags = [flag for flag in flags if conf.channel_bus_capabilities & flag]
        channelConfig[conf.serial_number][conf.hw_channel] = {
                "name": conf.name,
                "hw_type": conf.hw_type,
                "bus_capabilites": set_flags,
                "hw_channel": conf.hw_channel,
                "transceiver_name": conf.transceiver_name,
                "hw_index": conf.hw_index
            }
    return channelConfig


class VectorCanChannel():
    def __init__(self, userChannelConfig, dbPath = "", txtLog = False):
        """_summary_

        Args:
            userChannelConfig (_type_): userChannelConfig = {
                                        #         "hw_channel": 0, #the channel number (relative to the hardware physical channel)
                                        #         "serial_number": 12345, #the number of the harware if more of the same type is connected
                                        #         "ch_num": 0, #application channel number (this should be managed automatically to avoid definition of channel usage number like CANoe)
                                        #         "hw_type": "VS1630", #hardware type among the hardwareDict
                                        #         "bitrate": 500000, #bitrate of the current channel
                                        #         "fd": False,
                                        #         "data_bitrate": 2000000
                                        #     }
            dbPath (str, optional): _description_. Defaults to "".
            logFileName (str, optional): _description_. Defaults to "".

        Raises:
            ValueError: _description_
        """        

        channelConfig = getAvailableHw()
        self.loadDb(dbPath)

        vt.VectorBus.set_application_config(app_name=APPNAME, app_channel=userChannelConfig["ch_num"], hw_channel=userChannelConfig["hw_channel"], hw_index=channelConfig[userChannelConfig["serial_number"]][0]["hw_index"], hw_type=harwareDict[userChannelConfig["hw_type"]])#, **defaultConfig)
        if not userChannelConfig["fd"]:
            print(1 in channelConfig[userChannelConfig["serial_number"]][userChannelConfig["hw_channel"]]["bus_capabilites"], channelConfig[userChannelConfig["serial_number"]][userChannelConfig["hw_channel"]]["transceiver_name"] != "")
            if 1 in channelConfig[userChannelConfig["serial_number"]][userChannelConfig["hw_channel"]]["bus_capabilites"] and channelConfig[userChannelConfig["serial_number"]][userChannelConfig["hw_channel"]]["transceiver_name"] != "":
                print(channelConfig[userChannelConfig["serial_number"]][userChannelConfig["hw_channel"]])
                self.bus = can.interface.Bus(bustype='vector', app_name=APPNAME, channel=userChannelConfig["ch_num"], bitrate=userChannelConfig["bitrate"])
            else:
                raise ValueError(f'channel {userChannelConfig["hw_channel"]+1} of the hardware {channelConfig[userChannelConfig["serial_number"]][userChannelConfig["hw_channel"]]["name"]} has no CAN capabilities')
        else:
            #TO BE IMPLEMENTED (FD FUNCTIONALITY)
            self.bus = can.interface.Bus(bustype='vector', app_name=APPNAME, channel=userChannelConfig["ch_num"], bitrate=userChannelConfig["bitrate"], fd=True, data_bitrate=userChannelConfig["data_bitrate"])

        self.channelNum = userChannelConfig["ch_num"]
        self.channelName = userChannelConfig["name"]
        self.bitrate = userChannelConfig["bitrate"]
        
        self.logging = False
        self.txtLog = txtLog
        
        self.listener = can.BufferedReader()
        self.notifier = can.Notifier(self.bus, [self.listener])  

        # can log (blf) max size
        self.file_index = 1 #this is used to increment the file counter after reaching max filesize and creating a new consequent file
        self.maxSize = 10 * _MEGABYTE

        self.messages = {}  # Dictionary to store received messages
        self.newMessageFlag = True

        self.decode = False
        self.propagate = {}

        # Initialize the message length queue and time window
        self.message_length_queue = deque()
        self.time_window = 1  # example time window in seconds
        self.message_times = deque()  # To keep track of message timestamps

        self.bus_load = 0

        self.running = True


    def populatePropagation(self, elements):
        from queue import Queue
        module = importlib.import_module("lib.global_var")
        for element in elements:
            if hasattr(module, element):
                print(f"gloabl_var already has the variable {element}")
                continue
            else:
                # If the variable does not exist, create it and set it to a default value
                default_value = Queue()  # You can define your default value
                setattr(module, element, default_value)
                self.propagate[element] = getattr(module, element)





    def calculateBusLoad(self):
        """
        Calculate the bus load over a given time window.

        Args:
            frame_lengths (list of int): List of frame lengths (in bits) for each frame transmitted on the bus.
            time_window (float): The time window over which to calculate the bus load (in seconds).

        Returns:
            float: The bus load as a percentage.
        """

        total_frame_bits = sum(self.message_length_queue)
        bus_capacity = self.bitrate * self.time_window  # Total number of bits that can be transmitted in the time window

        self.bus_load = (total_frame_bits / bus_capacity) * 100  # Bus load as a percentage
        


    def loadDb(self, dbPath):
        try:
            if dbPath != "":
                # This function load the .dbc
                self.DBC = cantools.database.load_file(dbPath)

                return
            else:
                self.DBC = None
                print("Database path is empty, skipping db parsing")
                return
                
        except Exception as e:
            raise RuntimeError(f"error parsing the database: {e}")


    def parseMsg(self, message) -> dict:
        """Return the message decoded by cantools

        Args:
            id (_type_): _description_

        Returns:
            dict: _description_
        """        
        try:
            return self.DBC.decode_message(message.arbitration_id, message.data)
        except:
            return message

    


    def _worker(self):
        while self.running:
            try:
                msg = self.listener.get_message(timeout=1)
                if msg is not None:
                    if self.DBC is not None:
                        if self.decode:
                            self.messages[msg.arbitration_id] = self.parseMsg(msg)
                            #now propagate the value of a signal if is required by self.propagate list
                            for message in self.propagate.keys():
                                if msg.arbitration_id == int(message.split(".")[0]):
                                    try:
                                        self.propagate[message].put(self.messages[msg.arbitration_id][message.split(".")[1]])
                                    except KeyError:
                                        print(f"the message {msg.arbitration_id} has no signal {message.split('.')[1]}")
                                    except Exception:
                                        print(e)
                                        
                        else:
                            self.messages[msg.arbitration_id] = msg
                        # self.messages[0] = msg
                    else:
                        self.messages[0] = msg

                    # Standard CAN frame sizes in bits
                    arbitration_id_size = 11 if not msg.is_extended_id else 29  # Standard ID: 11 bits, Extended ID: 29 bits
                    control_field_size = 4  # Example size, may vary
                    data_field_size = len(msg.data) * 8  # 8 bits per byte
                    
                    self.message_length_queue.append(arbitration_id_size + control_field_size + data_field_size)
                    self.message_times.append(msg.timestamp)

                    if self.message_times and msg.timestamp - self.message_times[0] > self.time_window:
                        self.message_length_queue.popleft()
                        self.message_times.popleft()
                    
                    self.calculateBusLoad()

                    self.newMessageFlag = True
                       
            except Exception as e:
                self.stop()
                print(traceback.print_exc())
                print(f"error in worker, {e}")



    def _logger(self):
        """This is the worker method for the blf log.
        it must be nested in a thread and log all the message in the can bus using BLFWriter of python-can.
        If self.txtLog is true, create also a txt log.
        If the filesize is greater then self.maxSize, it stops the current writer and create a new one increasing
        self.file_index but mantaining the previous part.

        as exception, it stops the writer and the logging thread
        """        
        print("Start log", str(self.channelName))
        if self.txtLog:
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%Y_%m_%d_%H_%M_%S")
            logFileName = formatted_datetime + "_" + str(self.channelName) + "_" + str(self.file_index) + ".txt"
        while self.logging:

            if self.logging == False:
                self.writer.stop()

            try:
                for msg in self.bus:
                    self.writer.on_message_received(msg)
                    if self.writer.file_size() > self.maxSize:
                        self.file_index += 1
                        logFileName = self.logFileName_base + "_" + str(self.file_index) + ".blf"
                        self.writer.stop()
                        self.writer = can.BLFWriter(os.path.join(log_folder, logFileName), channel=self.channelNum, append=False)
                    
                    if self.txtLog:
                        # Open the text file in append mode and write the lastValue
                        with open(os.path.join(log_folder, logFileName), 'a') as file:
                            file.write(str(self.parseMsg(msg)) + "\n")

                
                       
            except Exception as e:
                self.stopLog()
                self.writer.stop()
                print(f"error in logger, {e}")
            


    def startLog(self):
        # Start reading CAN messages in a separate thread
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y_%m_%d_%H_%M_%S")
        self.logFileName_base = formatted_datetime + "_" + str(self.channelName) 
        logFileName = self.logFileName_base + "_" + str(self.file_index) + ".blf"
        self.writer = can.BLFWriter(os.path.join(log_folder, logFileName), channel=self.channelNum, append=False)

        self.logging = True
        can_thread = threading.Thread(target=self._logger)
        can_thread.start()
        return can_thread.native_id


    def stopLog(self):
        self.logging = False


    def start(self):
        # Start reading CAN messages in a separate thread
        self.running = True
        can_thread = threading.Thread(target=self._worker)
        can_thread.start()
        return can_thread.native_id

    def stop(self):
        self.running = False
        self.notifier.stop()
        self.bus.shutdown()

    def get_messages(self):
        self.newMessageFlag = False
        return self.messages


