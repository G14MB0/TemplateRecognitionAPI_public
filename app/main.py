'''
uvicor app.main:app --reload #start the server
'''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from .routes import strategyAPI, backtesterAPI
from app.routers import tkinter, scheduler
from app.routers.pythonBus import pythonBus

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
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3007",
    "http://127.0.0.1:3007",
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield  # This yield separates startup from shutdown code
    # Code here runs after the app stops
    print("This is a list of all appended that need to be closed, if there are many apart of 'MainThread', please fix it.")
    for thread in threading.enumerate(): 
        print(thread.name)
    print("-----------------------------")
    print("Application is shutting down")
    print("-----------------------------")




app = FastAPI(
    title="Ready2tesT_IOD",
    version="0.1",
    root_path="",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Filename", "Content-Length"]  # Esponi l'header X-Filename
)


app.include_router(tkinter.router)
app.include_router(pythonBus.router)
app.include_router(scheduler.router)



@app.get("/")
def root():
    
    return {"message": "This is the Ready2tesT_IOD API. Go to ./docs to see documentations"}


@app.get("/health")
def healt():
    return {"message": "the server is online!"}


@app.get("/pid")
def getPID():
    current_pid = os.getpid()
    return {"current_pid": current_pid}


@app.get("/close")
def killAll():
    os._exit(0)

@app.get("/console-output")
def get_console_output():
    output = output_manager.getvalue()
    return {"output": output}
