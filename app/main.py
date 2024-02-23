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
from app.routers import data

from app import models
from app.database import engine

from contextlib import asynccontextmanager

import threading



# This bind the database with the models (creating the tables if not present and all the stuff). no need for this if using Alembic 


origins = [
    "http://localhost:7387",
    "http://127.0.0.1:7387",
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """this lifespan metohod, used with the @asynccontextmanager decorator
    is the new way to deal with event in fastapi since the classical app.on("event") is deprecated
    """    

    models.Base.metadata.create_all(bind=engine) 
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
    title="Authentication and Data Management Interface",
    version="0.1",
    root_path="",
    lifespan=lifespan,  # this handle the lifespan method define before
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Filename", "Content-Length"]  # Esponi l'header X-Filename
)


app.include_router(data.router, prefix="/api/v1")



@app.get("/")
def root():
    return {"message": "This are the APIs. Go to ./docs to see documentations"}


@app.get("/health")
def healt():
    """this is just an enpoint to reach for alive
    """    
    return {"message": "the server is online!"}
