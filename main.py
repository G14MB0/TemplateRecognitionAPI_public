import uvicorn
from app.main import app
import sys
import psutil 


# HOST = "127.0.0.1"
HOST = "0.0.0.0"
PORT = 44280
WORKERS = 1


def serve(host: str, port: int, workers: int, wait: int = 15):

    # Check if a process is already running on the specified port and terminate it if found
    if is_process_running_on_port(port):
        terminate_process_on_port(port)

    # Start the Uvicorn server
    uvicorn.run("app.main:app", port=port, host=host, workers=workers, reload=True)



def signal_handler(signum, frame):
    print(f'Received termination signal {signum}')
    # Insert any cleanup code here
    sys.exit(0)


def is_process_running_on_port(port: int) -> bool:
    for conn in psutil.net_connections(kind="inet"):
        if conn.laddr.port == port:
            return True
    return False


def terminate_process_on_port(port: int):
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            proc_info = proc.info  # Access the 'info' property without parentheses
            if proc_info["name"].startswith("R2T"):
                for conn in proc.connections(kind="inet"):
                    if conn.laddr.port == port:
                        print(f"Terminating process {proc_info['pid']}")
                        proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


def hideConsole():
    try:
        import ctypes
        whnd = ctypes.windll.kernel32.GetConsoleWindow()
        if whnd != 0:
            ctypes.windll.user32.ShowWindow(whnd, 0)
    except:
        pass


if __name__ == "__main__":
    # Register signal handlers
    # signal.signal(signal.SIGINT, signal_handler)
    # signal.signal(signal.SIGTERM, signal_handler)
    
    hideConsole()
    process = serve(HOST, PORT, WORKERS)
    