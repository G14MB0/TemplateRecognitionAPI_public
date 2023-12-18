import ctypes
import threading
import time
import can
import traceback
from datetime import datetime
import os


class DataStruct(ctypes.Structure):
    _fields_ = [("value_analog", ctypes.c_int * 4),
                ("value_digital", ctypes.c_int)]


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


# Carica la DLL
pd = ctypes.CDLL("./lib/pythonBus/DAIO_dll.dll")

# Carica la funzione getData
get_data = pd.getData
get_data.argtypes = [ctypes.POINTER(DataStruct)]
get_data.restype = None

# Variabile globale per memorizzare i dati
my_data = DataStruct()

# Flag per controllare l'esecuzione del thread
running = True
writer = None
messages = {}
frequency = 1000
logging = False
newMessageFlag = False
running = True
lastValue = 0


def _logger():
    global messages, writer, frequency, logging

    # Define the path for the text file
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y_%m_%d_%H_%M_%S")
    logFileName = formatted_datetime + "_" + str("DAIO") + ".txt"
    while logging:
        try:
            for msg_id, msg in messages.items():
                writer.on_message_received(msg)
                # Open the text file in append mode and write the lastValue
                with open(os.path.join(log_folder, logFileName), 'a') as file:
                    file.write(str(lastValue) + "\n")
                    
        except Exception as e:
            writer.stop()
            print(traceback.print_exc())
            print(f"error in logger, {e}")
        time.sleep(frequency/1000)


def startLog(name):
    global messages, writer, frequency, logging

    # Start reading CAN messages in a separate thread
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y_%m_%d_%H_%M_%S")
    logFileName = formatted_datetime + "_" + str(name) + ".blf"

    writer = can.BLFWriter(os.path.join(log_folder, logFileName))
    logging = True
    can_thread = threading.Thread(target=_logger)
    can_thread.start()

    return can_thread.native_id

def stopLog():
    global writer, logging
    writer.stop()
    logging = False


# Funzione eseguita dal thread
def data_acquisition_thread():
    global messages, writer, frequency, newMessageFlag, running, lastValue
    while running:
        get_data(ctypes.byref(my_data))
        if my_data is not None:
            # Convert the analog value to a format suitable for CAN (e.g., a byte array)
            data = my_data.value_analog[0].to_bytes(4, byteorder='big', signed=False)  # adjust based on the expected range and precision
            lastValue = my_data.value_analog[0]
            # Create a CAN message with ID 5000
            message = can.Message(arbitration_id=5000, data=data, is_extended_id=False, timestamp=time.time())
            messages[5000] = message
        time.sleep(frequency/1000)  # Intervallo tra le richieste
        newMessageFlag = True




def start(hw_index = 0, frequency = 1000):
    global pd, thread
    # Crea ed avvia il thread
    try:
        thread = threading.Thread(target=data_acquisition_thread)
        thread.start()
        pd.start1(hw_index, frequency)
    except:
        stop()


def stop():
    global running, thread
    running = False
    pd.stop1()
    thread.join()

