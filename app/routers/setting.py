from app import schemas
from lib import local_config

#fastAPI things
from fastapi import APIRouter


router = APIRouter(
    prefix="/setting",
    tags=['Settings']
)


@router.get("/")
def getSettings():
    settings = local_config.readLocalConfig()
    return settings


@router.post("/")
def setSetting(data: schemas.SetSetting):
    local_config.writeLocalConfigVariable(data.name, data.value)
    return local_config.readLocalConfig()

