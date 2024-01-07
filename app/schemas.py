from typing import List, Optional, Dict, Any
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
##             LOGIN OPERATION SCHEMAS              ##
######################################################

class UserLogin(UserCreate):
    id: Optional[int]
    class Config:
        orm_mode = True
    # pass



######################################################
##             TOKEN OPERATION SCHEMAS              ##
######################################################

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None




######################################################
##           INVENTORY OPERATION SCHEMAS            ##
######################################################

class InventoryCreate(BaseModel):
    name: str
    description: Optional[str] = None

class InventoryResponse(InventoryCreate):
    id: int
    user_id: int
    created_at: datetime

class InventoryUpdate(BaseModel):
    name: str
    description: Optional[str] = None
    user_id: int