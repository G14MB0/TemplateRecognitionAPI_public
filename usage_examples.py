import requests
import asyncio
import websockets
import json
import http.client

# Define the base URL for the API
BASE_URL = "http://localhost:7386/api/v1/tm"
SETTING_URL = "http://localhost:7386/api/v1/setting"

PORT = 7386


def set_setting(name, value):
    url = f"{SETTING_URL}"
    data = {
        "name": name,
        "value": value
    }
    response = requests.post(url, json=data)
    return response.json()


set_setting("template_folder", "PATH_TO_YOUR_TEMPLATE")


# Initialize the Manager with the desired settings
def initialize_manager():
    url = f"{BASE_URL}/init"
    data = {
        "processNumber": 4,
        "resolution": (1920, 1080),
        "multiprocess": True,
        "camIndex": 0,
        "showImage": False,
        "saveFrame": True,
        "showImageGray": False
    }
    response = requests.post(url, json=data)
    return response.json()

# Start the Processes
def start_processes():

    conn = http.client.HTTPConnection("localhost", PORT)  # or use HTTPSConnection for HTTPS
    conn.request("GET", "/api/v1/tm/startprocesses")

    response = conn.getresponse()
    print(response.status, response.reason)
    data = response.read()
    print(data.decode("utf-8"))

    conn.close()

    # url = f"{BASE_URL}/startprocesses"
    # response = requests.get(url)
    # return response.json()

start_processes()

# Load the Templates
def load_templates():
    url = f"{BASE_URL}/loadtemplate"
    response = requests.get(url)
    return response.json()

# Start Live Video
def start_live_video():
    url = f"{BASE_URL}/startvideo"
    response = requests.get(url)
    return response.json()

# Check Instant Trigger
def check_instant_trigger(templates):
    url = f"{BASE_URL}/check/instant"
    data = {"templates": templates}
    response = requests.post(url, json=data)
    return response.json()



async def receive_live_trigger(uri):
    async with websockets.connect(uri) as websocket:
        # Accept the connection
        print("Connected to the server")
        
        try:
            while True:
                message = await websocket.recv()
                print("Received message:", message)
                
        except websockets.exceptions.ConnectionClosed:
            print("Connection with the server was closed")
        except Exception as e:
            print(f"An error occurred: {e}")


# Replace "ws://localhost:8000/ws/startLiveTrigger" with your actual WebSocket server URI
# uri = "ws://localhost:7386/ws/startLiveTrigger"

# Start the event loop and the coroutine
# asyncio.get_event_loop().run_until_complete(receive_live_trigger(uri))


# # Example sequence of API calls following the flowchart
# if __name__ == "__main__":
#     # Initialize the Manager
#     init_response = initialize_manager()
#     print("Initialize Manager:", init_response)

#     # Decide if new templates need to be loaded based on some condition
#     # This is just an example condition; replace with your actual logic
#     new_template_condition = True
    
#     if new_template_condition:
#         # Load Templates
#         load_templates_response = load_templates()
#         print("Load Templates:", load_templates_response)
    
#     # Start Processes
#     start_processes_response = start_processes()
#     print("Start Processes:", start_processes_response)
    
#     # Start Live Video
#     start_live_video_response = start_live_video()
#     print("Start Live Video:", start_live_video_response)

#     # Here you would have your logic to check if the camera is correct
#     # Assuming the camera is correct, we proceed to check the instant trigger
#     camera_correct = True
    
#     if camera_correct:
#         # Check Instant Trigger with a list of template names
#         templates_to_check = ["template1", "template2"]
#         check_instant_trigger_response = check_instant_trigger(templates_to_check)
#         print("Check Instant Trigger:", check_instant_trigger_response)
