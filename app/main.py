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


'''
uvicorn app.main:app --reload #start the server without the main.py file
'''

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from .routes import strategyAPI, backtesterAPI

from contextlib import asynccontextmanager

import threading

import sys
import io
import os
import datetime


class DualOutput:
    def __init__(self, base_name):
        now = datetime.datetime.now()
        formatted_date = now.strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f"{base_name}_{formatted_date}.txt"
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        self.file = open(file_name, 'a')
        self.buffer = io.StringIO()

    def write(self, data):
        self.file.write(data)
        self.buffer.write(data)

    def getvalue(self):
        return self.buffer.getvalue()

    def flush(self):
        self.file.flush()
        self.buffer.flush()

    def close(self):
        self.file.close()
    
    def isatty(self):
        return False

# Creare una nuova istanza DualOutput per gestire l'output
# output_manager = DualOutput('D:\\ready2test\\log\\Ready2tesT_IOD\\live_output')
# sys.stdout = output_manager


origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """this lifespan metohod, used with the @asynccontextmanager decorator
    is the new way to deal with event in fastapi since the classical app.on("event") is deprecated
    """    

    # Code here runs after the app startup
    print("---------------------------------------------------------------")
    print("The app has started and this is the lifespan method telling you")
    print("---------------------------------------------------------------")

    yield  # This yield separates startup from shutdown code

    # Code here runs after the app stops

    # this is used to print all the thread that remains appended after the application close (if some opened by you), if any thread but MainThread is
    # still there, you need to handle that thread correctly in order to make it close before the app shutdown.
    # this can be appreciate if you use "reload" parameter, since it not works with not correctly closed thread
    print("This is a list of all appended that need to be closed, if there are many apart of 'MainThread', please fix it,.")
    for thread in threading.enumerate(): 
        print(thread.name)

    print("-------------------------------------------------------------")
    print("The app has stop and this is the liferspan method telling you")
    print("-------------------------------------------------------------")




app = FastAPI(
    title="simpleApp_Backend",
    version="0.1",
    root_path="",
    lifespan=lifespan  # this handle the lifespan method define before
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Filename", "Content-Length"]  # Esponi l'header X-Filename
)


# app.include_router(tkinter.router)



@app.get("/")
def root():
    return {"message": "This is the simpleApp_Backend API. Go to ./docs to see documentations"}


@app.get("/health")
def healt():
    """this is just an enpoint to reach for alive
    """    
    return {"message": "the server is online!"}


@app.get("/pid")
def getPID():
    """this method return the pid (process identifierc)

    Returns:
        process pid, web format
    """    
    current_pid = os.getpid()
    return {"current_pid": current_pid}


@app.get("/close")
def killAll():
    """termiate the current app using os module.
    It can't return nothing since the app stops
    """    
    os._exit(0)

@app.get("/console-output")
def get_console_output():
    """this method return the console output that is collected by the "DualOutput" object output_manager

    Returns:
        console output
    """    
    output = output_manager.getvalue()
    return {"output": output}
