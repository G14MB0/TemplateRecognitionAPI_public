import ctypes
import threading
import time
import can
import traceback
from datetime import datetime
import os
from lib.global_var import g_q_Voltage

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



class DAIOChannel():
    def __init__(self, hwIndex, frequency, name = "DAIO", txtWriter = False, channelNum = 1):

        class DataStruct(ctypes.Structure):
            _fields_ = [("value_analog", ctypes.c_int * 4),
                        ("value_digital", ctypes.c_int)]

        # Carica la DLL
        self.daio = ctypes.CDLL("./lib/pythonBus/DAIO_dll.dll")
        # Carica la funzione getData
        self.get_data = self.daio.getData
        self.get_data.argtypes = [ctypes.POINTER(DataStruct)]
        self.get_data.restype = None

        # Variabile globale per memorizzare i dati
        self.my_data = DataStruct()
        self.messages = {}  # Dictionary to store received messages
        self.lastValue = 0

        self.txtWriter = txtWriter

        # self.hwIndex = hwIndex
        # self.frequency = frequency
        self.newMessageFlag = True

        self.frequency = frequency
        self.hwIndex = hwIndex
        self.channelNum = channelNum

        self.name = name
        self.file_index = 1 #this is used to increment the file counter after reaching max filesize and creating a new consequent file
        self.maxSize = 100 * 1024 * 1024 #100 Mb Max log file size

        # Flag per controllare l'esecuzione del thread
        self.running = True


    def _worker(self):
        while self.running:
            self.get_data(ctypes.byref(self.my_data))
            if self.my_data is not None:
                    # Convert the analog value to a format suitable for CAN (e.g., a byte array)
                    data = self.my_data.value_analog[0].to_bytes(4, byteorder='big', signed=False)  # adjust based on the expected range and precision
                    timestamp = time.time()
                    self.lastValue = f"{timestamp} {self.my_data.value_analog[0]}"

                    #this put the last value of voltage measurement in a global queue
                    g_q_Voltage.put(self.my_data.value_analog[0])

                    # Create a CAN message with ID 666
                    message = can.Message(arbitration_id=666, data=data, is_extended_id=False, timestamp=timestamp)
                    self.messages[666] = message
            time.sleep(self.frequency/1000)  # Intervallo tra le richieste
            self.newMessageFlag = True



    def _logger(self):
        if self.txtWriter:
            # Define the path for the text file
            max_file_size = 10 * 1024 # 10 Kb
            # Define the path for the text file
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%Y_%m_%d_%H_%M_%S")
            logFileName = formatted_datetime + "_" + str("DAIO") + ".txt"
            logFilePath = os.path.join(log_folder, logFileName)
            logFileName = formatted_datetime + "_" + str("DAIO") + "_" + str(self.file_index) + ".txt"

        while self.logging:
            try:
                for msg_id, msg in self.messages.items():
                    self.writer.on_message_received(msg)
                    if self.writer.file_size() > self.maxSize:
                        self.file_index += 1
                        logFileName = self.logFileName_base + "_" + str(self.file_index) + ".blf"
                        self.writer.stop()
                        self.writer = can.BLFWriter(os.path.join(log_folder, logFileName), channel=self.channelNum, append=False)
                    
                    if self.txtWriter:
                        # Open the text file in append mode and write the lastValue
                        # Check if file exceeds maximum size
                        if os.path.exists(logFilePath) and os.path.getsize(logFilePath) >= max_file_size:
                            # Create a new file with updated timestamp
                            current_datetime = datetime.now()
                            formatted_datetime = current_datetime.strftime("%Y_%m_%d_%H_%M_%S")
                            logFileName = formatted_datetime + "_" + str("DAIO") + ".txt"
                            logFilePath = os.path.join(log_folder, logFileName)

                        # Open the text file in append mode and write the lastValue
                        with open(logFilePath, 'a') as file:
                            file.write(str(self.lastValue) + "\n")
                        
            except Exception as e:
                self.stopLog()
                self.writer.stop()
                print(traceback.print_exc())
                print(f"error in logger, {e}")
            time.sleep(self.frequency/1000)
            


    def startLog(self):

        # Start reading CAN messages in a separate thread
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y_%m_%d_%H_%M_%S")
        logFileName = formatted_datetime + "_" + str(self.name) + ".blf"

        self.writer = can.BLFWriter(os.path.join(log_folder, logFileName), self.channelNum)
        self.logging = True
        can_thread = threading.Thread(target=self._logger)
        can_thread.start()

        return can_thread.native_id


    def stopLog(self):
        self.writer.stop()
        self.logging = False



    def start(self):
        # Start reading CAN messages in a separate thread
        self.running = True
        can_thread = threading.Thread(target=self._worker)
        can_thread.start()
        time.sleep(0.2)
        self.daio.start1(self.hwIndex, self.frequency) 
        return can_thread.native_id

    def stop(self):
        self.running = False
        self.daio.stop1()

    
    def get_messages(self):
        self.newMessageFlag = False
        return self.messages