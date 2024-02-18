# Copyright (c) 2023 Gianmaria Castaldini

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# In order to start the app, simply run this file.
# Modify first the capitalized parameter to match preferences!!!



import uvicorn
from app.main import app
import psutil 

# used to retrive openapi schema from fastAPI and save it in a file
import requests

### Parameters for uvicorn server
# HOST = "127.0.0.1"
HOST = "0.0.0.0"
PORT = 12345
WORKERS = 1

RELOAD = True # Reload the app after any save
APPPATH = "app.main:app"

### Parameters for openapi schema autosave
OPENAPI = False # If True, save a local copy of the openapi schema created by fastAPI



def serve(host: str, port: int, workers: int, reload: bool = False, appPath: str = ""):
    """This method start the FastAPI application using uvicorn

    Args:
        host (str): the app ip address
        port (int): the app port
        workers (int): if need multiprocess. 
        reload (bool, optional): is passed as the reload parameter of uvicorn. auto restart the app at any changes in the code.
        appPath (str, optional): if reload is True, the app argument must be passed as a string (like the one used directly in terminal)
    """    

    # Start the Uvicorn server
    if reload:
        if appPath == "":
            raise RuntimeError("The parameter appPath must be defined when reload is True! (something like app.main:app)")
        uvicorn.run(appPath, port=port, host=host, workers=workers, reload=reload)
    else:
        uvicorn.run(app, port=port, host=host, workers=workers, reload=reload)




if __name__ == "__main__":
    process = serve(HOST, PORT, WORKERS, reload=RELOAD, appPath=APPPATH)

    