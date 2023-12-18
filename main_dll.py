import ctypes
import threading
import time

class DataStruct(ctypes.Structure):
    _fields_ = [("value_analog", ctypes.c_int * 4),
                ("value_digital", ctypes.c_int)]

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

# Funzione eseguita dal thread
def data_acquisition_thread():
    while running:
        get_data(ctypes.byref(my_data))
        # Stampa o elabora i dati qui
        print("Analog Values:", list(my_data.value_analog))
        print("Digital Value:", my_data.value_digital)
        time.sleep(0.2)  # Intervallo tra le richieste

# Crea ed avvia il thread
thread = threading.Thread(target=data_acquisition_thread)
thread.start()

try:
    pd.start1(0, 1000)
except KeyboardInterrupt:
    running = False
    pd.stop1()
finally:
    running = False
    pd.stop1()
    thread.join()  # Aspetta che il thread finisca
