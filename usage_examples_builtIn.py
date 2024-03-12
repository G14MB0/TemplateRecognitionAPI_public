import json
try:
    # Python 3
    from http.client import HTTPConnection
except ImportError:
    # Python 2
    from httplib import HTTPConnection


# Define the base URL and setting URL
BASE_URL = "http://localhost:7386/api/v1/tm"
SETTING_URL = "http://localhost:7386/api/v1/setting"
PORT = 7386


def set_setting(name, value):
    conn = HTTPConnection("localhost", PORT)
    url = "/api/v1/setting"
    data = {
        "name": name,
        "value": value
    }
    headers = {'Content-type': 'application/json'}
    conn.request("POST", url, body=json.dumps(data), headers=headers)
    response = conn.getresponse()
    return json.loads(response.read().decode('utf-8'))



def initialize_manager():
    conn = HTTPConnection("localhost", PORT)
    url = "/api/v1/tm/init"
    data = {
        "processNumber": 4,
        "resolution": [1920, 1080],  # Changed tuple to list for JSON serialization
        "multiprocess": True,
        "camIndex": 0,
        "showImage": False,
        "saveFrame": True,
        "showImageGray": False
    }
    headers = {'Content-type': 'application/json'}
    conn.request("POST", url, body=json.dumps(data), headers=headers)
    response = conn.getresponse()
    return json.loads(response.read().decode('utf-8'))


def start_processes():
    conn = HTTPConnection("localhost", PORT)
    conn.request("GET", "/api/v1/tm/startprocesses")
    response = conn.getresponse()
    print(response.status, response.reason)
    data = response.read()
    print(data.decode("utf-8"))
    conn.close()


def load_templates():
    conn = HTTPConnection("localhost", PORT)
    conn.request("GET", "/api/v1/tm/loadtemplate")
    response = conn.getresponse()
    return json.loads(response.read().decode('utf-8'))


def start_live_video():
    conn = HTTPConnection("localhost", PORT)
    conn.request("GET", "/api/v1/tm/startvideo")
    response = conn.getresponse()
    return json.loads(response.read().decode('utf-8'))


def check_instant_trigger(templates):
    conn = HTTPConnection("localhost", PORT)
    url = "/api/v1/tm/check/instant"
    data = {"templates": templates}
    headers = {'Content-type': 'application/json'}
    conn.request("POST", url, body=json.dumps(data), headers=headers)
    response = conn.getresponse()
    return json.loads(response.read().decode('utf-8'))


initialize_manager()