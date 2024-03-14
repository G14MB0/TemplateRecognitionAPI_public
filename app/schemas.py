"""
This module contain pydantic schemas used to validate APIs I/O.
You can find all the schemas in API reference
"""

from typing import Optional, Tuple, List, Dict
import json

from pydantic import BaseModel, validator, EmailStr, Field #used as an isistance() to check data type
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



######################################################
##      SETTING OPERATION SCHEMA      ##
######################################################
    
class SetSettings(BaseModel):
    name: str
    value: str


######################################################
##      TEMPLATE MATCHING SCHEMAS      ##
######################################################
    
class InitializeManager(BaseModel):
    processNumber: int = Field(default=4, description="The number of processes to be utilized. Defaults to 4.")
    resolution: Tuple[int, int] = Field(default=(1920, 1080), description="The resolution of the camera as a tuple (width, height). Defaults to 1920x1080.")
    multiprocess: bool = Field(default=True, description="Flag to enable or disable multiprocessing. Defaults to True.")
    camIndex: int = Field(default=1, description="The index of the camera to be used. Defaults to 1.")
    showImage: bool = Field(default=False, description="Flag to show the processed image in a window, works only with Live Matching, no instant matching. Defaults to False.")
    saveFrame: bool = Field(default=True, description="Flag to enable or disable saving of matched frames locally. Defaults to True.")
    returnFrame: bool = Field(default=True, description="Flag to enable or disable returning the frame after a instant match (with rectangles)")
    showImageGray: bool = Field(default=False, description="Flag to show the processed image in grayscale (used only if showImage is True). Defaults to False.")
    
    class Config:
        title = "Initialize Manager Configuration"
        description = "This model is used to initialize and configure the manager for image processing tasks. It includes settings for process number, image resolution, multiprocessing enablement, camera index, and flags for displaying and saving images."



class TemplateTriggering(BaseModel):
    templates: List[str] = Field(default=[], description="LList of template names. Each element is the name of a template (string) without its file extension.")


class TemplateTriggeringResponseBase(BaseModel):
    position: List[int] = Field(..., description="Position of detected template, relative to the current frame. Origin at the top left corner. Format: [x,y].")
    confidence: float = Field(..., description="Confidence level of the template match, expressed as a float between 0 and 1, where 1 represents 100% confidence.")

    class Config:
        title = "Template Triggering Response Base"



class TemplateTriggeringResponse(BaseModel):
    template: Dict[str, TemplateTriggeringResponseBase] = Field(..., description="Dictionary of template matching results. Each key is the template name, and each value is an instance of `TemplateTriggeringResponseBase` containing the match results.")

    class Config:
        schema_extra = {
            "description": "This model is used as input to trigger a one-shot template matching"
        }


class ChangeThreshold(BaseModel):
    threshold: float = Field(description="Value of threshold. Reset at any manager initialization. limits: [0,1]")



class ChangeTemplateList(BaseModel):
    templateList: List = Field(description="A list of template to search for in the LiveSearching method")


class SetUpDistance(BaseModel):
    res: Tuple[int, int] = Field(default=(1280,720), description="Camera Resolution")
    index: int = Field(default=0, description="Camera Index")