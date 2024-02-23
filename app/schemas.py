from typing import Optional
import json

from pydantic import BaseModel, validator, EmailStr #used as an isistance() to check data type
from datetime import datetime


######################################################
##              USER OPERATION TOKEN                ##
######################################################  

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str]
    role: Optional[str]


class UserUpdate(BaseModel):
    id: Optional[int] = None
    email: Optional[EmailStr] = None
    name: Optional[str]
    role: Optional[str]


class UserResponse(BaseModel):
    created_at: datetime
    email: EmailStr
    name: str
    id: int
    role: str
    created_at: datetime
    class Config:
        orm_mode = True



######################################################
##           DATA OPERATION SCHEMAS            ##
######################################################

class DataCreate(BaseModel):
    name: str
    data: str

    # # Serialize data when dumping to JSON
    # class Config:
    #     json_encoders = {
    #         dict: lambda v: json.dumps(v)
    #     }
        
    # @validator('data', pre=True, each_item=False)
    # def parse_json(cls, v):
    #     if isinstance(v, str):
    #         try:
    #             return json.loads(v)
    #         except ValueError:
    #             raise ValueError(f"Unable to parse string to dict: {v}")
    #     return v


class DataResponse(DataCreate):
    id: int
    owner_id: int
    created_at: datetime


class DataUpdate(BaseModel):
    name: str
    data: int

