import requests

# Define the base URL for the API
BASE_URL = "http://localhost:7386/api/v1/tm"
SETTING_URL = "http://localhost:7386/api/v1/setting"


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
    url = f"{BASE_URL}/startprocesses"
    response = requests.get(url)
    return response.json()

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
