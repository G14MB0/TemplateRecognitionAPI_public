from typing import List, Optional, Dict, Any
import json

from pydantic import BaseModel, validator
from datetime import datetime


class UserChannelConfig(BaseModel):
    hw_channel: int
    serial_number: int
    ch_num: int  #application channel number
    hw_type: str #this is something like "VN1630" and is then converted in the method to the corresponding int
    bitrate: int = 500000
    fd: bool = False
    data_bitrate: int = 2000000 #if the fd parameter is true, this is used as data bitrate for the arbitration in CAN-FD
    name: str = "" # this is optional but is needed in the log filename.
    txtLog: bool = False


class VectorChannelConfig(UserChannelConfig):
    db_path: str
    maxSize: int = 100 * 1024 * 1024 #default 100 Mb, max file size for logging part
    decode: bool = False
    propagate: str = ""  #this must be a list of element separated by a comma (,). it will be used to propagate the value of those elements in all the code


class StopBus(BaseModel):
    name: str

class startIod(BaseModel):
    interval: int #interval from the end of the test in days

class startPeriodic(BaseModel):
    interval: int
    mu: str = "s" #the measurment unit of interval, should be "s", "m", "h"
    info: str = ""


class DAIOstart(BaseModel):
    hw_index: int = 0
    frequency: int = 1000

class DAIOlogStart(BaseModel):
    name: str