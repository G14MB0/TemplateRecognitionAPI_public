#fastAPI things
from fastapi import APIRouter

from lib.timerHandler import timerHandler as th
from lib.iod.reporting import *
from app import schemas
import os
import json
import datetime


user_profile = os.environ.get('USERPROFILE')
new_folder_path = os.path.join(user_profile, 'Documents', 'Ready2tesT', 'IOD')
log_folder = os.path.join(new_folder_path, 'file')
# Checking if the folder exists, if not, create it along with the subfolder
if not os.path.exists(new_folder_path):
    os.makedirs(new_folder_path)
    print(f"Created folder: {new_folder_path}")

if not os.path.exists(log_folder):
    os.makedirs(log_folder)
    print(f"Created subfolder: {log_folder}")


router = APIRouter(
    prefix="/timerhandler",
    tags=['timerHandler']
)


@router.get("/")
def getInfo():
    return "TimerHandler"


def checkDeadline():
    """this fixed method is used to check if the current time is greater then the target time saved in the file target_time.json
    """    
    # Load the target time from the file
    with open(log_folder+'/target_time.json', 'r') as file:
        data = json.load(file)
        target_time = datetime.datetime.fromisoformat(data['target_time'])
        current_time = datetime.datetime.now()
        if current_time >= target_time:
            print("************************************")
            print("       END OF THE IOD PERIOD        ")
            print("************************************")
            print(f"curent time: {current_time} -- target time: {target_time}")



@router.post("/startiod")
def startIod(data: schemas.startIod):
    """start the IOD task by pushing the target time in the targer_time.json, used then by checkDeadline

    Args:
        data (schemas.startIod): _description_
    """    
    # Calculate the target time (data.interval is the timedelta in days)
    target_time = datetime.datetime.now() + datetime.timedelta(days=data.interval)
    # Store the target time in a file
    with open(log_folder+'/target_time.json', 'w') as file:
        json.dump({'target_time': target_time.isoformat()}, file)
    
    th.define_task(2, "s", checkDeadline)



@router.get("/stopiod")
def addTask():
    th.stop_all_tasks()


@router.get("/destroy")
def destroy():
    th.destroy()


@router.post("/startperiodicreport")
def startTask(data: schemas.startPeriodic):
    th.define_task(data.interval, data.mu, createReport, data.info)
    pass
